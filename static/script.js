let data = {};

function _createTd(content) {
    const _td = document.createElement("td");
    _td.appendChild(content);
    return _td;
}

function _createInput(index, commit, key, value, type) {
    const _input = document.createElement("input");
    _input.dataset.index = index;
    _input.dataset.commit = commit;
    _input.dataset.key = key;
    _input.type = type;
    _input.value = value || "";
    _input.addEventListener("change", async function () {
        const index = this.dataset.index;
        const commit = this.dataset.commit;
        const key = this.dataset.key;
        const value = this.value;
        await edit_commits(index, key, value);
    })
    return _input;
}

function _createP(content) {
    const _p = document.createElement("p");
    _p.innerText = content;
    return _p
}

async function get_commits() {
    await fetch("/git_commits")
        .then(res => res.json())
        .then(res => {

            data = res;

            const _tbody = document.querySelector("#table-git-commits-table tbody");
            res.forEach((commit, index) => {
                const tr = document.createElement("tr");
                tr.appendChild(_createTd(_createP(commit.commit)))
                tr.appendChild(_createTd(_createInput(index, commit.commit, "author_name", commit.author_name, "text")));
                tr.appendChild(_createTd(_createInput(index, commit.commit, "author_email", commit.author_email, "text")));
                tr.appendChild(_createTd(_createInput(index, commit.commit, "author_date", commit.author_date, "text")));
                tr.appendChild(_createTd(_createInput(index, commit.commit, "committer_name", commit.committer_name, "text")));
                tr.appendChild(_createTd(_createInput(index, commit.commit, "committer_email", commit.committer_email, "text")));
                tr.appendChild(_createTd(_createInput(index, commit.commit, "committer_date", commit.committer_date, "text")));
                tr.appendChild(_createTd(_createInput(index, commit.commit, "message", commit.message, "text")));
                _tbody.appendChild(tr);
            });
        })
        .catch(err => {
            console.error(err);
        });
}

async function edit_commits(index, key, value) {
    const commit = data[index];
    const notice = `
You are chaning commit ${commit.commit}, key ${key}, value from ${commit[key]} to ${value}.
    `;
    if (confirm(notice)) {

        console.log(key, value);

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
    }
}

(async () => {
    get_commits();
})();