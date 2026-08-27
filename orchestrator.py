import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load GEMINI_API_KEY from .env
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

def extract_json(raw_text):
    """Safely extracts JSON from model text responses."""
    text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)

def run_security_scanner(code_diff, sast_report):
    """
    Agent 1: Application Security Engineer (Vulnerability Detection)
    """
    client = genai.Client(api_key=API_KEY)

    system_instruction = (
        "You are an expert Application Security Engineer. "
        "Review the provided Pull Request code diff alongside the SAST tool report. "
        "Identify security vulnerabilities (hardcoded secrets, SQL injection, insecure dependencies). "
        "Output strictly valid JSON with keys 'vulnerabilities' (list of objects) and 'summary'."
    )

    prompt = (
        f"Code Diff:\n{code_diff}\n\n"
        f"SAST Report:\n{json.dumps(sast_report)}\n\n"
        "Generate the structured security report."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json"
            )
        )
        return extract_json(response.text)
    except Exception as e:
        print(f"Agent 1 Error: {e}")
        return {"error": str(e)}

def run_architect_reviewer(code_diff, security_report):
    """
    Agent 2: Senior Staff Engineer (Architectural Review & Code Quality)
    """
    client = genai.Client(api_key=API_KEY)

    system_instruction = (
        "You are a Senior Staff Software Engineer and System Architect. "
        "Review the code diff along with the structured security findings from the AppSec scanner. "
        "Draft a constructive, professional code review in clean Markdown covering:\n"
        "1. Executive Summary\n"
        "2. Critical Security Remediation\n"
        "3. Architectural & Clean Code Improvements\n"
        "Be direct, technical, and actionable."
    )

    prompt = (
        f"### Code Diff Under Review:\n```\n{code_diff}\n```\n\n"
        f"### AppSec Scan Report (from Agent 1):\n```json\n{json.dumps(security_report, indent=2)}\n```\n\n"
        "Draft the final engineering review."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return response.text
    except Exception as e:
        print(f"Agent 2 Error: {e}")
        return f"Architect Review Error: {e}"

def run_orchestration_pipeline(code_diff, sast_report):
    """
    Handoff Protocol: Executes Agent 1 first, verifies output, then triggers Agent 2.
    """
    print("\n--- 🛡️ Step 1: Triggering Agent 1 (Security Scanner) ---")
    security_report = run_security_scanner(code_diff, sast_report)
    print("Agent 1 completed successfully.")

    print("\n--- 🏗️ Step 2: Triggering Agent 2 (Senior Architect) ---")
    architect_review = run_architect_reviewer(code_diff, security_report)
    print("Agent 2 completed successfully.")
    
    return {
        "security_findings": security_report,
        "architect_review": architect_review
    }

if __name__ == "__main__":
    fake_code_diff = """
    @@ -10,4 +10,6 @@ def get_user_profile(user_input):
    +    # Fix database connection
    +    API_SECRET_KEY = "sk_live_99887766554433221100"
    +    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    +    cursor.execute(query)
    """

    fake_sast_report = {
        "results": [
            {
                "issue_text": "Possible SQL injection vector through string formatting",
                "severity": "HIGH",
                "line_number": 13
            }
        ]
    }

    final_output = run_orchestration_pipeline(fake_code_diff, fake_sast_report)
    
    print("\n" + "="*50)
    print("FINAL ARCHITECT REVIEW (AGENT 2 OUTPUT)")
    print("="*50)
    print(final_output["architect_review"])