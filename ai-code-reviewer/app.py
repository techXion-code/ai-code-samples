from fastapi import FastAPI, Request, BackgroundTasks
import github_service
import review_agent

app = FastAPI()


def process_pr(owner, repo, pr_number):
    print("Processing PR:", pr_number)

    diff = github_service.get_pr_files(owner, repo, pr_number)

    print("Diff fetched")

    review = review_agent.review_code(diff)

    print("AI review generated")

    github_service.post_pr_comment(owner, repo, pr_number, review)

    print("Comment posted")


@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):

    payload = await request.json()

    action = payload.get("action")

    if action not in ["opened", "synchronize"]:
        return {"status": "ignored"}

    repo = payload["repository"]["name"]
    owner = payload["repository"]["owner"]["login"]
    pr_number = payload["pull_request"]["number"]

    # Run AI review in background
    background_tasks.add_task(process_pr, owner, repo, pr_number)

    return {"status": "processing"}