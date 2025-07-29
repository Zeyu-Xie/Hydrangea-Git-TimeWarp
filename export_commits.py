import pandas as pd
import subprocess
import sys

# Arguments
REPO_PATH = sys.argv[1]
EXPORT_PATH = sys.argv[2]

# Get output
output = subprocess.check_output(
    ["git", "log", "--pretty=format:%H%x1f%an%x1f%ae%x1f%ad%x1f%s%x1e"],
    cwd=REPO_PATH,
    text=True,
)

# Parse output
rows = []
for line in output.strip("\n\x1e").split("\x1e"):
    if not line.strip():
        continue
    fields = line.strip().split("\x1f")
    rows.append(
        {
            "Commit": fields[0],
            "Author": fields[1],
            "Email": fields[2],
            "Date": fields[3],
            "Message": fields[4],
        }
    )
commits = pd.DataFrame(rows, columns=["Commit", "Author", "Email", "Date", "Message"])

# Save output
commits.to_csv(EXPORT_PATH)
