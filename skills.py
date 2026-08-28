import os
import subprocess
import json
import sqlite3
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
import requests
import os

def fetch_pr_diff(owner, repo, pr_number, github_token=None):
    """
    Fetches the raw code diff of a pull request using the GitHub REST API.
    """
    # GitHub REST API endpoint for fetching a specific pull request
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    # We must specify the 'diff' media type in the Accept header 
    # to get the actual code changes instead of JSON metadata.
    headers = {
        "Accept": "application/vnd.github.v3.diff"
    }
    
    # If a GitHub Personal Access Token is provided, add it to headers to prevent rate-limiting
    if github_token:
        headers["Authorization"] = f"token {github_token}"
        
    try:
        response = requests.get(url, headers=headers)
        
        # Check if the API request was successful
        if response.status_code == 200:
            print(f"Successfully fetched diff for PR #{pr_number}")
            return response.text
        else:
            print(f"Failed to fetch diff. Status Code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Quick Test Block ---
if __name__ == "__main__":
    # Feel free to test this on any public repo and PR once we have one!
    # diff_output = fetch_pr_diff("arnavk-helios", "devsecops-code-review-automator", 1)
    # print(diff_output)
    pass
import subprocess
import json

def run_security_scan(target_path="."):
    """
    Executes the SAST bash script and returns the structured scan results.
    """
    try:
        # Run the bash script using Python subprocess
        result = subprocess.run(
            ["./run_sast.sh", target_path],
            capture_output=True,
            text=True
        )
        
        # Parse output as JSON if Bandit produced results
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {"metrics": {}, "results": []}
        
    except Exception as e:
        print(f"Error running security scan: {e}")
        return {"error": str(e)}
import sqlite3

def query_pr_history(limit=5):
    """
    Queries the local SQLite database for recent pull request scans 
    to provide historical context to the AI agents.
    """
    db_path = "audit_logs.db"
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Formulate the SQL query to fetch the latest scans
        query = "SELECT pr_number, agent_decisions, security_flags FROM scans ORDER BY id DESC LIMIT ?"
        cursor.execute(query, (limit,))
        
        # Fetch the results
        rows = cursor.fetchall()
        
        # Format the output into a readable list of dictionaries
        history = []
        for row in rows:
            history.append({
                "pr_number": row[0],
                "decisions": row[1],
                "flags": row[2]
            })
            
        conn.close()
        return history
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
import os
import requests

def post_pr_comment(owner, repo, pr_number, comment_body, github_token=None):
    """
    Posts a Markdown comment directly to a GitHub Pull Request discussion thread.
    """
    token = github_token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN is required to post comments.")
        return False

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": comment_body}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            print(f"Successfully posted review comment to PR #{pr_number}")
            return True
        else:
            print(f"Failed to post comment. HTTP {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"Error posting comment to GitHub: {e}")
        return False
import os
import requests

def send_discord_alert(pr_number, issue_count=0):
    """
    Broadcasts a scan summary alert directly to a Discord channel via Webhook.
    """
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL is not set.")
        return False

    # Format the message based on the scan results
    if issue_count > 0:
        message = f"🚨 **PR #{pr_number} scanned:** {issue_count} security issues found. Review required."
    else:
        message = f"✅ **PR #{pr_number} scanned:** 0 issues found. Code is clean!"

    payload = {"content": message}

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(f"Successfully sent Discord alert for PR #{pr_number}")
            return True
        else:
            print(f"Failed to send Discord alert. HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error posting to Discord: {e}")
        return False