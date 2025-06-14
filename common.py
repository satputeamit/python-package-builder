import os
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)

from langchain_groq import ChatGroq


groqKey=os.getenv("GROQ_API_KEY")
model =os.getenv("MODEL")


code = ""

llm = ChatGroq(groq_api_key=groqKey, model=model)