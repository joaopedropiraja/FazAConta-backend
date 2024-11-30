# from contextlib import asynccontextmanager
# from uuid import UUID, uuid4
# from fastapi import FastAPI, HTTPException
# from beanie import (
#     Delete,
#     Insert,
#     Replace,
#     SaveChanges,
#     Update,
#     after_event,
#     init_beanie,
#     Document,
# )

# from fazaconta_backend.shared.infra.config.settings import Settings
# from motor.motor_asyncio import AsyncIOMotorClient
# import redis.asyncio as redis
# import os
# import uvicorn
# from pydantic import BaseModel, Field
# from typing import Optional, List


# class DomainEvents:
#     dEvents = []  # class (or static) variable

#     @staticmethod
#     def addDEvent(dEvent):
#         DomainEvents.dEvents.append(dEvent)


# # MongoDB settings
# MONGO_URI = Settings().mongo_uri
# DATABASE_NAME = Settings().database_name

# # Redis settings
# REDIS_HOST = os.getenv("REDIS_HOST", Settings().redis_host)
# REDIS_PORT = int(os.getenv("REDIS_PORT", Settings().redis_port))


# # User model for MongoDB (Beanie)
# class User(Document):
#     id: UUID = Field(default_factory=uuid4)
#     name: str
#     email: str
#     age: Optional[int] = None

#     @after_event(Insert, Replace, Update, Delete, SaveChanges)
#     def capitalize_name(self):
#         print(self.id)

#     class Settings:
#         name = "users"  # Collection name


# # Pydantic model for user input validation
# class UserCreate(BaseModel):
#     name: str
#     email: str
#     age: Optional[int] = None


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Initialize MongoDB
#     mongo_client = AsyncIOMotorClient(MONGO_URI)
#     await init_beanie(
#         database=mongo_client[DATABASE_NAME],
#         document_models=[User],  # Register the User model
#     )
#     print("Connected to MongoDB")

#     # Initialize Redis
#     redis_client = redis.from_url(
#         f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True"
#     )
#     print("Connected to Redis")

#     # Attach resources to `app.state`
#     app.state.mongo_client = mongo_client
#     app.state.redis = redis_client

#     # Yield to FastAPI application (setup complete)
#     yield

#     # Shutdown resources
#     await app.state.redis.close()
#     print("Redis connection closed")
#     mongo_client.close()
#     print("MongoDB connection closed")


# # Create FastAPI application with lifespan
# app = FastAPI(lifespan=lifespan)


# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to FazaConta Backend!"}


# @app.get("/health")
# async def health_check():
#     return {"status": "OK"}


# @app.get("/redis/test")
# async def redis_test():
#     """
#     Example route to test Redis functionality.
#     It sets and gets a value from Redis.
#     """
#     redis_client = app.state.redis
#     await redis_client.set("test_key", "test_value")
#     value = await redis_client.get("test_key")
#     return {"test_key": value}


# # User-related endpoints


# @app.post("/users", response_model=User)
# async def create_user(user_data: UserCreate):
#     """
#     Create a new user in the MongoDB database.
#     """
#     # DomainEvents.addEvent({"name": "João"})
#     user = User(**user_data.dict())
#     DomainEvents.addDEvent({"name": "joão"})
#     await user.insert()
#     return user


# @app.get("/users", response_model=List[User])
# async def get_users():
#     """
#     Retrieve all users from the MongoDB database.
#     """
#     print(DomainEvents.dEvents)
#     users = await User.find_all().to_list()
#     return users


# @app.get("/users/{user_id}", response_model=User)
# async def get_user(user_id: str):
#     """
#     Retrieve a user by ID.
#     """
#     user = await User.get(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @app.put("/users/{user_id}", response_model=User)
# async def update_user(user_id: str, user_data: UserCreate):
#     """
#     Update an existing user's data.
#     """
#     user = await User.get(user_id)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.name = user_data.name
#     user.email = user_data.email
#     user.age = user_data.age
#     await user.save()
#     return user


# @app.delete("/users/{user_id}")
# async def delete_user(user_id: str):
#     """
#     Delete a user by ID.
#     """
#     user = await User.get(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     await user.delete()
#     return {"detail": "User deleted successfully"}


# if __name__ == "__main__":
#     # uvicorn.run("fazaconta_backend.main:app", host="0.0.0.0", port=8000, reload=True)
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import uvicorn

from fazaconta_backend.shared.infra.http.app import App


app = App.connect()

if __name__ == "__main__":
    uvicorn.run("fazaconta_backend.main:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
