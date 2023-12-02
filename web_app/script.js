let tg = window.Telegram.WebApp;
tg.expand()

let mario = document.getElementById("mario_id");
let albert = document.getElementById("albert_id");


function changeBackColor (element, color) {
    element.style.backgroundColor = color
}

mario.addEventListener("click", () => {
    console.log("Mario")
    changeBackColor(mario, "#7CB9E8")
    let data = {
        user_id: tg.InitDataUnsafe.user.id,
        person_id: 1
    }
    console.log(data)
    tg.sendData(JSON.stringify(data));
    tg.close();
});

albert.addEventListener("click", () => {
    console.log("Albert")
    changeBackColor(albert, "#7CB9E8")
    let data = {
        user_id: tg.InitDataUnsafe.user.id,
        person_id: 2
    }
    console.log(data)
    tg.sendData(JSON.stringify(data));
    tg.close();
});
