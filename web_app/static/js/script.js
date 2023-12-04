let tg = window.Telegram.WebApp;
tg.expand();

let user_id = tg.initDataUnsafe.user.id;

const url = "https://9c1e-91-105-181-137.ngrok-free.app";
const headers = {
    'Content-Type': 'application/json'
    'Authorization': tg.initDataUnsafe.hash,
    'Init-Data': tg.initData
  };

let mario = document.getElementById("mario_id");
let albert = document.getElementById("albert_id");


// Utils
function changeBackColor (element, color) {
    element.style.backgroundColor = color
}

function sendDataToBot (data) {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          console.log("Data has been sent!");
          tg.close();
        })
        .catch((error) => {
          console.error('Error:', error);
        });
}


// Listeners
mario.addEventListener("click", () => {
    console.log("Mario")
    changeBackColor(mario, "#7CB9E8")
    let data = {
        user_id: user_id,
        person_id: 1
    }
    console.log(data)
    sendDataToBot(data)
});

albert.addEventListener("click", () => {
    console.log("Albert")
    changeBackColor(albert, "#7CB9E8")
    let data = {
        user_id: user_id,
        person_id: 2
    }
    console.log(data)
    sendDataToBot(data)
});
