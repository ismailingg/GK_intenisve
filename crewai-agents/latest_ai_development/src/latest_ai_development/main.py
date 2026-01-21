#!/usr/bin/env python
import sys
from datetime import datetime
from latest_ai_development.crew import LatestAiDevelopmentCrew

def run():
    """
    Run the crew.
    """
    # 1. Prepare the dynamic data
    inputs = {
        'topic': 'AI Agent Frameworks',
        'current_year': str(datetime.now().year)
    }
    
    # 2. Kick off the process
    # This creates the Crew object and starts the task execution
    result = LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
    
    # 3. Handle the output
    print("\n\n########################")
    print("## Here is your Report ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    run()