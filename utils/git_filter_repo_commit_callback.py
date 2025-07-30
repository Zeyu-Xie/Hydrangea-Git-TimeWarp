import datetime
import os
import subprocess


def _iso_to_git_raw(iso_str):
    iso_str = iso_str.strip()
    dt = datetime.datetime.fromisoformat(iso_str)
    ts = int(dt.timestamp())
    offset = dt.strftime("%z") if dt.strftime("%z") else "+0000"
    return f"{ts} {offset}"


def git_filter_repo_commit_callback(repo_path: str, commit_id: str, data: dict):
    """
    Update commit metadata in a git repository using git-filter-repo.

    Args:
        repo_path (str): Path to the git repository.
        commit_id (str): SHA-1 hash of the commit to update.
        data (dict): Dictionary of commit metadata to update.

    Raises:
        ValueError: If the repository path, commit ID, or data are invalid.
    """

    # == Init ==

    # Commit ID in lower case
    commit_id = commit_id.lower()
    # Available keys
    keys = [
        "author_name",
        "author_email",
        "author_date",
        "committer_name",
        "committer_emaik",
        "committer_date",
        "message",
    ]
    data = {k: data[k] for k in keys if k in data}

    # == Exceptions (Path) ==

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

    # == Exceptions (Commit ID) ==

    # Length
    if len(commit_id) != 40:
        raise ValueError(
            f"Commit ID '{commit_id}' is not a valid 40-character SHA-1 hash."
        )
    # Illegal characters
    for i in range(40):
        if commit_id[i] not in "0123456789abcdef":
            raise ValueError(
                f"Commit ID '{commit_id}' contains invalid character '{commit_id[i]}' at position {i}."
            )

    # == Exceptions (data) ==

    # Data type
    for key, val in data.items():
        if not isinstance(val, str):
            raise ValueError(f"Value for key '{key}' must be a string.")

    # == Run git filter-repo command

    # Special case
    if len(data) <= 0:
        print("No data provided to update commit.")
        return
    # Construct callback string
    callback = f'if commit.original_id == b"{commit_id}":'
    for key, val in data.items():
        _val = val
        if key == "author_date" or key == "committer_date":
            _val = _iso_to_git_raw(val)
        callback += "\n"
        callback += f"    commit.{key} = b{repr(_val)}"
    # Run git filter-repo command
    output = subprocess.check_output(
        ["git", "filter-repo", "--force", "--commit-callback", callback],
        text=True,
        cwd=repo_path,
    )
    print(output)


__all__ = ["git_filter_repo_commit_callback"]
