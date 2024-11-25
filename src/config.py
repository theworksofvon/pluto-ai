import os
from pydantic import BaseModel

class Config(BaseModel):



    OLLAMA_API_URL: str = os.environ.get("OLLAMA_API_URL")
    OLLAMA_MODEL_NAME: str = os.environ.get("OLLAMA_MODEL_NAME")



config = Config()