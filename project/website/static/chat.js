document.addEventListener("DOMContentLoaded", function () {
    // Initialize the chat widget on page load.
    initChatWidget();
  });
  
  function toggleAudio() {
    let audio = document.getElementById('bg-audio');
    let icon = document.getElementById('audio-icon');
  
    if (audio.paused) {
      audio.play();
      // Adjust the path if necessary or use templating as in your HTML.
      icon.src = "/static/sound1.png";
    } else {
      audio.pause();
      icon.src = "/static/sound.png";
    }
  }
  
  function initChatWidget() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    
    // Add an initial greeting message.
    addMessage('Welcome to Itihasa! How can I help you plan your journey through India\'s heritage?', 'bot');
    
    // Toggle chat widget visibility.
    chatToggle.addEventListener('click', function() {
      if (chatWidget.style.display === 'none' || chatWidget.style.display === '') {
        chatWidget.style.display = 'block';
        // Change the toggle icon to a "close" icon.
        chatToggle.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
      } else {
        chatWidget.style.display = 'none';
        // Change back to the default chat icon.
        chatToggle.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';
      }
    });
    
    // Allow sending messages via the Enter key.
    document.getElementById('user-input').addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  }
  
  function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;
    
    // Add the user message to the chat widget.
    addMessage(message, 'user');
    input.value = '';
    
    // Send the message to the server.
    fetch('/chatbot/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
      // If the server provides a redirect URL, redirect the browser.
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else {
        addMessage(data.response, 'bot');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      addMessage('Sorry, there was an error processing your request.', 'bot');
    });
  }
  
  function addMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    
    if (sender === 'user') {
      messageElement.classList.add('user-message');
      messageElement.textContent = message;
    } else {
      messageElement.classList.add('bot-message');
      messageElement.textContent = message;
    }
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  