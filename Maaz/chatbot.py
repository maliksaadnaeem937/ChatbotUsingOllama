from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
# Initialize Ollama client (Cloud or local)
# Replace "llama2" with your cloud model name if needed
client = ChatOllama(model="gpt-oss:20b-cloud")

def get_ai_response(messages: list[tuple[str, str]]) -> str:
    """
    messages: list of tuples (role, content)
    role: "user" or "assistant"
    returns: AI response as string
    """
    chat_messages = []
    for role, content in messages:
        if role.lower() == "user":
            chat_messages.append(HumanMessage(content))
        else:
            chat_messages.append(AIMessage(content))

    # Send messages to Ollama and get response
    response = client.chat(chat_messages)
    return response.content
