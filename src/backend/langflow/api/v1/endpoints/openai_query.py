from fastapi import APIRouter, HTTPException, Depends
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from typing import Optional
from langflow.services.auth import get_current_user
from langflow.services.deps import get_settings_service

router = APIRouter(tags=["OpenAI Query"])

class QueryRequest(BaseModel):
    query: str
    template: Optional[str] = "Question: {query}\n\nAnswer:"
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-3.5-turbo"

class QueryResponse(BaseModel):
    response: str
    status: str = "success"

@router.post("/process_query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    settings_service=Depends(get_settings_service),
    current_user=Depends(get_current_user),
):
    try:
        # Initialize OpenAI Chat model
        chat = ChatOpenAI(
            temperature=request.temperature,
            model_name=request.model,
            openai_api_key=settings_service.settings.OPENAI_API_KEY,
        )
        
        # Create prompt template
        prompt = PromptTemplate(
            input_variables=["query"],
            template=request.template
        )
        
        # Create and run chain
        chain = LLMChain(llm=chat, prompt=prompt)
        response = chain.run(query=request.query)
        
        return QueryResponse(
            response=response,
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )