import os
import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from dotenv import load_dotenv

# Import skills and multi-agent orchestrator
from skills import fetch_pr_diff, run_security_scan, post_pr_comment
from orchestrator import run_orchestration_pipeline

load_dotenv()

app = FastAPI(title="DevSecOps PR Webhook")

def process_pull_request(owner: str, repo: str, pr_number: int):
    """
    Background worker that runs the DevSecOps agent pipeline and posts the review.
    """
    print(f"\n🚀 [WORKER] Starting automated scan on {owner}/{repo} PR #{pr_number}...")
    
    # 1. Fetch code diff from PR
    token = os.environ.get("GITHUB_TOKEN")
    code_diff = fetch_pr_diff(owner, repo, pr_number, github_token=token)
    if not code_diff:
        print("❌ Could not retrieve PR diff.")
        return

    # 2. Run local SAST scan
    sast_report = run_security_scan(".")

    # 3. Run Gemini & Multi-Agent Orchestration
    results = run_orchestration_pipeline(code_diff, sast_report)
    architect_review = results.get("architect_review")

    # 4. Post the review back to the GitHub PR thread
    if architect_review:
        post_pr_comment(owner, repo, pr_number, architect_review, github_token=token)
        print(f"✅ Successfully completed pipeline and commented on PR #{pr_number}")

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        payload = await request.json()
        
        # Intercept pull_request 'opened' or 'reopened' events
        if "pull_request" in payload:
            action = payload.get("action")
            if action in ["opened", "reopened", "synchronize"]:
                pr_number = payload["pull_request"]["number"]
                repo_full_name = payload["repository"]["full_name"]
                owner, repo = repo_full_name.split("/")

                # Run heavy analysis as a background task to respond to GitHub immediately
                background_tasks.add_task(process_pull_request, owner, repo, pr_number)
                return {"status": "triggered", "message": f"Agent scan queued for PR #{pr_number}"}

        return {"status": "ignored", "message": "Event ignored"}
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)