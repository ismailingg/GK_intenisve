from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import re

client = OpenAI(
    api_key = os.getenv("GOOGLE_API_KEY"),
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/")

class chatbot:
    def __init__(self,system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role":"system","content":system})

    def run_llm(self):
        response = client.chat.completions.create(
            model="gemini-2.5-computer-use-preview-10-2025",
            messages=self.messages
        )
        return response.choices[0].message.content

    def __call__(self,message):
        self.messages.append({"role":"user","content":message})
        result = self.run_llm()
        self.messages.append({"role":"assistant","content":result})
        return result

# bot = chatbot(system="You are a helpful assistant")
# print(bot("What is the capital of France?"))


