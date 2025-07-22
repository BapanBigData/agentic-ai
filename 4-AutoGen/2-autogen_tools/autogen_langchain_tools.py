import warnings
warnings.filterwarnings("ignore", message="Importing debug from langchain")

import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


model_client=OpenAIChatCompletionClient(
    model='gpt-4o-mini',
    temperature=0.3,
    api_key=api_key
)

search_tool = TavilySearch()

def search_web(query:str) ->str:
    """Search the web for the given query and return the results."""
    
    try:
        results = search_tool.invoke(query)
        return results
    except Exception as e:
        print(f"Error occurred while searching the web: {e}")
        return "No results found." 
    

search_agent = AssistantAgent(
    name="SearchAgent",
    model_client=model_client,
    tools=[search_web],
    description="An agent that can search the web for information.",
    system_message="You are a helpful assistant that can search the web for information using the search_web tool." \
    "Please make sure that you use the search_web tool to find information before you return the answer." \
    "don't send the year in query, rather use latest or recently etc.",
    reflect_on_tool_use=True,
)

async def run_search():
    """Run the search agent with a sample query."""
    
    query = "What is the latest news on crude oil and Trump Tariff?" 
    print(f"Querying: {query}")
    
    
    result = await search_agent.run(task=query)
    
    # print(result.messages[-1])
    # print('\n')
    
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(run_search())