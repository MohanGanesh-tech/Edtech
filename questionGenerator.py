
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from outputFormator import QuestionOutputFormator
import redisConnection
import asyncio

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

client = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)
inMemory = redisConnection.RedisConnection()

with open('SystemMessage.json', 'r') as file:
    system_message_dict = json.load(file)

# async def stream_output(prompt, response_format):
#     chunks = []
#     async for chunk in client.astream(prompt, response_format):
#         chunks.append(chunk)
#         print(chunk.content, end='', flush=False)

def IntialQuestionGenerator(student):
    conversation = []
    system_message = SystemMessage(content=str(system_message_dict["initalQuestionGenerator"]))

    prompt_template = PromptTemplate(
            input_variables=["grade"],
            template="I am {grade} grade student, ask me question releated to my grade"
        )
    human_message = HumanMessage(content=str(prompt_template.format(grade=student["grade"])))

    conversation.append(system_message)
    conversation.append(human_message)

    template = ChatPromptTemplate(messages=conversation)
    prompt_value = template.format()

    response = client.invoke(prompt_value, response_format={"type": "json_object"})
    # asyncio.run(stream_output(prompt_value, response_format={"type": "json_object"}))

    parser = JsonOutputParser(pydantic_object=QuestionOutputFormator)
    parsed_response = parser.parse(response.content)

    ai_message = AIMessage(content=str(parsed_response))
    conversation.append(ai_message)
    inMemory.set(f'student:{student["student_id"]}', str(conversation[1:]))
    return parsed_response


def NextQuestionGenerator(student_id):
    conversation = []
    system_message = SystemMessage(content=system_message_dict["nextQuestionGenerator"])
    conversationWithoutSystemMessage = eval(inMemory.get(f'student:{student_id}'))
    conversation.append(system_message)
    conversation.extend(conversationWithoutSystemMessage)

    template = ChatPromptTemplate(messages=conversation)
    prompt_value = template.format()

    response = client.invoke(prompt_value, response_format={"type": "json_object"})
    parser = JsonOutputParser(pydantic_object=QuestionOutputFormator)
    parsed_response = parser.parse(response.content)

    ai_message = AIMessage(content=str(parsed_response))
    conversation.append(ai_message)
    inMemory.set(f'student:{student_id}', str(conversation[1:]))
    return parsed_response