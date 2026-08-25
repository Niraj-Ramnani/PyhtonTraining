# data transfer object ( data validation )
from pydantic import BaseModel

class ProductDTOS(BaseModel):
    id:int
    title:str
    price: int = 0