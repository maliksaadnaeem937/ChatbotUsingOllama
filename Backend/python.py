from langchain_ollama import ChatOllama
llm = ChatOllama(model="gpt-oss:20b-cloud")

print("Ask questions. Type 'quit' to exit.\n")

while True:
    question = input("You: ")
    
    if question.lower() == 'quit':
        break
    
    response = llm.invoke(question)
    print(f"AI: {response.content}\n")