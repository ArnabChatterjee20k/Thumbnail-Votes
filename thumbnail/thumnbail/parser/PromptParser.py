from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import List

class PromptParser(BaseModel):
    prompts:List[str] = Field(title="prompts",description="List of three words prompt generated", max_items=4)

prompt_parser = PydanticOutputParser(pydantic_object=PromptParser)
