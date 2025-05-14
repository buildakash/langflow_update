from fastapi import APIRouter, HTTPException, Depends
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel
from typing import Optional
from langflow.services.auth import get_current_user
from langflow.services.deps import get_settings_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    system_message: Optional[str] = None
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-3.5-turbo"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@router.post("/chat_completion", response_model=ChatResponse)
async def process_chat(
    request: ChatRequest,
    settings_service=Depends(get_settings_service),
    current_user=Depends(get_current_user),
):
    try:
        chat = ChatOpenAI(
            temperature=request.temperature,
            model_name=request.model,
            openai_api_key=settings_service.settings.OPENAI_API_KEY,
        )
        
        messages = []
        if request.system_message:
            messages.append(SystemMessage(content=request.system_message))
        messages.append(HumanMessage(content=request.message))
        
        response = chat(messages)
        
        return ChatResponse(
            response=response.content,
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )