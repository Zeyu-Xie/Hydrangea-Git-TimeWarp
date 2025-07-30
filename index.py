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
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

static_files = StaticFiles(directory=STATIC_DIR)
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# == Routers ==

# Create app
app = FastAPI()
app.mount("/static", static_files, name="static")


# Routers - Resources
@app.get("/", response_class=HTMLResponse)
def request_(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/style.css", response_class=StaticFiles)

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


# Routers - Check connections
@app.get("/check_connections")
def request_check_connections():
    return Response(content="OK", media_type="text/plain", status_code=200)


# == Run ==

# Run app
if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
