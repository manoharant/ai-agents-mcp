import os

import logfire
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()
logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))

client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
)
model = OpenAIModel(os.getenv('AZURE_OPENAI_MODEL_NAME'), provider=OpenAIProvider(openai_client=client))
agent = Agent(model,instrument=True)


async def main():
    result = await agent.run("hello!")
    while True:
        print(f"\n{result.output}")
        user_input = input("\n> ")
        result = await agent.run(user_input,
                                 message_history=result.new_messages(),
                                 )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
