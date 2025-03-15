document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("calc-form");
    const input = document.getElementById("expression");
    const resultDiv = document.getElementById("result");
    const historyList = document.getElementById("history");
    const solveForm = document.getElementById("solve-form");
    const equationInput = document.getElementById("equation");
    const solveResult = document.getElementById("solve-result");
    const plotForm = document.getElementById("plot-form");
    const plotInput = document.getElementById("plot-function");
    const plotResult = document.getElementById("plot-result");
    const plotImage = document.getElementById("plot-image");
    const themeToggle = document.getElementById("theme-toggle");

    // ✅ Fix: Ensure math calculation section works correctly
    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        let expression = input.value.trim();

        if (!expression) {
            resultDiv.innerHTML = "⚠️ Please enter an expression!";
            return;
        }

        try {
            let response = await fetch("http://127.0.0.1:5000/calculate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ expression }),
            });

            let data = await response.json();
            if (response.ok) {
                resultDiv.innerHTML = `✅ <strong>Result:</strong> ${data.result}`;
                addToHistory(expression, data.result);
            } else {
                resultDiv.innerHTML = `❌ <strong>Error:</strong> ${data.error}`;
            }
        } catch {
            resultDiv.innerHTML = "❌ Error connecting to the server!";
        }
    });

    // ✅ Fix: Ensure equation solver section works correctly
    solveForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        let equation = equationInput.value.trim();

        if (!equation) {
            solveResult.innerHTML = "⚠️ Please enter an equation!";
            return;
        }

        try {
            let response = await fetch("http://127.0.0.1:5000/solve", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ equation }),
            });

            let data = await response.json();
            if (response.ok) {
                solveResult.innerHTML = `✅ <strong>Solution:</strong> ${data.solution.join(", ")}`;
            } else {
                solveResult.innerHTML = `❌ <strong>Error:</strong> ${data.error}`;
            }
        } catch {
            solveResult.innerHTML = "❌ Error connecting to the server!";
        }
    });

    // ✅ Fix: Ensure graph plotting works correctly
    plotForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        let functionStr = plotInput.value.trim();

        if (!functionStr) {
            plotResult.innerHTML = "⚠️ Please enter a function!";
            return;
        }

        try {
            let response = await fetch("http://127.0.0.1:5000/plot", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ function: functionStr }),
            });

            if (response.ok) {
                // ✅ Fix: Fetch the image from /get_plot instead of /plot
                plotImage.src = `http://127.0.0.1:5000/get_plot?timestamp=${new Date().getTime()}`;
                plotImage.style.display = "block";
                plotResult.innerHTML = `✅ <strong>Graph generated for:</strong> ${functionStr}`;
            } else {
                let data = await response.json();
                plotResult.innerHTML = `❌ <strong>Error:</strong> ${data.error}`;
                plotImage.style.display = "none";
            }
        } catch {
            plotResult.innerHTML = "❌ Error connecting to the server!";
        }
    });

    // ✅ Function to add calculation history dynamically
    function addToHistory(expression, result) {
        let li = document.createElement("li");
        li.innerHTML = `<strong>${expression} = ${result}</strong>`;
        historyList.prepend(li);
    }

    // ✅ Fix: Ensure dark mode toggles correctly
    themeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");

        themeToggle.textContent = document.body.classList.contains("dark-mode") ? "☀️ Light Mode" : "🌙 Dark Mode";
    });

    // ✅ Fix: Ensure dark mode is remembered after refresh
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
        themeToggle.textContent = "☀️ Light Mode";
    }
});
