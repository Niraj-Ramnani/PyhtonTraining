from fastapi import FastAPI,Request
from mockdata import products
from dtos import ProductDTOS
app = FastAPI()

@app.get("/")
def home():
    return "Home page"

@app.get("/products")
def getproducts():
    return products

# path parameters
@app.get("/product/{product_id}")
def getproduct(product_id: int):
    for x in products:
        if x.get("id") == product_id:
            return x
    return {"error": "product not found"}  

#  query parameters
@app.get("/greet")
def greet(name : str , age : int ):
    return{
        "greet" : f"hello {name} , your age is {age}" 
    }

# query params using request

@app.get("/greeting")
def greeting(request:Request):
    query_params = dict(request.query_params)
    return{
        "greeting" : f"Hello {query_params.get("name")} , your age is {query_params.get("age")}"
    }


## post route
@app.post("/create_product")
def create_product(product_data:ProductDTOS):
    # print(product_data)
    product_data = product_data.model_dump()
    products.append(product_data)
    return {"satus":"product created " , "data " : product_data}

# Put method

@app.put("/update_product/{product_id}")
def update_product(product_data:ProductDTOS , product_id : int):
    for i, x in enumerate(products):
        if x.get("id") == product_id:
            products[i] = product_data.model_dump()
            return {"status":"Products updated" , "product" : product_data}
    return{"error" : "product not found"}


# Delete method

@app.delete("/delete_product/{product_id}")
def delete_product(product_id:int):
    for i, x in enumerate(products):
        if x.get("id") == product_id:
            deleted_product = products.pop(i)
            return {"status" : "product deleted " , "product" : deleted_product}
    return{"error" : "product not found"}