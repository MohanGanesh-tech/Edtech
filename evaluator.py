import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from outputFormator import EachAnswerEvaluatorOutputFormator, OverallEvaluatorOutputFormator
import redisConnection

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

client = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), temperature=0.8)
inMemory = redisConnection.RedisConnection()

with open('SystemMessage.json', 'r') as file:
    system_message_dict = json.load(file)

def EachQuestionEvaluator(student_id, answer):
    conversation = []
    system_message = SystemMessage(content=system_message_dict["eachQ&AEvaluator"])
    conversationWithoutSystemMessage = eval(inMemory.get(f'student:{student_id}'))
    human_message = HumanMessage(content=answer)
    conversation.append(system_message)
    conversation.extend(conversationWithoutSystemMessage)
    conversation.append(human_message)
    
    template = ChatPromptTemplate(messages=conversation)
    prompt_value = template.format()

    response = client.invoke(prompt_value, response_format={"type": "json_object"})
    parser = JsonOutputParser(pydantic_object=EachAnswerEvaluatorOutputFormator)
    parsed_response = parser.parse(response.content)

    ai_message = AIMessage(content=str(parsed_response))
    conversation.append(ai_message)
    inMemory.set(f'student:{student_id}', str(conversation[1:]))
    return parsed_response


def OverallStudentEvaluator(student_id):
    conversation = []
    system_message = SystemMessage(content=system_message_dict["overallStudenteveluator"])
    conversationWithoutSystemMessage = eval(inMemory.get(f'student:{student_id}'))
    conversation.append(system_message)
    conversation.extend(conversationWithoutSystemMessage)

    template = ChatPromptTemplate(messages=conversation)
    prompt_value = template.format()

    response = client.invoke(prompt_value, response_format={"type": "json_object"})
    parser = JsonOutputParser(pydantic_object=OverallEvaluatorOutputFormator)
    parsed_response = parser.parse(response.content)

    ai_message = AIMessage(content=str(parsed_response))
    conversation.append(ai_message)
    inMemory.set(f'student:{student_id}', str(conversation[1:]))
    return [parsed_response,conversation[1:]]