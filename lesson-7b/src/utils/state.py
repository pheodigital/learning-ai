from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage
import operator

class MessagesState(TypedDict):
    """State with messages and LLM call count."""
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
