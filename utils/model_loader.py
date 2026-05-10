import os
from dotenv import load_dotenv
from typing import Any, Optional, Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from utils.config_loader import load_config

load_dotenv()


class ConfigLoader:
    def __init__(self):
        print("Initializing ConfigLoader...")
        self.config = load_config()
        print("ConfigLoader initialized.")

    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()  # Initialize the config loader

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return the LLM model based on the specified provider.
        """
        print("LLM loading...")
        print(f"Model provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading Groq LLM...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY is not set. Please set it in the environment or .env file.")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(model=model_name, api_key=groq_api_key)
            print("Groq LLM loaded successfully.")
        elif self.model_provider == "openai":
            print("Loading OpenAI LLM...")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set. Please set it in the environment or .env file.")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model=model_name, openai_api_key=openai_api_key)
            print("OpenAI LLM loaded successfully.")

        return llm
