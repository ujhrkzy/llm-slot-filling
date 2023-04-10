# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

_DEFAULT_SLOT_EXTRACTION_TEMPLATE = """
You are an AI assistant, reading the transcript of a conversation between an AI and a human.
From the last line of the conversation, extract all proper named entity(here denoted as slots) that match about restaurant reservation.
The named entity tag required for a restaurant_reservation are palce, number_of_people, and start_datetime.

The output should be returned in the following json format.
{{
    "restaurant_address": "Define restaurant address identified from the conversation. Do not include nouns in the address, such as the name of a store; define only the city."
    "number_of_people": "Define the number of people identified from the conversation. Define only numbers."
    "reservation_datetime": "Define start datetime(yyyy/mm/dd hh:mi) identified from the conversation. Format should follow yyyy/mm/dd hh:mi"
}}

If there is no match for each slot, assume null.(e.g., user is simply saying hello or having a brief conversation).

EXAMPLE
Conversation history:
Person #1: 新しいプロジェクトが開始した
AI: "Good luck!"
Current Slots: {{"restaurant_address": null, "number_of_people": null, "reservation_datetime": null}}
Last line:
Person #1: プロジェクトメンバーとの親睦を兼ねて会食を検討している
Output Slots: {{ "restaurant_address": null, "number_of_people": null, "reservation_datetime": null}}
END OF EXAMPLE

EXAMPLE
Conversation history:
Person #1: 新しいプロジェクトが開始した
AI: "Good luck!"
Person #1: プロジェクトメンバーとの親睦を兼ねて会食を検討している
AI: "プロジェクトメンバーは何人ですか"
Current Slots: {{"restaurant_address": null, "number_of_people": null, "reservation_datetime": null}}
Last line:
Person #1: 10人
Output Slots: {{"restaurant_address": null, "number_of_people": "10", "reservation_datetime": null}}
END OF EXAMPLE

EXAMPLE
Current datetime: 2023/04/10 11:20
Conversation history:
Person #1: 東京が良い
AI: いつ食事にいきますか
Current Slots: {{"restaurant_address": 東京, "number_of_people": null, "reservation_datetime": null}}
Last line:
Person #1: 明日の20:30
Output Slots: {{"restaurant_address": 東京, "number_of_people": null, "reservation_datetime": 2023/04/11 20:30}}
END OF EXAMPLE

Output Slots must be in json format!

Begin!
Current datetime: {current_datetime}
Conversation history (for reference only):
{history}
Current Slots:
{slots}
Last line of conversation (for extraction):
Human: {input}

Output Slots:"""
SLOT_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["history", "input", "slots", "current_datetime"],
    template=_DEFAULT_SLOT_EXTRACTION_TEMPLATE,
)


_DEFAULT_TEMPLATE = """
The following is a friendly conversation between a human and an AI.
The AI is talkative and provides lots of specific details from its context.
If the AI does not know the answer to a question, it truthfully says it does not know.

If restaurant_address is null with respect to the Current Slots value, ask a question about the restaurant_address.
However, do not use the word "restaurant_address" directly. Use expressions that are natural conversational expressions.

If number_of_people is null with respect to the Current Slots value, ask a question about the number_of_people.
However, do not use the word "number_of_people" directly. Use expressions that are natural conversational expressions.

If reservation_datetime is null with respect to the Current Slots value, ask a question about the reservation_datetime.
However, do not use the word "reservation_datetime" directly. Use expressions that are natural conversational expressions.

If current slots does not contain null, AI output should be output Finish[yes].
EXAMPLE
Conversation history:
Human: 東京が良い
AI: わかりました。いつ行きますか？
Current Slots: {{"restaurant_address": 東京, "number_of_people": 4, "reservation_datetime": 2023/04/11 20:30}}
Last line:
Human: 20:30
AI: Finish[yes]
END OF EXAMPLE

You don't have to output about Human's answer.
You don't have to output about Current Slots.

Begin!
Current conversation:
{history}
Current Slots:
{slots}
Human: {input}
AI:"""
CHAT_PROMPT = PromptTemplate(input_variables=["history", "input", "slots"], template=_DEFAULT_TEMPLATE)
