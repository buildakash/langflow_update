from fastapi import APIRouter, HTTPException, Depends
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["OpenAI"])  # Remove prefix here

class ChatRequest(BaseModel):
    message: str
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-3.5-turbo"

class ChatResponse(BaseModel):
    response: str

@router.post("/")  # Changed from /chat to /
async def chat_endpoint(request: ChatRequest):  # Removed auth dependency for testing
    try:
        chat = ChatOpenAI(
            temperature=request.temperature,
            model_name=request.model
        )
        
        messages = [HumanMessage(content=request.message)]
        response = chat(messages)
        
        return ChatResponse(response=response.content)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )