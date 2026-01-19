"""
Todo app main python file
"""
from fastapi import FastAPI, APIRouter, Request

from app.api.v1.routers import  todo_routers
from app.core.config import settings
from app.core.logger import logger
from app.dependencies import db

## create fast api "app" object using settings
app = FastAPI(title=settings.app_name, debug=settings.debug)
logger.debug("Application successfuly started !")

## manage middleware 
## custom middleware to log every requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.debug(f"Completed with status {response.status_code}")
    return response


## CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# include routers 
app.include_router(todo_routers.router, tags=["todo"])



