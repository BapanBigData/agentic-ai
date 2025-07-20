import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()


import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


model_client=OpenAIChatCompletionClient(
    model='gpt-4o-mini'
)


def reverse_string(text: str) -> str:
    '''
    Reverse the given text

    input:str

    output:str

    The reverse string is returned.
    '''
    return text[::-1]


reverse_tool = FunctionTool(reverse_string,description='A tool to reverse a string')



agent = AssistantAgent(
    name="ReverseStringAgent",
    model_client= model_client,
    system_message='You are a helpful assistant that can reverse string using reverse_string tool. Give the result with summary',
    tools=[reverse_tool],
    reflect_on_tool_use=True
)

async def main(): 
    result = await agent.run(task = 'Reverse the string "Hello, World!"')

    print(result.messages[-1].content)

if (__name__ == "__main__"):
    asyncio.run(main())

    # print(reverse_string("Hello, World!"))