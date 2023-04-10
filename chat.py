from langchain.chat_models import ChatOpenAI

from app.slot_filling_conversation import SlotFillingConversationChain
from app.slot_memory import SlotMemory

llm = ChatOpenAI(temperature=0.7)
memory = SlotMemory(llm=llm)
chat = SlotFillingConversationChain.create(llm=llm, memory=memory)

command = input("You: ")
while True:
    response = chat.predict_demo(input=command)
    print(f"AI: {response}")
    command = input("You: ")
    if command == "exit":
        chat.log()
        break
