from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello World"}

@app.post("/{name}")
async def starname(name):
    return {f"Location: {name}"}
