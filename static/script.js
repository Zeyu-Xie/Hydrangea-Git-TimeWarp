// Commits data (dict)
let repo_name = "";
let repo_path = "";
let data = {};

// Functions for creating elements in tables
function _createDiv(content) {
    const _div = document.createElement("div");
    _div.appendChild(content);
    return _div;
}
function _createInput(index, key, value) {
    const _input = document.createElement("input");
    _input.dataset.index = index;
    _input.dataset.key = key;
    _input.value = value || "";
    _input.addEventListener("change", async function () {
        await edit_commits(this.dataset.index, this.dataset.key, this.value);
    })
    return _input;
}
function _createP(text) {
    const _p = document.createElement("p");
    _p.innerText = text;
    return _p
}
function _createTd(content) {
    const _td = document.createElement("td");
    _td.appendChild(content);
    return _td;
}

// Function for edit commits
async function edit_commits(index, key, value) {
    const commit = data[index];
    const notice = `You are chaning commit ${commit.commit}, key ${key}, value from ${commit[key]} to ${value}. Are you sure of this operation?`;
    if (confirm(notice)) {

        await fetch(`/git_filter_repo_commit_callback?commit=${commit.commit}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ [key]: value })
        })
            .then(res => res.json())
            .then(res => {
                console.log(res);
            })
            .catch(err => {
                console.error(err);
            });
        location.reload();
    } else {
        console.log("Palsed");
        location.reload();
    }
}


// Run get commits at the beginning
(async () => {

    // Get repo info
    await fetch("repo_name")
        .then(res => res.text())
        .then(res => {
            repo_name = res;
        })
        .catch(err => {
            console.error(err);
        });
    await fetch("repo_path")
        .then(res => res.text())
        .then(res => {
            repo_path = res;
        })
        .catch(err => {
            console.error(err);
        });

    // Get commits data
    await fetch("/git_commits")
        .then(res => res.json())
        .then(res => {
            data = res;
        })
        .catch(err => {
            console.error(err);
        });

    // Render repo info table
    document.querySelector("#p-repo-name").innerText = repo_name;
    document.querySelector("#p-repo-path").innerText = repo_path;

    // Render commits table
    const _tbody = document.querySelector("#table-git-commits tbody");
    data.forEach((commit, index) => {
        const _tr = document.createElement("tr");
        _tr.appendChild(_createTd(_createP(commit.commit)))
        _tr.appendChild(_createTd(_createDiv(_createInput(index, "author_name", commit.author_name))));
        _tr.appendChild(_createTd(_createDiv(_createInput(index, "author_email", commit.author_email))));
        _tr.appendChild(_createTd(_createDiv(_createInput(index, "author_date", commit.author_date))));
        _tr.appendChild(_createTd(_createDiv(_createInput(index, "committer_name", commit.committer_name))));
        _tr.appendChild(_createTd(_createDiv(_createInput(index, "committer_email", commit.committer_email))));
        _tr.appendChild(_createTd(_createDiv(_createInput(index, "committer_date", commit.committer_date))));
        _tr.appendChild(_createTd(_createDiv(_createInput(index, "message", commit.message))));
        _tbody.appendChild(_tr);
    });
})();