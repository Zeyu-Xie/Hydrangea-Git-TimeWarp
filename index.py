# Import libraries
import argparse
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn

# Import own libraries
from utils import git_commits, git_filter_repo_commit_callback, git_origin

# == Parse Arguments ==

# Parse arguments
parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument("repo_path", type=str, help="Repo's path.")
parser.add_argument("--host", type=str, default="0.0.0.0", help="Local server's host.")
parser.add_argument("--port", type=int, default=5400, help="Local server's port.")
args = parser.parse_args()

HOST = args.host
PORT = args.port
REPO_PATH = args.repo_path

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
HTML_PATH = os.path.join(STATIC_DIR, "index.html")

static_files = StaticFiles(directory=STATIC_DIR)

# == Routers ==

# Create app
app = FastAPI()
app.mount("/static", static_files, name="static")


# Routers - Check connections
@app.get("/check_connections")
def request_check_connections():
    return Response(content="OK", media_type="text/plain", status_code=200)


# Routers - Functions
@app.get("/git_commits", response_class=JSONResponse)
def request_git_commits():
    content = git_commits(repo_path=REPO_PATH)
    return JSONResponse(content=content)


@app.post("/git_filter_repo_commit_callback", response_class=JSONResponse)
async def request_git_filter_repo_commit_callback(request: Request):
    try:
        commit = request.query_params.get("commit")
        body = await request.json()
        git_filter_repo_commit_callback(
            repo_path=REPO_PATH, commit_id=commit, data=body
        )
        return JSONResponse(content={"status": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "detail": str(e)}, status_code=500
        )


# Routers - Info
@app.get("/repo_name")
def request_repo_name():
    return Response(
        content=os.path.basename(REPO_PATH), media_type="text/plain", status_code=200
    )


@app.get("/repo_path")
def request_repo_path():
    return Response(content=REPO_PATH, media_type="text/plain", status_code=200)


# Routers - Page
@app.get("/", response_class=HTMLResponse)
async def home():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content


# == Run ==

# Run app
if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
