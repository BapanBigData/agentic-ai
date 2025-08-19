import os
from dotenv import load_dotenv
import asyncio 
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


async def main(main_task):

    params = StdioServerParams(
        command = 'uvx',
        args=['mcp-server-time', '--local-timezone=Asia/Kolkata']
    )

    model = OpenAIChatCompletionClient(
        model='gpt-4o-mini',
        temperature=0.0
    )

    async with McpWorkbench(server_params=params) as workbench:
        
        print("=" * 100)
        tools = await workbench.list_tools()
        print(tools)
        print("=" * 100)
        print()
        
        agent = AssistantAgent(
            name='Agent',
            system_message='You are a helpful assistant',
            model_client=model,
            workbench=workbench,
            reflect_on_tool_use=True
        )

        async for message in agent.run_stream(task=main_task):
            print("-"*100)
            print(message)
            print('-'*100)
    
    return

if(__name__=='__main__'):
    main_task = 'What is the time in Yakutsk now?'
    asyncio.run(main(main_task))