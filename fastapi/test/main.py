from fastapi import FastAPI
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"},{"item_name": "Boo"}] 

@app.get("/")
async def read_something():
    return {"msg":"Hello World"}

#item_id will be read as a string here
@app.get("/item/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

#item_id will be read as an integer here (and a validation error (422) will appear if something other than an int is input)
@app.get("/things/{thing_id}")
async def read_thing(thing_id:int):
    return {"thing_id": thing_id}

@app.get("/models/{model_name}") 
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return{"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return{"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}

#query parameters with defaults
@app.get("/items/")
async def read_items_db(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#optional parameters can be made by setting their default to None
@app.get("/item-optional/{item_id}")
async def read_item_optional(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q" : q}
    return{"item_id": item_id}


    

