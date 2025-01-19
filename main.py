import uvicorn
from user.interface.controllers.user_controller import router as user_routers
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Container
from example.ch06_02.sync_ex import router as sync_ex_routers
from example.ch06_02.async_ex import router as async_ex_routers

app = FastAPI()
# container = Container()
app.container = Container()
app.include_router(user_routers)
app.include_router(sync_ex_routers)
app.include_router(async_ex_routers)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )

@app.get("/")
def hello():
    return {"hello": "FastAPI"}

if __name__ == "__name__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)