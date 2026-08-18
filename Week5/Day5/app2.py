from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    id : int 
    name : str
    email : str

@app.post("/user")
def createuser(user : User ){
    return{
        "name" : user.name,
        
    }
}