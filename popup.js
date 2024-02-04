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

document.getElementById('extraChargeChecker').addEventListener('click',function(){
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const url = tabs[0].url;
        fetch('http://localhost:5000/extra_charge', {
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
                //console.log("Scraping status:", data.status);
                alert('Scraping status: ' + data.status);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error during js: ' + error.message); // Display the error in an alert
        });
    });
})

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchButton').addEventListener('click', function () {
        // Get the URL of the current tab
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            var currentTab = tabs[0];
            var currentUrl = currentTab.url;

            // Make an AJAX request to the server
            var xhr = new XMLHttpRequest();
            xhr.open('GET', 'http://localhost:5000/search?url=' + encodeURIComponent(currentUrl), true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Handle successful response
                        console.log(xhr.responseText);
                        // Process the response, maybe update UI accordingly
                    } else {
                        // Handle error response
                        console.error('Request failed:', xhr.status);
                    }
                }
            };
            xhr.send();
        });
    });
});
