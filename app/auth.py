# app/auth.py
import time
from typing import Any, Dict, Optional

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from .config import settings

HTTP_BEARER = HTTPBearer(auto_error=False)

ISSUER = settings.__dict__.get("CLERK_ISSUER") or ""
AUDIENCE = settings.__dict__.get("CLERK_AUDIENCE") or None
JWKS_URL = f"{ISSUER}/.well-known/jwks.json" if ISSUER else ""

# simple in-memory JWKS cache
_JWKS: Optional[Dict[str, Any]] = None
_JWKS_FETCHED_AT: float = 0
_JWKS_TTL = 60 * 60 * 12  # 12 hours


async def _get_jwks() -> Dict[str, Any]:
    global _JWKS, _JWKS_FETCHED_AT
    now = time.time()
    if _JWKS and (now - _JWKS_FETCHED_AT) < _JWKS_TTL:
        return _JWKS
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(JWKS_URL)
        r.raise_for_status()
        _JWKS = r.json()
        _JWKS_FETCHED_AT = now
        return _JWKS


def _pick_key(jwks: Dict[str, Any], kid: str) -> Optional[Dict[str, Any]]:
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            return k
    return None


async def require_user(creds: HTTPAuthorizationCredentials = Depends(HTTP_BEARER)) -> Dict[str, Any]:
    if not ISSUER:
        raise HTTPException(status_code=500, detail="CLERK_ISSUER not configured")

    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = creds.credentials

    # 1) find signing key by kid
    unverified = jwt.get_unverified_header(token)
    kid = unverified.get("kid")
    jwks = await _get_jwks()
    key = _pick_key(jwks, kid)
    if not key:
        # refresh JWKS once if kid is new
        _ = await _get_jwks()
        jwks = await _get_jwks()
        key = _pick_key(jwks, kid)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token key")

    # 2) decode & verify
    options = {}
    if not AUDIENCE:
        options["verify_aud"] = False  # if you didn't set an audience in Clerk

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=[key.get("alg", "RS256")],
            issuer=ISSUER,
            audience=AUDIENCE if AUDIENCE else None,
            options=options,
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token invalid: {e}")

    # payload contains sub (user id), email, etc.
    return payload
