from agents import Agent, Runner
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

agent = Agent(name="A1", model="gpt-4")

async def chat(message, history):
    resp = await Runner.run(agent, message)
    return resp.final_output

demo = gr.ChatInterface(fn=chat, title="OpenAI powered chatbot")

if __name__=='__main__':
    demo.launch()