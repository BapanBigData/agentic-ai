import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
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
    name='Writer',
    description='you are a great writer',
    model_client=model_client,
    system_message='You are a skilled writer. Produce clear, concise, and engaging content based on the given input.'
)

assistant2 = AssistantAgent(
    name='Reviewer',
    description='you are a great reviewer',
    model_client=model_client,
    system_message='You are a professional reviewer. Evaluate the content critically and provide actionable feedback in under 30 words.'
)

assistant3 = AssistantAgent(
    name='Editor',
    description='you are a great editor',
    model_client=model_client,
    system_message='You are a skilled editor. Enhance the content for clarity, coherence, and grammar while preserving the original intent.'
)


team = RoundRobinGroupChat(
    participants=[assistant, assistant2, assistant3],
    max_turns=1
)

async def main():
    task = 'Complete the given: Where the mind is without fear and the head is held high..'

    while True:
        stream = team.run_stream(task=task)
        
        await Console(stream)

        feedback_from_user_or_application=input('Please Provide feedback to the team: ')

        if(feedback_from_user_or_application.lower().strip()=='exit'):
            break

        task = feedback_from_user_or_application

    
if (__name__ == '__main__'):
    asyncio.run(main())