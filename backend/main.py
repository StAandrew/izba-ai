from fastapi import FastAPI
from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
from tools.historical_data_tool import historical_data_tool_func
from tools.get_current_market_data import get_current_market_data
from tools.orchestrator import get_orchestrator_response

from agent_implementation import agent


app = FastAPI()

@app.get("/llama_index_agent/{user_query}")
def get_react_agent_response(user_query: str) -> dict[str,str]:
    response = agent.chat(
        user_query
    )
    return {
        "debug_info": "",
        "llm_response": response.response
    }

@app.get("/orchestrator/{user_query}")
def get_orchestrator_output(user_query: str) -> dict[str,str]:
    response = get_orchestrator_response(user_query)
    return {
        "debug_info": response["debug_info"],
        "llm_response": response["llm_response"]
    }

@app.get("/historical_prices/{user_query}")
def get_historical_prices(user_query: str) -> dict[str,str]:
    """
    Fetch historical price data.

    Example of a user query: "What was the difference in the average price between detached and terraced houses in January 2024?"
    """    
    response = historical_data_tool_func(user_query)

    return {
        "debug_info": response["debug_info"],
        "llm_response": response["llm_response"]
    }


@app.get("/current_listings/{user_query}")
def get_current_listings(user_query: str):
    """
    Fetch the current listings available.
    """
    response = get_current_market_data(user_query)

    return response