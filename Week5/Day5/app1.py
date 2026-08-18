from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return"Home page"

@app.get("/user")
def user():
    return "user page "


@app.get("/user/{userid}")
def user(userid : int ):
    return {f"page with user id {userid}"}


@app.get("/products")
def products(id : int ,cat : str ):
    return {
        "id" : id,
        "cat" : cat
    }