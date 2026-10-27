const inputElement = document.getElementById("userInput");
const aiToggle = document.getElementById("aiMode");

inputElement.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && inputElement.value !== "") {
        const params = new URLSearchParams({
            q: inputElement.value,
            aiEnabled: String(aiToggle.checked)
        });
        window.location.href = `serp.html?${params}`;
    }
});
