from fastapi import FastAPI

app = FastAPI(__name__)

@app.get("/")
async def test():
    return "Hi!"

