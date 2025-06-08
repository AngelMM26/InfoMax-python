document.getElementById("submit").onclick = function () {
    const query = document.getElementById("userInput").value;

    fetch(`http://127.0.0.1:5000/search?q=${query}`)
        .then(result => result.json())
        .then(data => {
            const start = document.getElementById("results");
            start.innerHTML = ""

            for (let page of data.results) {
                let link = document.createElement("a");
                link.href = page.url;
                link.innerText = page.title;
                link.target = "_blank"
                start.appendChild(link);
            }
        });
}
