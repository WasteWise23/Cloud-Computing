from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from pydantic import EmailStr
from passlib.hash import bcrypt
from typing import List
import uuid
import data

app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserWithId(User):
    id: str

def generate_unique_id():
    return str(uuid.uuid4())

@app.get("/")
def welcome():
    return {"message": "Selamat Datang"}

@app.get("/get-users")
def get_users():
    if not data.data_list:
        return {"message" : "User list is Empty"}
    return data.data_list

@app.get("/get-user/{user_id}")
def get_data_withId(user_id: str):
    get_data = next((user for user in data.data_list if user.id == user_id), None)

    if get_data:
        return {"id": get_data.id, "name": get_data.name}
    
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/register")
def post_data(user: User):
    hashed_password = bcrypt.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    unique_id = generate_unique_id()
    item_with_id = UserWithId(**user.dict(), id=unique_id)
    data.data_list.append(item_with_id)
    return item_with_id.dict()
