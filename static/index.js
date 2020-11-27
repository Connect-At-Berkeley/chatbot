const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");


   
const BOT_IMG = "https://i.ibb.co/TKjfK1y/Group-8.png";
const PERSON_IMG = "https://i.ibb.co/z7mrNQD/user-icon.png";
const BOT_NAME = "Connect@Cal";
const PERSON_NAME = "You";

$.getJSON("../static/intents.json", function(data)
  {
    for (var i = 0; i<data["intents"].length; i++)
    {
      if(typeof data["intents"][i].links !== 'undefined'){
        console.log(data["intents"][i].links);
      }
    }
  });


function sendMessage(message)
{
  
  const msgText = message;
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  botResponse(msgText);
}

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  botResponse(msgText);
});

    
function appendButton(msg, buttonName) {
  //   Simple solution for small apps
  const msgHTML = ` 
  <button onclick="sendMessage(${msg})" margin-left: 1000px; style=" border-radius: 5px; padding: 10px; font-family: 'Quicksand', sans-serif;" class="msger-send-btn"> ${buttonName}</button>`;
  console.log("appended button")



  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
  console.log("appended button2")
}

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div style="color:#056BA5; background-color:#F0F0F0;" class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          
        </div>

        <div class="msg-text">${text}</div>

      </div>
    </div>
    `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}
    /*function appendLinks(name, img, side, text) {
      //   Simple solution for small apps
      const msgHTML = `
<div class="msg ${side}-msg">
  <div class="msg-img" style="background-image: url(${img})"></div>

  <div style="color:#056BA5; background-color:#F0F0F0;" class="msg-bubble">
    <div class="msg-info">
      <div class="msg-info-name">${name}</div>
      
    </div>

    <div class="msg-text">${text}</div>
  </div>
</div>
`;
    


      msgerChat.insertAdjacentHTML("beforeend", msgHTML);
      msgerChat.scrollTop += 500;
    }*/
function appendMessageChat(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div style="color:black; background-color:white;" class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
    `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(rawText) {

  // Bot Response
  $.get("/get", { msg: rawText }).done(function (data) {
    console.log(rawText);
    console.log(data);
    const msgText = data;
    if (msgText == "Let’s start with getting to know you a little bit better! Which group do you fall in? 🎓"){
      appendMessageChat(BOT_NAME, BOT_IMG, "left", msgText);
      appendButton("'help me please'", "Help Me");
      console.log("after append button")
      
    }
    else {
      appendMessageChat(BOT_NAME, BOT_IMG, "left", msgText);
    }
  });

}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

// function formatDate(date) {
//   const h = "0" + date.getHours();
//   const m = "0" + date.getMinutes();

//   return `${h.slice(-2)}:${m.slice(-2)}`;
// }