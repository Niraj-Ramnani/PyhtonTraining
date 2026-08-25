from pydantic import BaseModel

class TaskSchema(BaseModel):
    title:str
    descrtipiton:str
    