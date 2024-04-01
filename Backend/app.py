import uvicorn
from fastapi import FastAPI
from routers import authentication_router, user_routes, code_block_routes, folder_routes

app = FastAPI()
app.include_router(authentication_router.router)
app.include_router(user_routes.router)
app.include_router(code_block_routes.router)
app.include_router(folder_routes.router)


@app.get("/")
async def home():
    """Root endpoint"""
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run(app)
