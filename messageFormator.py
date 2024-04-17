from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def convert_conversation(conversation):
    def message_to_dict(message):
        return {'role': message.type, 'content': message.content}
    return [message_to_dict(message) for message in conversation]

def convert_to_original(conversation_dicts):
    original_conversation = []
    for message_dict in conversation_dicts:
        if message_dict['role'] == 'system':
            original_conversation.append(SystemMessage(message_dict['content']))
        elif message_dict['role'] == 'human':
            original_conversation.append(HumanMessage(message_dict['content']))
        elif message_dict['role'] == 'ai':
            original_conversation.append(AIMessage(message_dict['content']))
        else:
            raise ValueError("Unknown message type")
    return original_conversation
