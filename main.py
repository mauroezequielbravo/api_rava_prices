import uvicorn
from fastapi import FastAPI
from routers import cedears, bonos

app = FastAPI()

app.include_router(cedears.router)
app.include_router(bonos.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
