// Arguments and configs
const FIELDS = [
    "commit",
    "author_name",
    "author_email",
    "author_date",
    "committer_name",
    "committer_email",
    "committer_date",
    "message"
];

// Commits data (dict)
let repo_name = "";
let repo_path = "";
let data = {};

// Functions for creating elements
function _createDiv(content, dataset = {}) {
    const _div = document.createElement("div");
    for (const key in dataset) {
        _input.dataset[key] = dataset[key];
    }
    _div.appendChild(content);
    return _div;
}
function _createInput(value, dataset = {}) {
    const _input = document.createElement("input");
    for (const key in dataset) {
        _input.dataset[key] = dataset[key];
    }
    _input.value = value;
    return _input;
}
function _createP(text, dataset = {}) {
    const _p = document.createElement("p");
    for (const key in dataset) {
        _input.dataset[key] = dataset[key];
    }
    _p.innerText = text;
    return _p
}
function _createTd(content, dataset = {}) {
    const _td = document.createElement("td");
    for (const key in dataset) {
        _input.dataset[key] = dataset[key];
    }
    _td.appendChild(content);
    return _td;
}

// Functions for edit commits
async function edit_commits(index, key, value) {

    // Old commit data
    const commit = data[index];

    // Contents filling
    document.querySelectorAll(".commit").forEach(item => item.innerText = commit["commit"]);
    document.querySelectorAll(".key").forEach(item => item.innerText = key);
    document.querySelectorAll(".old-value").forEach(item => item.innerText = commit[key]);
    document.querySelectorAll(".value").forEach(item => item.innerText = value);

    // Styles and events
    document.querySelector("#div-alert-frame").style.display = "block";
    document.querySelector("#button-alert-frame-continue").addEventListener("click", async () => {
        document.querySelector("#wait-message-alert-frame-continue").style.display = "block";
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
    })
    document.querySelector("#button-alert-frame-cancel").addEventListener("click", () => {
        console.log("Palsed");
        location.reload();
    })
}


// Run get commits at the beginning
(async () => {

    // Get data
    await fetch("/git_commits")
        .then(res => res.json())
        .then(res => {
            data = res;
        })
        .catch(err => {
            console.error(err);
        });
    await fetch("/repo_name")
        .then(res => res.text())
        .then(res => {
            repo_name = res;
        })
        .catch(err => {
            console.error(err);
        });
    await fetch("/repo_path")
        .then(res => res.text())
        .then(res => {
            repo_path = res;
        })
        .catch(err => {
            console.error(err);
        });

    // Render data
    document.querySelectorAll(".repo-name").forEach(item => item.innerText = repo_name);
    document.querySelectorAll(".repo-path").forEach(item => item.innerText = repo_path);

    const _tbody = document.querySelector("#table-git-commits tbody");
    data.forEach((commit, index) => {

        const _tr = document.createElement("tr");

        for (const field of FIELDS) {
            if (field === "commit") {
                const _p = _createP(text = commit.commit);
                _p.className = "font-mono";
                const _td = _createTd(content = _p);
                _tr.appendChild(_td);
            } else {
                const _input = _createInput(commit[field], { "index": index, "key": field });
                _input.addEventListener("change", async function () {
                    await edit_commits(this.dataset.index, this.dataset.key, this.value);
                })
                const _div = _createDiv(_input);
                const _td = _createTd(_div);
                _tr.appendChild(_td);
            }
        }

        _tbody.appendChild(_tr);
    });
})();