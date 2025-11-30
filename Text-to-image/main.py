# install huggingface_hub, dotenv, gradio
import gradio as gr
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# place your HF_TOKEN = {HF_TOKEN=your_huggingface_token_here}
# in .env file on root of your app.
load_dotenv()

# 1.Load model
model_id = "stabilityai/stable-diffusion-xl-base-1.0"
client = InferenceClient(model_id, token=os.getenv("HF_TOKEN"))

# 2.Generate Image
def generate_image(prompt):
    return client.text_to_image(prompt)

# 3.Create UI using gradio
demo = gr.Interface(
    fn=generate_image,
    inputs=gr.Textbox(label="Enter your image prompt"),
    outputs="image",
    title="AI Image Generator",
    description="Type what you want to see!"
)

# 4.launch app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 8080)))