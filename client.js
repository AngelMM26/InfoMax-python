document.getElementById("submit").onclick = function () {
    const query = document.getElementById("userInput").value;

    fetch(`http://127.0.0.1:5000/search?q=${query}`)
        .then(result => result.json())
        .then(data => {
            const start = document.getElementById("results");
            start.innerHTML = ""

            for (i = 0; i < data.results.length; i++) {
                let link = document.createElement("a");
                link.href = data.results[i];
                link.innerText = `${data.results[i]}`
                link.target = "_blank"
                start.appendChild(link);
            }
        });
}
