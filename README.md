# Hydrangea-Git-TimeWarp

A macOS web-based tool to change Git commit records.

## Usage

```bash
python index.py [-h] [--host HOST] [--port PORT] repo_path
```

### Positional Arguments

| Argument    | Description  |
| ----------- | ------------ |
| `repo_path` | Repo's path. |

### Options

| Option         | Description                 |
| -------------- | --------------------------- |
| `-h`, `--help` | Show help message and exit. |
| `--host HOST`  | Local server's host.        |
| `--port PORT`  | Local server's port.        |


## System Dependencies

1. [git-filter-repo](https://github.com/newren/git-filter-repo): Quickly rewrite git repository history (filter-branch replacement)