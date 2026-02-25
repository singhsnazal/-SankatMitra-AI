const chat = document.getElementById("chat");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const uploadBtn = document.getElementById("uploadBtn");
const imageInput = document.getElementById("imageInput");

let selectedImage = null;

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
// Send Message
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