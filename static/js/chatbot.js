document.addEventListener("DOMContentLoaded", function () {

    const chatbotButton =
        document.getElementById("chatbot-button");

    const chatbotWindow =
        document.getElementById("chatbot-window");

    const chatbotClose =
        document.getElementById("chatbot-close");

    const chatbotForm =
        document.getElementById("chatbot-form");

    const chatbotInput =
        document.getElementById("chatbot-input");

    const chatbotMessages =
        document.getElementById("chatbot-messages");


    if (
        !chatbotButton ||
        !chatbotWindow ||
        !chatbotForm ||
        !chatbotInput ||
        !chatbotMessages
    ) {
        return;
    }


    // =====================================================
    // OPEN CHATBOT
    // =====================================================

    chatbotButton.addEventListener(
        "click",
        function () {

            chatbotWindow.classList.add("active");

            chatbotButton.classList.add("hidden");

            setTimeout(function () {

                chatbotInput.focus();

            }, 250);
        }
    );


    // =====================================================
    // CLOSE CHATBOT
    // =====================================================

    if (chatbotClose) {

        chatbotClose.addEventListener(
            "click",
            function () {

                chatbotWindow.classList.remove("active");

                chatbotButton.classList.remove("hidden");

            }
        );
    }


    // =====================================================
    // ADD MESSAGE
    // =====================================================

    function addMessage(message, sender) {

        const messageWrapper =
            document.createElement("div");

        messageWrapper.className =
            "chat-message " + sender;


        const messageBubble =
            document.createElement("div");

        messageBubble.className =
            "chat-message-bubble";


        messageBubble.textContent =
            message;


        messageWrapper.appendChild(
            messageBubble
        );


        chatbotMessages.appendChild(
            messageWrapper
        );


        scrollToBottom();


        return messageWrapper;
    }


    // =====================================================
    // TYPING INDICATOR
    // =====================================================

    function showTypingIndicator() {

        const typingWrapper =
            document.createElement("div");

        typingWrapper.className =
            "chat-message bot typing-message";


        typingWrapper.innerHTML = `
            <div class="chat-message-bubble typing-bubble">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;


        chatbotMessages.appendChild(
            typingWrapper
        );


        scrollToBottom();


        return typingWrapper;
    }


    // =====================================================
    // SCROLL
    // =====================================================

    function scrollToBottom() {

        chatbotMessages.scrollTop =
            chatbotMessages.scrollHeight;
    }


    // =====================================================
    // SEND MESSAGE TO AI
    // =====================================================

    async function sendMessage(message) {

        if (!message) {
            return;
        }


        addMessage(
            message,
            "user"
        );


        chatbotInput.value = "";


        chatbotInput.disabled = true;


        const sendButton =
            chatbotForm.querySelector(
                "button[type='submit']"
            );


        if (sendButton) {

            sendButton.disabled = true;

        }


        const typingIndicator =
            showTypingIndicator();


        try {

            const response =
                await fetch(
                    "/api/chat",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            message: message

                        })

                    }
                );


            const data =
                await response.json();


            typingIndicator.remove();


            if (
                !response.ok ||
                !data.success
            ) {

                addMessage(

                    data.error ||
                    "Sorry, I couldn't process your request.",

                    "bot"

                );

                return;
            }


            addMessage(
                data.answer,
                "bot"
            );


        } catch (error) {

            console.error(
                "Chatbot error:",
                error
            );


            typingIndicator.remove();


            addMessage(

                "I'm having trouble connecting right now. Please try again.",

                "bot"

            );


        } finally {

            chatbotInput.disabled = false;


            if (sendButton) {

                sendButton.disabled = false;

            }


            chatbotInput.focus();

        }

    }


    // =====================================================
    // NORMAL MESSAGE SUBMISSION
    // =====================================================

    chatbotForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const message =
                chatbotInput.value.trim();


            if (!message) {
                return;
            }


            sendMessage(message);

        }
    );


    // =====================================================
    // SUGGESTION BUTTONS
    // =====================================================

    const suggestions =
        document.querySelectorAll(
            ".chat-suggestion"
        );


    suggestions.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const question =
                    button.dataset.question;


                if (!question) {
                    return;
                }


                sendMessage(question);

            }
        );

    });


    // =====================================================
    // ENTER KEY
    // =====================================================

    chatbotInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                chatbotForm.requestSubmit();

            }

        }
    );

});

