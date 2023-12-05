// Example POST method implementation:

document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.getElementById("toggleSidebar");
  const sidebar = document.querySelector(".sidebar");

  toggleButton.addEventListener("click", function () {
    sidebar.classList.toggle("hidden");
  });
  const voiceButton = document.getElementById("voiceButton");

  voiceButton.addEventListener("click", function () {
      startVoiceRecognition();
  });
});

async function startVoiceRecognition() {
  const recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.lang = 'en-US';

  recognition.onresult = function (event) {
      const result = event.results[0][0].transcript;
      questionInput.value = result;
  };

  recognition.onerror = function (event) {
      console.error('Speech recognition error:', event.error);
  };

  recognition.start();
}

async function postData(url = "", data = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

const sendButton = document.getElementById("sendButton");
const questionInput = document.getElementById("questionInput");
const right1 = document.querySelector(".right1");
const right2 = document.querySelector(".right2");
const modelSelect = document.getElementById("modelSelect");



sendButton.addEventListener("click", async () => {
  const question = questionInput.value;
  questionInput.value = "";

  // Hide the entire right1 div
  right1.style.display = "none";

  // Show the input within right1 and right2
  questionInput.style.display = "block";
  right2.style.display = "block";

  // Set the questions in the chat interface
  document.getElementById("question1").innerHTML = question;
  document.getElementById("question2").innerHTML = question;
  const selectedModel = modelSelect.value;

  // Get the answer and populate it!
  const result = await postData("/api", { question: question, model: selectedModel });
  document.getElementById("solution").innerHTML = result.answer;
  // const result = await postData("/api", { question: question });
  // document.getElementById("solution").innerHTML = result.answer;
});

