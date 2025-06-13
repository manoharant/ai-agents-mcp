import os
from pydantic_ai.mcp import MCPServerStdio

import logfire
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()
logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))

trackspace_server = MCPServerStdio('uvx', [
        "mcp-atlassian",
        "--jira-url=https://trackspace.lhsystems.com",
        "--jira-personal-token=ODc3NzY0MTA4ODcxOiBJ9mv0YoroEjadWSd6IVQllX9G",
      ])

elastic_server = MCPServerStdio('npx', args=[
        "-y",
        "@elastic/mcp-server-elasticsearch",
      ],env={"ES_URL":"http://localhost:9200","ES_USERNAME":"test","ES_PASSWORD":"test","ES_INDEX":"filebeat-8.17.1-2025"})

client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
)
model = OpenAIModel(os.getenv('AZURE_OPENAI_MODEL_NAME'), provider=OpenAIProvider(openai_client=client))
agent = Agent(model,instrument=True,mcp_servers=[trackspace_server,elastic_server])



async def main():
    async with agent.run_mcp_servers():
        result = await agent.run("hello!")
        while True:
            print(f"\n{result.output}")
            user_input = input("\n> ")
            result = await agent.run(user_input,
                                     message_history=result.new_messages())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())