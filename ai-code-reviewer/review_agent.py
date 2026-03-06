import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def review_code(diff):

    prompt = f"""
You are a senior software engineer reviewing a pull request.

Analyze this code diff and identify:

- Bugs
- Performance problems
- Security issues
- Code quality improvements

Provide a structured review.

Code Diff:
{diff}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content