import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

model_client = OpenAIChatCompletionClient(
    model='gpt-4o-mini',
    temperature=0.3
)

assistant = AssistantAgent(
    name='Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='You are a really helpful assistant who help on the task given.'
)

user_proxy_agent = UserProxyAgent(
    name ='UserProxy',
    description='you are a user proxy agent',
    input_func=input
)

termination_condition = TextMentionTermination(text='APPROVE')


team = RoundRobinGroupChat(
    participants=[assistant, user_proxy_agent],
    termination_condition=termination_condition,
    max_turns=10
)

stream = team.run_stream(task = 'Write a great poem about india?')

async def main():
    await Console(stream)

if (__name__ == '__main__'):
    asyncio.run(main())