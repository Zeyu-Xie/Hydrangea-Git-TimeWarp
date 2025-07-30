import os
import pandas as pd
import subprocess


def git_commits(repo_path: str) -> dict:
    """
    Extracts commit information from a git repository and returns it as a pandas DataFrame.

    Args:
        repo_path (str): Path to the local git repository.

    Returns:
        pd.DataFrame: DataFrame containing commit hash, author name, author email, date, and commit message.

    Raises:
        ValueError: If the repository path does not exist, is not a directory, or is not a git repository.
        RuntimeError: If git log command fails or output cannot be parsed.
    """

    # == Exceptions ==

    # Repo path not exist
    if not os.path.exists(repo_path):
        raise ValueError(f"Repository path '{repo_path}' does not exist.")
    # Not a folder
    if os.path.isfile(repo_path):
        raise ValueError(f"Repository path '{repo_path}' is a file, not a directory.")
    # Not a repository
    repo_git_path = os.path.join(repo_path, ".git")
    if not os.path.exists(repo_git_path):
        raise ValueError(
            f"Directory '{repo_path}' is not a valid git repository (missing .git folder)."
        )

    # == Run Command and Parse ==

    # Run git log command
    try:
        output = subprocess.check_output(
            [
                "git",
                "log",
                "--date=iso8601-strict",
                "--pretty=format:%H%x1f%an%x1f%ae%x1f%ad%x1f%cn%x1f%ce%x1f%cd%x1f%s%x1e",
            ],
            cwd=repo_path,
            text=True,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to run git log: {e}")
    # Parse output
    try:
        rows = []
        for line in output.strip("\n\x1e").split("\x1e"):
            if not line.strip():
                continue
            fields = line.strip().split("\x1f")
            rows.append(
                {
                    "commit": fields[0],
                    "author_name": fields[1],
                    "author_email": fields[2],
                    "author_date": fields[3],
                    "committer_name": fields[4],
                    "committer_email": fields[5],
                    "committer_date": fields[6],
                    "message": fields[7],
                }
            )
        commits_pd = pd.DataFrame(
            rows,
            columns=[
                "commit",
                "author_name",
                "author_email",
                "author_date",
                "committer_name",
                "committer_email",
                "committer_date",
                "message",
            ],
        )
    except Exception as e:
        raise RuntimeError(f"Failed to parse git log output: {e}")

    # == Return ==

    # Return dict
    return commits_pd.to_dict(orient="records")


__all__ = ["git_commits"]
