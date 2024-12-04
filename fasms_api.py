from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/applicants")
def create_person():
    return {"create": "applicant"}

@app.post("/api/application")
def create_application():
    return {"create": "application"}
    # new applications

@app.get("/api/applicants")
def get_persons():
    return {"list": "applicant"}

@app.get("/api/schemes")
def get_schemes():
    return {"list": "schemes"}

@app.get("/api/schemes/eligible")
def get_schemes_eligible ():
    assert( False)

