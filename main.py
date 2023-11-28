from fastapi import FastAPI, staticfiles
from routers import movements, bus_routes


app = FastAPI()

app.include_router(movements.router)
app.include_router(bus_routes.router)
app.mount('/routes', staticfiles.StaticFiles(directory='routes'), name='bus_routes')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
