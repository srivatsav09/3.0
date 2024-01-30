chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "summarize") {
    // Implement your text summarization logic here
    let summarizedText = "This is a sample summary.";
    sendResponse({ summary: summarizedText });
  }
  // Add other actions as needed
});
