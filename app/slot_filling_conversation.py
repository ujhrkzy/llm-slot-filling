import json
from typing import Any, Dict, List

from langchain import LLMChain
from langchain.chains import ConversationChain
from langchain.chains.conversation.prompt import PROMPT
from langchain.prompts.base import BasePromptTemplate
from langchain.schema import BaseLanguageModel, messages_to_dict
from pydantic import Extra, root_validator

from app.prompt import CHAT_PROMPT
from app.slot_memory import SlotMemory


class SlotFillingConversationChain(LLMChain):
    memory: SlotMemory
    """Default memory store."""
    prompt: BasePromptTemplate = PROMPT
    """Default conversation prompt to use."""

    input_key: str = "input"  #: :meta private:
    output_key: str = "response"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Use this since so some prompt vars come from history."""
        return [self.input_key]

    @classmethod
    def create(cls, llm: BaseLanguageModel, memory: SlotMemory) -> ConversationChain:
        return ConversationChain(llm=llm, memory=memory, prompt=CHAT_PROMPT)

    @root_validator()
    def validate_prompt_input_variables(cls, values: Dict) -> Dict:
        """Validate that prompt input variables are consistent."""
        memory_keys = values["memory"].memory_variables
        input_key = values["input_key"]
        if input_key in memory_keys:
            raise ValueError(
                f"The input key {input_key} was also found in the memory keys "
                f"({memory_keys}) - please provide keys that don't overlap."
            )
        prompt_variables = values["prompt"].input_variables
        expected_keys = memory_keys + [input_key]
        if set(expected_keys) != set(prompt_variables):
            raise ValueError(
                "Got unexpected prompt input variables. The prompt expects "
                f"{prompt_variables}, but got {memory_keys} as inputs from "
                f"memory, and {input_key} as the normal input key."
            )
        return values

    def log(self):
        history = self.memory.chat_memory
        messages = json.dumps(messages_to_dict(history.messages), indent=2, ensure_ascii=False)
        print(f"memory: {messages}")

    def predict_demo(self, **kwargs: Any) -> str:
        """Format prompt with kwargs and pass to LLM.

        Args:
            **kwargs: Keys to pass to prompt template.

        Returns:
            Completion from LLM.

        Example:
            .. code-block:: python

                completion = llm.predict(adjective="funny")
        """
        response = self(kwargs)
        output = response[self.output_key]
        slots = response[self.memory.slot_key]
        return f"{output}\n【Slot】: {slots}"
