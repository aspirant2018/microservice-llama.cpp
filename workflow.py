# The Class of the graphflow
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
import logging



import requests

url = "http://localhost:8080/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}


# Print response
#print(response.status_code)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class State(TypedDict):
    query:str
    response:str


import httpx

async def node1(State: State) -> State:

    logger.info(State)



    async with httpx.AsyncClient() as client:

        payload = {
            "model": "any-model",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a pirate."
                },
                {
                    "role": "user",
                    "content": f"{State['query']}"
                }
            ]
        }

        response = await client.post(url, headers=headers, json=payload)
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Raw response: {response.text}")
        try:
            assistant_answer = response.json()['choices'][0]['message']['content']
            return {'response': assistant_answer}
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {response.text}")
            raise e
        



class Workflow:
    def __init__(self,name):
        """Initialize a new compiled graph instance"""
        self.name = name
        self.builder = StateGraph(State)
        self.graph = self._build_graph()

        
    def _build_graph(self):
        """Construct and compile the graph"""
        
        # Add nodes
        self.builder.add_node("node1",  node1)
        # Add edges
        self.builder.add_edge(START, "node1")
        
        return self.builder.compile()
    
    def __call__(self, *args, **kwds):
        return f"{self.name}"
    
    