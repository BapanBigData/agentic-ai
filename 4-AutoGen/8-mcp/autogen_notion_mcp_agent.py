import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination


from dotenv import load_dotenv
load_dotenv()


SYSTEM_MESSAGE = """
You are a helpful assistant that can search and summarize content from the user's Notion workspace and also list what is asked.
Try to assume the tool and call the same and get the answer. Say TERMINATE when you are done with the task.
"""


async def config():
    
    params = StdioServerParams(
        command="npx.cmd",
        args=['-y','mcp-remote','https://mcp.notion.com/mcp'],
        env={
            'NOTION_API_KEY': os.getenv("NOTION_API_KEY")
        },
        read_timeout_seconds=30
    )

    model = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        temperature=0.0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    mcp_tools= await mcp_server_tools(server_params=params)

    agent= AssistantAgent(
        name='notion_agent',
        system_message=SYSTEM_MESSAGE,
        model_client=model,
        tools=mcp_tools,
        reflect_on_tool_use=True
    )

    team = RoundRobinGroupChat(
        participants=[agent],
        max_turns=5,
        termination_condition=TextMentionTermination('TERMINATE')
    )

    return team


async def orchestrate(team, task):
    async for msg in team.run_stream(task=task):
        yield msg


async def main(task):
    team = await config()

    async for msg in orchestrate(team, task):
        print('-'*100)
        print(msg)
        print('-'*100)
    
    return

if __name__ =='__main__':
    task = 'Create a new page titled  "FitnessNotion"'
    asyncio.run(main(task))

# Note: Run the code on Terminal using CMD