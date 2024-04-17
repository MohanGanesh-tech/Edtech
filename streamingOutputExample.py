from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
llm = ChatOpenAI()

async def stream_output(prompt):
    chunks = []
    
    async for chunk in llm.astream(prompt):
        chunks.append(chunk)
        print(chunk.content, end='', flush=True)

print(asyncio.run(stream_output("hello. tell me something about yourself")))
