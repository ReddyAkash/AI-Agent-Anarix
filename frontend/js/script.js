document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    function addMessage(message, sender) {
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("chat-message", sender);

        const messageBubble = document.createElement("div");
        messageBubble.classList.add("message-bubble");
        messageBubble.innerText = message;

        messageContainer.appendChild(messageBubble);
        chatBox.appendChild(messageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageBubble;
    }

    async function sendMessage() {
        const question = userInput.value.trim();
        if (!question) return;

        addMessage(question, "user");
        userInput.value = "";

        const botMessageBubble = addMessage("...", "bot");

        try {
            const response = await fetch("http://127.0.0.1:8000/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question }),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let botResponse = "";
            botMessageBubble.innerText = "";

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                botResponse += decoder.decode(value, { stream: true });
                botMessageBubble.innerText = botResponse;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        } catch (error) {
            botMessageBubble.innerText = "Sorry, something went wrong.";
            console.error("Error:", error);
        }
    }
});