from fastapi.responses import JSONResponse

class AuthMiddleware:

    def __init__(self, app, routes):
        self.app = app
        self.routes = routes

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            if any(self._match_route(path, route) for route in self.routes):
                headers = dict(scope["headers"])
                auth_header = headers.get(b'authorization','')
                if not self._is_authorized(auth_header):
                    response = JSONResponse({"message": "Unauthorized"}, status_code=401)
                    await response(scope, receive, send)
                    return
        await self.app(scope, receive, send)
    
    def _match_route(self, path, route):
        if route.endswith("/**"):
            base_route = route[:-3]
            return path.startswith(base_route)
        return path == route
    
    def _is_authorized(self, auth_header):
        # Implement your authorization logic here
        #return auth_header == b"Bearer valid_token"
        return True
    
