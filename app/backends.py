from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    UnauthenticatedUser,
    SimpleUser,
)

from . import oauth2


class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        session_id = conn.cookies.get("session_id")

        username = oauth2.get_current_user(session_id)

        if username is None:
            roles = ["anon"]
            return AuthCredentials(roles), UnauthenticatedUser()

        roles = ["authenticated"]
        return AuthCredentials(roles), SimpleUser(username)
