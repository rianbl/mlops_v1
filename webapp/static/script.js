document.getElementById("prediction-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let features = [
        parseFloat(document.getElementById("sepal_length").value),
        parseFloat(document.getElementById("sepal_width").value),
        parseFloat(document.getElementById("petal_length").value),
        parseFloat(document.getElementById("petal_width").value)
    ];

    let response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "features": features })
    });

    let result = await response.json();
    document.getElementById("result").textContent = result.error || `Previsão: ${result.prediction}`;
});
