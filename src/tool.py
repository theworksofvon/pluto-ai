from pydantic import BaseModel
from abc import ABC, abstractmethod

class Tool(BaseModel, ABC):


    def construct_prompt():
        """
        RAG method to intercept prompt and place relevent knowledge inside the context window
        """
        pass

    @abstractmethod
    def action():
        NotImplementedError()