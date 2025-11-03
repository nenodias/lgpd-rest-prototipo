import os
from pymongo import AsyncMongoClient

async def get_database() -> AsyncMongoClient:
    try:
        host = os.getenv("MONGO_HOST", "localhost")
        port = os.getenv("MONGO_PORT", "27017")
        user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        db_name = os.getenv("MONGO_INITDB_DATABASE", "lgpd_db")

        if user and password:
            uri = f"mongodb://{user}:{password}@{host}:{port}/?authSource=admin"
        else:
            uri = f"mongodb://{host}:{port}/"
        client = AsyncMongoClient(uri)
        return client
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

async def close_database(client: AsyncMongoClient):
    try:
        await client.close()
    except Exception as e:
        print(f"Error closing database connection: {e}")

        