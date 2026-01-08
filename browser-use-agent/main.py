from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import re
from playwright.async_api import async_playwright
from io import BytesIO
from PIL import Image as PILImage
from IPython.display import display
import asyncio

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
            model="gemini-2.5-flash",
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

async def take_screenshot(url):
    p = await async_playwright().start()
    browser = None
    try:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        screenshot = await page.screenshot()
        img = PILImage.open(BytesIO(screenshot))
        display(img)
    finally:
        # Clean up resources in reverse order
        if browser:
            await browser.close()
        await p.stop()

#asyncio.run(take_screenshot("https://www.google.com"))

tools = [{
    "type": "function",
    "function": {
        "name": "load_page",
        "description": "Go to a webpage.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string"
                }
            },
            "required": [
                "url"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}, {
    "type": "function",
    "function": {
        "name": "click_element",
        "description": "Click on an element by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "element_id": {
                    "type": "number"
                }
            },
            "required": [
                "element_id"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]


