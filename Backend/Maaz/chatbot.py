from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Initialize Ollama cloud model
llm = ChatOllama(model="gpt-oss:20b-cloud")  # replace with your model

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

    # Use invoke() method
    chain = llm | StrOutputParser()
    response = chain.invoke(chat_messages)

    return str(response)
