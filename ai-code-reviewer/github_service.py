import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_pr_files(owner, repo, pr_number):
   url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

   response = requests.get(url, headers=headers)

   print("Status:", response.status_code)
   print("Response:", response.text)

   files = response.json()
   diff_text = ""
   if not isinstance(files, list):
        raise Exception(f"Unexpected GitHub response: {files}")

   for file in files:
        patch = file.get("patch")

        if patch:
            diff_text += f"\nFile: {file['filename']}\n"
            diff_text += patch + "\n"
   print("diff_text:", diff_text)
   return diff_text


def post_pr_comment(owner, repo, pr_number, comment):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"

    payload = {"body": comment}
    response = requests.post(url, json=payload, headers=headers)
    print("POST COMMENT STATUS:", response.status_code)
