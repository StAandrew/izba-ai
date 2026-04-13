import json
import os
import requests

from dotenv import load_dotenv, find_dotenv


def use_search_engine(input: str) -> str:
    """This tool takes in some string as an input and provides a result of a basic internet search as a string.
    
    Use this tool for queries not covered by other tools.
    """
    
    URL = "https://api.tavily.com/search"

    # Define the parameters for the API request
    load_dotenv(find_dotenv())
    payload = {
        "api_key": os.environ.get("TAVILY_API_KEY"),
        "query": input,
        "search_depth": "basic",
        "include_answer": True,
        "include_images": False,
        "include_image_descriptions": False,
        "include_raw_content": False,
        "max_results": 5,
        "include_domains": [],
        "exclude_domains": []
    }

    # Set the appropriate headers (if needed, such as for content type)
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(URL,headers=headers,data=json.dumps(payload))

    search_answer = response.json()["answer"]

    return search_answer