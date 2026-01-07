# uv add google-genai
# add key to your env. GEMINI_API_KEY=[YOUR-KEY]

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

myfile = client.files.upload(file="sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=["Generate a transcript of the speech.", myfile]
)

print(response.text)
