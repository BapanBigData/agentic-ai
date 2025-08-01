from autogen_ext.models.openai import OpenAIChatCompletionClient
from configs.constants import MODEL_OPENAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_model_client():
    openai_model_client = OpenAIChatCompletionClient(
        model=MODEL_OPENAI,
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=0.0
    )

    return openai_model_client
