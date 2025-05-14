import fitz  # PyMuPDF
import re
import requests

def extract_text_and_links(pdf_path):
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    links = [link["uri"] for page in doc for link in page.get_links() if "uri" in link]
    return text, links

def extract_github_username(url):
    match = re.search(r"github\\.com/([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None

def fetch_repos(username, token):
    r = requests.get(
        f"https://api.github.com/users/{username}/repos",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    )
    return r.json() if r.status_code == 200 else []

def fetch_readme(username, repo, token):
    url = f"https://api.github.com/repos/{username}/{repo}/readme"
    r = requests.get(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    })
    return r.text if r.status_code == 200 else ""

def fetch_languages(username, repo, token):
    url = f"https://api.github.com/repos/{username}/{repo}/languages"
    r = requests.get(url, headers={"Authorization": f"token {token}"})
    return r.json() if r.status_code == 200 else {}
