// const messageForm = document.getElementById('messageForm') as HTMLFormElement;
// const chatBox = document.getElementById('chatbox') as HTMLDivElement;
// const messageInput = document.getElementById('message') as HTMLInputElement;

// function addMessage(text: string, sender: 'user' | 'bot'): void {
//     const msgDiv = document.createElement('div');
//     msgDiv.className = `message ${sender}`;
//     msgDiv.textContent = `${sender === 'user' ? 'You' : 'Mistral'}: ${text}`;
//     chatBox.appendChild(msgDiv);
//     chatBox.scrollTop = chatBox.scrollHeight;
// }

// function speak(text: string): void {
//     const utterance = new SpeechSynthesisUtterance(text);
//     speechSynthesis.speak(utterance);
// }

// async function send_msg(msg: string): Promise<void> {
//     const response = await fetch('/chat', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//         },
//         body: `message=${encodeURIComponent(msg)}`
//     });

//     if (response.ok) {
//         const data: { response: string } = await response.json();
//         addMessage(data.response, 'bot');
//         speak(data.response);
//     } else {
//         addMessage("Error contacting server", 'bot');
//     }
// }

// messageForm.addEventListener('submit', function (e: Event) {
//     e.preventDefault();
//     const userMessage = messageInput.value.trim();
//     if (userMessage) {
//         addMessage(userMessage, 'user');
//         send_msg(userMessage);
//         messageInput.value = '';
//     }
// });
