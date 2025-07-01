// const obj=document.getElementById("msg_form");
// const chatbox=document.getElementById("chatbox");

// async function send_msg(msg) {
//     const response=await fetch('/chat',{
//         method:'POST',
//         headers:{
//             'Content-Type':'application/x-www-form-urlencoded'
//         },
//         body: `message=${encodeURIComponent(msg)}`,
//     });
//     if(response.ok){
//         const data=await response.json();
//         addMessage(data.response);
//     }
    
// }

// function addMessage(message) {
//     const newMessage = document.createElement('div');
//     newMessage.innerText = message;
//     chatbox.appendChild(newMessage);
// }

// obj.addEventListener("submit",(e)=>{
// e.preventDefault();
// const user_msg=obj.elements['message'].value;
// addMessage('user',user_msg);
// sendMessage(user_msg);
// })  

// const messageForm = document.getElementById('messageForm');
// const chatBox = document.getElementById('chatbox');

// function addMessage(message, sender = "bot") {
//     const newMessage = document.createElement('div');
//     newMessage.innerText = `${sender}: ${message}`;
//     chatBox.appendChild(newMessage);
// }

// messageForm.addEventListener('submit', function (e) {
//     e.preventDefault();
//     const userMessage = messageForm.elements['message'].value;
//     addMessage(userMessage, "you");
//     send_msg(userMessage);
//     messageForm.reset();
// });

// async function send_msg(msg) {
//     const response = await fetch('/chat', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded'
//         },
//         body: `message=${encodeURIComponent(msg)}`
//     });

//     if (response.ok) {
//         const data = await response.json();
//         addMessage(data.response, "mistral");
//     } else {
//         addMessage("Error contacting server", "system");
//     }
// }
