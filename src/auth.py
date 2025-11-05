import jwt, os
from bson.objectid import ObjectId as BsonObjectId
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pymongo.asynchronous.database import AsyncDatabase

class AuthMiddleware:

    def __init__(self, app, routes, aplicacao=None):
        self.app = app
        self.routes = routes
        self.aplicacao = aplicacao

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            if any(self._match_route(path, route) for route in self.routes):
                headers = dict(scope["headers"])
                auth_header = headers.get(b'authorization','')
                if not await self._is_authorized(auth_header, scope):
                    response = JSONResponse({"message": "Unauthorized"}, status_code=401)
                    await response(scope, receive, send)
                    return
        await self.app(scope, receive, send)
    
    def _match_route(self, path, route):
        if route.endswith("/**"):
            base_route = route[:-3]
            return path.startswith(base_route)
        return path == route
    
    async def _is_authorized(self, auth_header, scope):
        try:
            auth_header = auth_header.split(b" ")[1]
            dados = jwt.decode(auth_header, os.getenv("APP_SECRET_KEY", "secret"), algorithms=["HS256"])
            if dados["id"]:
                app: FastAPI = self.aplicacao
                db: AsyncDatabase = app.state.db
                registro = None
                if scope["path"].startswith("/perfil_pf"):
                    registro = await db["pessoas_fisicas"].find_one({"_id":BsonObjectId(dados["id"])})
                elif scope["path"].startswith("/perfil_pj"):
                    registro = await db["pessoas_juridicas"].find_one({"_id":BsonObjectId(dados["id"])})
                scope["current_user"] = registro
        except Exception as e:
            print(e)
            return False
        return True
    
