// Event listener for the "Scrape Data" button
document.getElementById("scrapeDataButton").addEventListener("click", function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const url = tabs[0].url;
        fetch('http://localhost:5000/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                alert('Error: ' + data.error); // Display the error in an alert
            } else {
                console.log("Scraping status:", data.status);

                // Filter predictions with a value of 1
                const filteredPredictions = data.predictions.filter(entry => entry.prediction === 1);

                // Display only the text for filtered predictions in a single alert
                const predictionsString = filteredPredictions.map(entry => `Text: ${entry.text}`).join('\n');

                alert('Scraping status: ' + data.status + '\n\nText for Predictions with value 1:\n' + predictionsString);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message); // Display the error in an alert
        });
    });
});

document.getElementById("summarizeButton").addEventListener("click", function () {
    // Redirect to the summarizing HTML site
    chrome.runtime.sendMessage({ action: "summarize" });
});
document.getElementById("policyCheckerButton").addEventListener("click", function () {
    // Inform the background script to open a new tab for the policy checker
    chrome.runtime.sendMessage({ action: "policyChecker" });
});
