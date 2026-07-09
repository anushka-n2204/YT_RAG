// =====================================================
//                  DOM ELEMENTS
// =====================================================

const youtubeInput = document.getElementById("youtube_url");
const loadVideoBtn = document.getElementById("loadVideoBtn");
const sendBtn = document.getElementById("sendBtn");
const questionInput = document.getElementById("question");
const thumbnail = document.getElementById("thumbnail");
const videoTitle = document.getElementById("videoTitle");
const statusText = document.getElementById("status");
const chatContainer = document.getElementById("chatContainer");
const typing = document.getElementById("typing");
const logoutBtn = document.getElementById("logoutBtn");
const userId = document.getElementById("userid");

// =====================================================
//                PAGE INITIALIZATION
// =====================================================

window.onload = () => {
    const user = getUser();

    if (user == null) {
        window.location.href = "login.html";
        return;
    }

    userId.innerHTML = "User ID : " + user;
    typing.style.display = "none";
};

// =====================================================
//                     LOGOUT
// =====================================================

logoutBtn.addEventListener("click", () => logout());

// =====================================================
//              LOAD YOUTUBE VIDEO
// =====================================================

loadVideoBtn.addEventListener("click", loadVideo);

async function loadVideo() {
    const youtube_url = youtubeInput.value.trim();

    if (youtube_url === "") {
        alert("Please enter a YouTube URL.");
        return;
    }

    loadVideoBtn.disabled = true;
    loadVideoBtn.innerHTML = "Loading...";
    statusText.innerHTML = "Creating Vector Store...";

    try {
        const data = await ingestVideo(youtube_url);
        console.log(data);

        if (data.status) {
            saveConversation(data.conversation_id);
            statusText.innerHTML = "AI Ready";
            videoTitle.innerHTML = "Video Loaded Successfully";
            appendBotMessage("✅ Video Loaded Successfully.\n\nYou can now ask questions about this video.");
            questionInput.focus();
        } else {
            statusText.innerHTML = "Failed";
            alert(data.message || "Unable to load video.");
        }
    } catch (error) {
        console.error(error);
        statusText.innerHTML = "Failed";
        alert("Unable to load video.");
    } finally {
        loadVideoBtn.disabled = false;
        loadVideoBtn.innerHTML = "Load Video";
    }
}

// =====================================================
//                  SEND QUESTION
// =====================================================

sendBtn.addEventListener("click", sendQuestion);

questionInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendQuestion();
    }
});

async function sendQuestion() {
    const question = questionInput.value.trim();

    if (question === "") {
        return;
    }

    const conversation_id = getConversation();
    if (conversation_id == null) {
        alert("Please load a YouTube video first.");
        return;
    }

    sendBtn.disabled = true;
    questionInput.disabled = true;

    appendUserMessage(question);
    questionInput.value = "";
    typing.style.display = "block";

    try {
        const data = await askQuestion(question);
        console.log(data);
        typing.style.display = "none";

        if (data?.status === false) {
            appendBotMessage(data.message || "Unable to generate a response right now.");
        } else if (data?.BOT || data?.bot || data?.message) {
            appendBotMessage(data.BOT || data.bot || data.message);
        } else {
            appendBotMessage("No response received.");
        }
    } catch (error) {
        console.log(error);
        typing.style.display = "none";
        appendBotMessage("Server Error.");
    } finally {
        sendBtn.disabled = false;
        questionInput.disabled = false;
        questionInput.focus();
    }
}

// =====================================================
//              APPEND USER MESSAGE
// =====================================================

function appendUserMessage(message) {
    const messageBox = document.createElement("div");
    messageBox.classList.add("user-message");
    messageBox.innerHTML = message;
    chatContainer.appendChild(messageBox);
    scrollToBottom();
}

// =====================================================
//              APPEND BOT MESSAGE
// =====================================================

function appendBotMessage(message) {
    const messageBox = document.createElement("div");
    messageBox.classList.add("bot-message");
    messageBox.innerHTML = message;
    chatContainer.appendChild(messageBox);
    scrollToBottom();
}

// =====================================================
//              SHOW TYPING ANIMATION
// =====================================================

function showTyping() {
    typing.style.display = "block";
}

function hideTyping() {
    typing.style.display = "none";
}

// =====================================================
//             AUTO SCROLL CHAT
// =====================================================

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// =====================================================
//              CHECK LOGIN SESSION
// =====================================================

function checkLogin() {
    const user = getUser();
    if (user == null) {
        alert("Please Login First.");
        window.location.href = "login.html";
        return false;
    }
    return true;
}

// =====================================================
//          PAGE STARTUP CHECK
// =====================================================

if (!checkLogin()) {
    throw new Error("User Not Logged In");
}
