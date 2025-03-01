const uploadButton = document.querySelector("#upload-button");
const fileInput = document.querySelector("#file-input");
const calorieCount = document.querySelector("#calorie-count");
const foodItem = document.querySelector("#food-item");
const imagePreview = document.querySelector("#image-preview");
const imagePreviewContainer = document.querySelector(
  "#image-preview-container"
);

document.querySelectorAll(".navbar a").forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    target.scrollIntoView({ behavior: "smooth" });
  });
});

const errorMessage = document.querySelector("#error-message");
const loadingText = document.querySelector("#loading-text");
const loadingMessagesContainer = document.querySelector("#loading-messages");

uploadButton.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;

  resetUI(); // ✅ Clears previous results before uploading

  // Show image preview
  const reader = new FileReader();
  reader.onload = function (e) {
    imagePreview.src = e.target.result;
    imagePreviewContainer.style.display = "block";
  };
  reader.readAsDataURL(file);

  // Start loading messages first, then call uploadImage after 6 sec
  startLoadingMessages(() => {
    uploadImage(file);
  });
});

function uploadImage(file) {
  errorMessage.style.display = "none";

  const fd = new FormData();
  fd.append("image", file);

  fetch("/upload", {
    method: "POST",
    body: fd,
  })
    .then((response) => response.json())
    .then((data) => {
      stopLoadingMessages();
      if (data.error) {
        showError(data.error);
        return;
      }

      foodItem.textContent = `🍽️ ${data.calories.food_items[0].name}`;
      calorieCount.textContent = `🔥 ${data.calories.total} kcal`;

      foodItem.style.opacity = "1";
      calorieCount.style.opacity = "1";
    })
    .catch(() => {
      stopLoadingMessages();
      showError("Error processing image. Please try again.");
    });
}

// ✅ Function to reset UI before a new upload
function resetUI() {
  foodItem.textContent = "";
  calorieCount.textContent = "";
  foodItem.style.opacity = "0";
  calorieCount.style.opacity = "0";
  loadingText.textContent = "";
  loadingMessagesContainer.style.display = "none";
  errorMessage.style.display = "none";
}

// Function to show loading messages in order, then call API
function startLoadingMessages(callback) {
  uploadButton.textContent = "Processing...";
  loadingMessagesContainer.style.display = "block";
  loadingText.style.opacity = "0";

  const messages = [
    "Segmenting image using Mask R-CNN...",
    "Detecting the food item using YOLOv8...",
    "Finding the calories using volume...",
  ];

  let index = 0;

  function showNextMessage() {
    if (index < messages.length) {
      loadingText.style.opacity = "0";
      setTimeout(() => {
        loadingText.textContent = messages[index];
        loadingText.style.opacity = "1";
        index++;
        setTimeout(showNextMessage, 1500); // Show next message after 2 sec
      }, 500);
    } else {
      // After all messages are shown, call the callback (uploadImage)
      setTimeout(callback, 1000);
    }
  }

  showNextMessage();
}

// Function to stop loading messages
function stopLoadingMessages() {
  uploadButton.textContent = "Upload Image";
  loadingMessagesContainer.style.display = "none";
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.style.display = "block";
}
