const chat = document.getElementById("chat");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const uploadBtn = document.getElementById("uploadBtn");
const imageInput = document.getElementById("imageInput");
const recordBtn = document.getElementById("recordBtn");

let selectedImage = null;

// 🎙 Recording variables
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// ==========================
// Upload Image
// ==========================
uploadBtn.addEventListener("click", () => {
  imageInput.click();
});

imageInput.addEventListener("change", () => {
  selectedImage = imageInput.files[0];

  if (selectedImage) {
    addMessage("📷 Image selected: " + selectedImage.name, "user");
  }
});

// ==========================
// 🎙 Microphone Recording
// ==========================
recordBtn.addEventListener("click", async () => {
  if (!isRecording) {
    startRecording();
  } else {
    stopRecording();
  }
});

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = sendAudioToServer;

    mediaRecorder.start();
    isRecording = true;
    recordBtn.innerText = "⏹";
    addMessage("🎙 Recording...", "user");

  } catch (err) {
    addMessage("Microphone permission denied.", "bot");
  }
}

function stopRecording() {
  mediaRecorder.stop();
  isRecording = false;
  recordBtn.innerText = "🎙";
}

// ==========================
// Send Recorded Audio
// ==========================
async function sendAudioToServer() {
  const audioBlob = new Blob(audioChunks, { type: "audio/webm" });

  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");

  try {
    const response = await fetch("/query", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (data.transcribed_text) {
      addMessage("📝 " + data.transcribed_text, "bot");
    }

    if (data.answer) {
      addMessage(data.answer, "bot");
    } else if (data.error) {
      addMessage("Error: " + data.error, "bot");
    }

  } catch (error) {
    addMessage("Audio processing failed.", "bot");
  }
}

// ==========================
// Send Text / Image
// ==========================
sendBtn.addEventListener("click", async () => {
  const query = document.getElementById("query").value.trim();

  if (!query && !selectedImage) return;

  if (query) addMessage(query, "user");

  const formData = new FormData();

  if (query) formData.append("question", query);
  if (selectedImage) formData.append("image", selectedImage);

  try {
    const response = await fetch("/query", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (data.answer) {
      addMessage(data.answer, "bot");
    } else if (data.error) {
      addMessage("Error: " + data.error, "bot");
    }

  } catch (error) {
    addMessage("Server error. Please try again.", "bot");
  }

  // Reset inputs
  document.getElementById("query").value = "";
  imageInput.value = "";
  selectedImage = null;
});

// ==========================
// Clear Chat
// ==========================
clearBtn.addEventListener("click", () => {
  chat.innerHTML = "";
});

// ==========================
// Add Message Bubble
// ==========================
function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = "message " + sender;
  msg.innerText = text;
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}