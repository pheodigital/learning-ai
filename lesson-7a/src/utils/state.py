from typing_extensions import TypedDict
from typing import Literal

class AgentState(TypedDict):
  """Email agent state representation."""
  email: str
  category: Literal["urgent", "technical", "billing", "general"]
  template: str
  draft: str
  approved: bool
  customer_name: str