const toggleButton = document.querySelector('.dark-light');
const colors = document.querySelectorAll('.color');
// window.onload = function() {
//   document.body.classList.toggle('dark-mode');
// };
document.body.classList.toggle('dark-mode');
colors.forEach(color => {
  color.addEventListener('click', e => {
    colors.forEach(c => c.classList.remove('selected'));
    const theme = color.getAttribute('data-color');
    document.body.setAttribute('data-theme', theme);
    color.classList.add('selected');
  });
});

toggleButton.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
});

  function appendOwnerMessage() {
    // Create elements
    var text = document.getElementById('prompt').value;
    var chatMsg = document.createElement('div');
    chatMsg.classList.add('chat-msg');
    chatMsg.classList.add('owner');
    var chatMsgContent = document.createElement('div');
    chatMsgContent.classList.add('chat-msg-content');
    
    var chatMsgText = document.createElement('div');
    chatMsgText.classList.add('chat-msg-text');
    chatMsgText.textContent = text;
    
    // Append elements
    chatMsgContent.appendChild(chatMsgText);
    chatMsg.appendChild(chatMsgContent);
    
    // Append to existing div with id 'msgs'
    var msgsDiv = document.getElementById('msgs');
    if (msgsDiv) {
        msgsDiv.appendChild(chatMsg);
    } else {
        console.error('msgs div not found');
    }
}
function appendMessage() {
  // Create elements
  var text = document.getElementById('prompt').value;
  var chatMsg = document.createElement('div');
  chatMsg.classList.add('chat-msg-content');
  var chatMsgContent = document.createElement('div');
  chatMsgContent.classList.add('chat-msg-content');
  
  var chatMsgText = document.createElement('div');
  chatMsgText.classList.add('chat-msg-text');
  chatMsgText.textContent = text;
  
  // Append elements
  chatMsgContent.appendChild(chatMsgText);
  chatMsg.appendChild(chatMsgContent);
  
  // Append to existing div with id 'msgs'
  var msgsDiv = document.getElementById('msgs');
  if (msgsDiv) {
      msgsDiv.appendChild(chatMsg);
  } else {
      console.error('msgs div not found');
  }
}

// Prevent form submission on button click
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('messageForm').addEventListener('submit', function(event) {
        event.preventDefault();
    });
});

