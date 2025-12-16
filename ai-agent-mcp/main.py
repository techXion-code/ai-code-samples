# uv init
# uv add python-dotenv openai-agents gradio
# Requires NodeJS installed

import asyncio
import os
from dotenv import load_dotenv
import gradio as gr
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio

# add open-ai key in your .env file
load_dotenv(override=True)

INSTRUCTIONS = """
You browse the internet to accomplish your instructions.
You are highly capable at browsing_toggle independently to accomplish your task,
including accepting cookies and dismissing popups when needed.
Do not visit more than 2 websites. Keep results concise to save tokens.
"""

# 1. Create MCP browser server 
async def create_browser_mcp():
    
    PLAYWRIGHT_PARAMS = {
    "command": "npx",
    "args": ["@playwright/mcp@latest"]
    }
    return MCPServerStdio(
        params=PLAYWRIGHT_PARAMS,
        client_session_timeout_seconds=60
    )

# 2. Create the OpenAI agent with mcp
def create_agent(browser_mcp):
    return Agent(
        name="investigator",
        instructions=INSTRUCTIONS,
        model="gpt-4.1-mini",
        mcp_servers=[browser_mcp],
    )

# 4. Run Agent 
async def run_agent(query: str) -> str:
    async with await create_browser_mcp() as browser_mcp:
        agent = create_agent(browser_mcp)
        result = await Runner.run(agent, query)
        return result.final_output

# 5. Gradio click hanlder --> async call to #4
def gradio_handler(query: str) -> str:
    return asyncio.run(run_agent(query))

# ----------- Gradio UI ----------- 

with gr.Blocks(title="AI Web-Browsing Agent Demo") as demo:
    gr.Markdown("# 🤖 AI Web-Browsing Agent")
    query_input = gr.Textbox(
        label="Task",
        placeholder="Find a recipe for guacamole.",
        lines=2
    )
    output = gr.Textbox(
        label="Agent Output",
        lines=12
    )
    run_btn = gr.Button("Run Agent 🚀")
    run_btn.click(
        fn=gradio_handler,
        inputs=query_input,
        outputs=output
    )
    
demo.launch()