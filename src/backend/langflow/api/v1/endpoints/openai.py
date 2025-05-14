from fastapi import APIRouter, HTTPException
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/openai", tags=["OpenAI"])

class QueryRequest(BaseModel):
    query: str
    temperature: float = 0.7
    model_name: str = "gpt-3.5-turbo"

class QueryResponse(BaseModel):
    response: str

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # Initialize OpenAI LLM
        llm = OpenAI(
            temperature=request.temperature,
            model_name=request.model_name
        )
        
        # Create a simple prompt template
        prompt = PromptTemplate(
            input_variables=["query"],
            template="Question: {query}\n\nAnswer:"
        )
        
        # Create and run the chain
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run(query=request.query)
        
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))