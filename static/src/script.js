const chatbotToggle = document.querySelector('.chatbot-toggle');
const chatbot = document.querySelector('.chatbot');
const chatMessages = document.querySelector('.chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const closeBtn = document.querySelector('.close-btn');

chatbotToggle.addEventListener('click', () => {
    if (chatbot.classList.contains('hidden')) {
        chatbot.classList.remove('hidden');
        setTimeout(() => chatbot.classList.add('chat-open'), 10);
    } else {
        chatbot.classList.remove('chat-open');
        setTimeout(() => chatbot.classList.add('hidden'), 300);
    }
});

closeBtn.addEventListener('click', () => {
    chatbot.classList.remove('chat-open');
    setTimeout(() => chatbot.classList.add('hidden'), 300);
});

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const messageText = userInput.value.trim();
    if (messageText) {
        const userMessageWrapper = document.createElement('div');
        userMessageWrapper.classList.add('message-wrapper', 'flex', 'items-center', 'mb-2', 'self-end');

        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user', 'bg-blue-100', 'p-2', 'rounded-lg', 'mr-2');
        userMessage.textContent = messageText;

        userMessageWrapper.appendChild(userMessage);

        const userEmoji = document.createElement('span');
        userEmoji.textContent = '👨';
        userMessageWrapper.appendChild(userEmoji);

        chatMessages.appendChild(userMessageWrapper);
        userInput.value = '';

        const spinner = document.querySelector('.spinner');
        spinner.classList.remove('hidden');

        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: messageText }),
        })
        .then(response => response.json())
        .then(data => {
            const botMessageWrapper = document.createElement('div');
            botMessageWrapper.classList.add('message-wrapper', 'flex', 'items-center', 'mb-2');

            const botEmoji = document.createElement('span');
            botEmoji.textContent = '🤖';
            botMessageWrapper.appendChild(botEmoji);

            const botMessage = document.createElement('div');
            botMessage.classList.add('message', 'bot', 'bg-green-100', 'p-2', 'rounded-lg', 'ml-2');
            botMessage.textContent = data.reply;

            botMessageWrapper.appendChild(botMessage);
            chatMessages.appendChild(botMessageWrapper);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            spinner.classList.add('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            spinner.classList.add('hidden');
        });
    }
}
