pageLang = document.getElementsByTagName('html')[0].getAttribute('lang');

let submitContainer = document.getElementById("submitContainer");

if (pageLang == "sv") {
    submitContainer.innerHTML = `      
        <p style="color: white; font-size: 20px;"> Ange ditt postnummer nedan <br> för att se om vi kör ut till dig.</p>
        <p style="color: white;" id="submitMessage"></p>
        <form id="submitForm">  
            <input type="text" id="submitText">
            <button type="submit" id="submitButton">Skicka</button>
        </form>`
} else {
    submitContainer.innerHTML = `
        <p style="color: white; font-size: 20px;"> Введіть свій поштовий індекс нижче, <br> щоб дізнатися, чи ми доставляємо вам.</p>
        <p style="color: white;" id="submitMessage"></p>
        <form id="submitForm">
            <input type="text" id="submitText">
            <button type="submit" id="submitButton">Надіслати</button>
        </form>`
}

let iframe_data = `
    <iframe 
        id="mapiframe" 
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2072.472099087858!2d15.768257516460107!3d58.70529006794066!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46594feedcca3b1d%3A0x6c778af446b70e00!2sDe%20Wijks%20v%C3%A4g%2029%2C%20612%2030%20Finsp%C3%A5ng!5e0!3m2!1sen!2sse!4v1664435816938!5m2!1sen!2sse"
        style="border:0;"
        allowfullscreen=""
        width="300"
        height="300"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        >
    </iframe>
`;
let map_div = document.querySelector("#map")
map_div.innerHTML = iframe_data;

document.getElementById("submitButton").onclick = function() {
    let form = document.getElementById("submitForm");
    function handleForm(event) { event.preventDefault(); } 
    form.addEventListener('submit', handleForm);

    const postnumbers = [
        98139,
        98140,
        98142,
        98138
    ]

    let userInput = parseInt(document.getElementById("submitText").value);

    if (pageLang == "sv") {
        if (userInput.toString().length !== 5) {
            document.getElementById("submitMessage").innerHTML = "Det angivna postnumret är inte giltigt!";
        } else if (postnumbers.includes(userInput)) {
            document.getElementById("submitMessage").innerHTML = "Vi kör ut till ditt postnummer!";
        } else {
            document.getElementById("submitMessage").innerHTML = "Vi kör inte ut till detta postnummer!";
        }
    } else {
        if (userInput.toString().length !== 5) {
            document.getElementById("submitMessage").innerHTML = "Введений поштовий індекс недійсний!";
        } else if (postnumbers.includes(userInput)) {
            document.getElementById("submitMessage").innerHTML = "Доставляємо на ваш поштовий індекс!";
        } else {
            document.getElementById("submitMessage").innerHTML = "Ми не доставляємо на цей поштовий індекс!";
        }
    }

}

let openhours = {
    "weekdays": {
        "open": 10,
        "close": 16
    },
    "saturday": {
        "open": 12,
        "close": 15
    },
    "sunday": {
        "open": "Closed",
        "close": "Closed"
    }
}

let openhours_text;
if (pageLang == "sv") {
    openhours_text = {
        "closed": "Vi har stängt idag",
        "closing_soon": "Vi stänger snart",
        "weekdayopenuntil": "Vi har öppet till klockan 16 idag",
        "weekdayopen": "Vi öppnar klockan 10",
        "weekdayclosed": "Vi öppnar klockan 10 imorgon",
        "weekdayclosed2": "Vi öppnar klockan 12 imorgon",
        "weekendopenuntil": "Vi har öppet till klockan 15 idag",
        "weekendopen": "Vi öppnar klockan 12",
        "weekendclosed": "Vi öppnar igen på Måndag klockan 10",
    }
}
else {
    openhours_text = {
        "closed": "Сьогодні ми закриті",
        "closing_soon": "Ми скоро зачиняємося",
        "weekdayopenuntil": "Ми працюємо до 16:00",
        "weekdayopen": "Ми відкриваємось о 10:00",
        "weekdayclosed": "Ми відкриваємось о 10:00 завтра",
        "weekdayclosed2": "Ми відкриваємось о 12 ранку. завтра",
        "weekendopenuntil": "Ми працюємо до 15:00",
        "weekendopen": "Ми відкриваємось о 12:00",
        "weekendclosed": "Ми знову відкриваємось у понеділок о 10:00",
    }
}

openhour_element = document.querySelector('#live-openhours');

current_date = new Date();
current_day = current_date.getDay();
current_hour = current_date.getHours();
current_minute = current_date.getMinutes();

if (current_day == 0) {
    openhour_element.innerText = openhours_text.closed;
} else if (current_day == 6) {
    if ((current_hour == (openhours.saturday.close - 1)) && current_minute >= 30) {
        openhour_element.innerText = openhours_text.closing_soon;
    } else if (current_hour >= openhours.saturday.open && current_hour < openhours.saturday.close) {
        openhour_element.innerText = openhours_text.weekendopenuntil;
    } else if (current_hour >= openhours.saturday.close) {
        openhour_element.innerText = openhours_text.weekendclosed;
    } else {
        openhour_element.innerText = openhours_text.weekendopen;
    }
} else if (current_day >= 1 && current_day <= 5) {
    if ((current_hour == (openhours.weekdays.close - 1)) && current_minute >= 30) {
        openhour_element.innerText = openhours_text.closing_soon;
    } else if (current_hour >= openhours.weekdays.open && current_hour < openhours.weekdays.close) {
        openhour_element.innerText = openhours_text.weekdayopenuntil;
    } else if (current_hour >= openhours.weekdays.close) {
        if (current_day + 1 == 6) {
            openhour_element.innerText = openhours_text.weekdayclosed2;
        } else {
            openhour_element.innerText = openhours_text.weekdayclosed;
        }
    } else {
        openhour_element.innerText = openhours_text.weekdayopen;
    }
}