from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from pydantic import BaseModel


from workflow import Workflow

import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

my_workflow = Workflow("workflow RAG")
print(my_workflow())
#response = my_workflow.graph.invoke({"query":'hello'})
#logger.info(response)


class queryInput(BaseModel):
    query: str



@app.post('/invoke')
async def invoke(input: queryInput):
    
    try:
        logger.info(f"query input from the user: {input.query}")

        response =  await my_workflow.graph.ainvoke({"query":input.query})
    
        # Return response
        return {"response": response['response']}
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))