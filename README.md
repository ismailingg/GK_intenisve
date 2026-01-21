# AI Agents: Implementation Patterns & Explorations

A collection of AI agent implementations exploring different architectures and patterns for autonomous task execution. This repository documents practical implementations of agent frameworks using language models with tool-use capabilities.

## Overview

This project explores agent architectures through hands-on implementation, focusing on:

- **ReAct (Reasoning + Acting) patterns** with iterative thought-action-observation loops
- **Function calling** with structured tool definitions and execution
- **Multi-turn agent workflows** with state management and tool orchestration
- **Browser automation** agents with real-world web interaction capabilities

## Agent Implementations

### Single-Agent (ReAct Pattern)

ReAct-style agent using structured text-based action parsing with a Thought → Action → Observation loop. Integrates external tools (Wikipedia, ArXiv, calculations) through custom action parsing.

**Location:** `single-agent/`

### Browser-Use Agent (Function Calling)

Browser automation agent built on OpenAI-compatible function calling APIs. Uses Playwright for headless browser control with structured tool definitions and async execution.

**Location:** `browser-use-agent/`

### CrewAI Agents

Multi-agent crew implementation using CrewAI framework for collaborative task execution. Agents work together to research and analyze latest AI developments with configurable roles and tasks.

**Location:** `crewai-agents/latest_ai_development/`

**How to run**

1. `cd crewai-agents/latest_ai_development`
2. Install dependencies: `pip install -e .`
3. Kick off the crew: `latest_ai_development` (or `crewai run`)
4. Report output is written to `output/report.md`

Configuration lives in `src/latest_ai_development/config/`:
- `agents.yaml` defines the researcher and reporting analyst
- `tasks.yaml` defines the research and reporting tasks (uses `topic` and `current_year` inputs)

*Expect more agent implementations coming soon.*

### Google-ADK Agents
*coming soon.*

## Architecture

implementations follow core agent design principles:

1. **LLM Orchestration**: Language model generates reasoning steps and action selections
2. **Tool Execution**: External tools (APIs, calculations, browser automation) execute actions
3. **State Management**: Conversation history and tool results inform subsequent reasoning
4. **Iterative Refinement**: Agents loop until task completion or max iterations

## Tech Stack

- **Language Models**: Google Gemini (via OpenAI-compatible API)
- **Browser Automation**: Playwright (async)
- **HTTP Requests**: httpx
- **Data Processing**: Standard library (json, re, asyncio)

## Notes

- This is a learning project exploring agent design patterns and implementations
- Code structure prioritizes clarity and educational value over production optimization
- Contributions, suggestions, and discussions are welcome

## License

[Add your license here]
