#from google.adk.agents import Agent
#from google import genai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
#client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
from openai import OpenAI # Use the OpenAI library
import os
import httpx
import json
import xml.etree.ElementTree as ET
import re
# Point the OpenAI client to Google's servers
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
class chatbot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role":"system","content":system})

    def __call__(self,message):
        self.messages.append({"role":"user","content":message})
        result = self.run_llm()
        self.messages.append({"role":"assistant","content":result})
        return result

    def run_llm(self):
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
           messages=self.messages
        )
        return response.choices[0].message.content

#bot = chatbot(system="You are an assistant which is very grumpy and never greets and is rude.")
#response = bot("say something nice?")
#print(response)

def wikipedia_search(query):
    url="https://en.wikipedia.org/w/api.php"
    params = {
        "action" : "query",
        "list" : "search",
        "srsearch" : query,
        "format" : "json"
    }
    headers = {"User-Agent": "MyTestAgent/1.0 (your-email@example.com)"}
    response = httpx.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["query"]["search"][0]["snippet"]

#print(wikipedia_search("Python"))
def calculate(expression):
    response = eval(expression)
    return response

#print(calculate("1+1"))
def research_papers(q):
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{q}",
        "start": 0,
        "max_results": 1
    }
    response = httpx.get(url, params=params, timeout=10.0)
    response.raise_for_status()
    
    # Debug: Check if response is empty
    if not response.text:
        return "Empty response from ArXiv API"
    
    # Debug: Print first 500 chars to see what we're getting
    # print(f"Response (first 500 chars): {response.text[:500]}")
    
    try:
        # ArXiv returns XML, so we parse it to get the summary
        root = ET.fromstring(response.text)
        
        # ArXiv XML uses Atom namespace: http://www.w3.org/2005/Atom
        # We need to use the correct namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        # Find the first entry
        entry = root.find('atom:entry', ns)
        if entry is not None:
            summary_elem = entry.find('atom:summary', ns)
            if summary_elem is not None and summary_elem.text:
                return summary_elem.text.strip()
        
        return "No academic papers found."
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        return f"Error parsing XML response: {e}"

#print(research_papers("AI"))
action_re = re.compile(r'^Action:\s*(\w+):\s*(.*)$')
action_dict = {
    "wikipedia_search": wikipedia_search,
    "calculate": calculate,
    "research_papers": research_papers
}
deet_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia_search:
e.g. wikipedia_search:
Returns a summary from searching Wikipedia

arxiv_search:
e.g. arxiv_search:
Returns a summary of research papers

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()
class agent:
    def __init__(self,system_prompt=[],max_turns=1,known_actions=None):
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.bot = chatbot(system_prompt)
        self.known_actions = known_actions or []

    def run(self,message):
        i = 0
        next_prompt=message
        while i < self.max_turns:
            i += 1
            result = self.bot(next_prompt)
            print(result)
            actions = [
                action_re.match(line)
                for line in result.split('\n')
                if action_re.match(line)
            ]
            if actions:
                action,action_input = actions[0].groups()
                if action not in self.known_actions:
                    raise Exception ("unknown action :{}:{}".format(action,action_input))

                print(f"running action : {action} with the input : {action_input}")

                observations = self.known_actions[action](action_input)
                print(f"\nobservations: {observations}")
                
                next_prompt = f"observations: {observations}"
            else:
                print("\n Tasks complete\n -----------------------------------------")

first_agent = agent(deet_prompt,3,action_dict) 
first_agent.run("explain the lightrag model")