
tg.expand()

let tg = window.Telegram.WebApp;
let mario = document.getElementById("mario_id");
let albert = document.getElementById("albert_id");

mario.addEventListener("click", () => {
    console.log("Mario")
    let data = {
        user_id: tga.InitDataUnsafe.user.user_id,
        person_id: 1
    }
    console.log(data)
    tg.sendData(JSON.stringify(data));
    tg.close();
});

albert.addEventListener("click", () => {
    console.log("Albert")
    let data = {
        user_id: tg.InitDataUnsafe.user.user_id,
        person_id: 2
    }
    console.log(data)
    tg.sendData(JSON.stringify(data));
    tg.close();
});
