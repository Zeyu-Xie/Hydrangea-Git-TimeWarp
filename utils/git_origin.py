import os
import subprocess


def git_origin(repo_path: str):
    """
    Get the list of git remotes for the given repository path.

    Args:
        repo_path (str): Path to the local git repository.

    Returns:
        List[str]: List of git remote descriptions as returned by 'git remote -v'.

    Raises:
        ValueError: If the path does not exist, is not a directory, or is not a git repository.
        RuntimeError: If the git command fails.
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

    # Run git remote command
    try:
        output = subprocess.check_output(
            ["git", "remote", "-v"],
            cwd=repo_path,
            text=True,
        )
        output_list = output.splitlines()
    except Exception as e:
        raise RuntimeError(f"Failed to run git log: {e}")

    # == Return ==

    # Return list
    return output_list


__all__ = ["git_origin"]
