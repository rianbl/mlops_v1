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

// Busca informações do modelo ao carregar a página
async function fetchModelInfo() {
    let response = await fetch("/model-info");
    let info = await response.json();
    document.getElementById("model-info").textContent = 
        `Model: ${info.name} - Version: ${info.version}`;
}

window.onload = fetchModelInfo;
