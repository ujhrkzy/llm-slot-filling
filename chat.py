from langchain.chat_models import ChatOpenAI

from app.slot_filling_conversation import SlotFilling
from app.slot_memory import SlotMemory

llm = ChatOpenAI(temperature=0.7)
memory = SlotMemory(llm=llm)
slot_filling = SlotFilling(llm=llm, memory=memory)
chain = slot_filling.create()

command = input("You: ")
while True:
    response = chain.predict(input=command)
    print(f"AI: {response}")
    slot_filling.log()
    command = input("You: ")
    if command == "exit":
        break
