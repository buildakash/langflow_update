from fastapi import APIRouter
from langflow.api.v1.endpoints import (
    chat,
    validate,
    flows,
    endpoints,
    components,
    chat_openai,
    openai_query,
    auth,  # Add this import
)

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router)  # Add this line
api_router.include_router(chat.router)
api_router.include_router(validate.router)
api_router.include_router(flows.router)
api_router.include_router(endpoints.router)
api_router.include_router(components.router)
api_router.include_router(
    chat_openai.router,
    prefix="/chat_openai",
    tags=["Chat OpenAI"]
)
api_router.include_router(
    openai_query.router,
    prefix="/openai_query",
    tags=["OpenAI Query"]
)