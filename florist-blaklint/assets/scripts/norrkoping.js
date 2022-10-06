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
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2080.2348908448453!2d16.245968316391878!3d58.57474118140123!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46593b2205ba56fd%3A0x15793d63ff39bc0c!2sF%C3%A4husgatan%2021%2C%20603%2072%20Norrk%C3%B6ping!5e0!3m2!1ssv!2sse!4v1665056140145!5m2!1ssv!2sse"
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
        96193,
        96194,
        96190,
        96191,
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

let weekdayToString = (int) => {
    switch (int) {
        case 0:
            return "sunday"
            break;
        case 1:
            return "monday"
            break;
        case 2:
            return "tuesday"
            break;
        case 3:
            return "wednesday"
            break;
        case 4:
            return "thursday"
            break;
        case 5:
            return "friday"
            break;
        case 6:
            return "saturday"
            break;
        default:
            break;
    }
}
let openhours_text;
if (pageLang == "sv") {
    openhours_text = {
        "closed": "Vi har stängt idag",
        "closing_soon": "Vi stänger snart",
        "monday": {
            "closeint": 17,
            "openInt": 10,
            "open": "Vi har öppet till 17 idag",
            "closed": "Vi öppnar kl 10 idag",
        },
        "tuesday": {
            "closeint": 16,
            "openInt": 10,
            "open": "Vi har öppet till 16 idag",
            "closed": "Vi öppnar kl 10 idag",
        },
        "wednesday": {
            "closeint": 15,
            "openInt": 10,
            "open": "Vi har öppet till 15 idag",
            "closed": "Vi öppnar kl 10 idag",
        },
        "thursday": {
            "closeint": 16,
            "openInt": 10,
            "open": "Vi har öppet till 16 idag",
            "closed": "Vi öppnar kl 10 idag",
        },
        "friday": {
            "closeint": 16,
            "openInt": 10,
            "open": "Vi har öppet till 16 idag",
            "closed": "Vi öppnar kl 10 idag",
        },
        "saturday": {
            "closeint": 15,
            "openInt": 12,
            "open": "Vi har öppet till 15 idag",
            "closed": "Vi öppnar kl 12 idag",
        },
        "weekdayOpenTommorrow": "Vi öppnar klockan 10 imorgon",
        "weekendOpenTommorrow": "Vi öppnar igen klockan 12 imorgon",
        "weekendclosed": "Vi öppnar igen på Måndag klockan 10",
    }
}
else {
    openhours_text = {
        "closed": "Сьогодні ми закриті",
        "closing_soon": "Ми скоро зачиняємося",
        "monday": {
            "closeint": 17,
            "openInt": 10,
            "open": "Ми працюємо до 17:00",
            "closed": "Ми відкриваємось о 10:00",
        },
        "tuesday": {
            "closeint": 16,
            "openInt": 10,
            "open": "Ми працюємо до 16:00",
            "closed": "Ми відкриваємось о 10:00",
        },
        "wednesday": {
            "closeint": 15,
            "openInt": 10,
            "open": "Ми працюємо до 15:00",
            "closed": "Ми відкриваємось о 10:00",
        },
        "thursday": {
            "closeint": 16,
            "openInt": 10,
            "open": "Ми працюємо до 16:00",
            "closed": "Ми відкриваємось о 10:00",
        },
        "friday": {
            "closeint": 16,
            "openInt": 10,
            "open": "Ми працюємо до 16:00",
            "closed": "Ми відкриваємось о 10:00",
        },
        "saturday": {
            "closeint": 15,
            "openInt": 12,
            "open": "Ми працюємо до 15:00",
            "closed": "Ми відкриваємось о 12:00",
        },
        "weekdayOpenTommorrow": "Ми відкриваємось о 10:00 завтра",
        "weekendOpenTommorrow": "Ми відкриваємось о 12:00 ранку. завтра",
        "weekendclosed": "Ми знову відкриваємось у понеділок о 10:00",
    }
}

openhour_element = document.querySelector('#live-openhours');
current_date = new Date();
current_day = current_date.getDay();
let current_day_string = weekdayToString(current_day);
current_hour = current_date.getHours();
current_minute = current_date.getMinutes();


// Closed on sundays
if (current_day == 0) {
    openhour_element.innerText = openhours_text.closed;
} 
else if (current_day >= 1 && current_day <= 6) {
    // on all other days

    // If its less than 30 minutes until closing time
    if (current_hour == (openhours_text[current_day_string].closeint - 1) && current_minute >= 30) {
        openhour_element.innerText = openhours_text.closing_soon;
    }

    // If its open
    else if (current_hour >= openhours_text[current_day_string].openInt && current_hour < openhours_text[current_day_string].closeint) {
        openhour_element.innerText = openhours_text[current_day_string].open;
    }

    // if its before opening time
    else if (current_hour < openhours_text[current_day_string].openInt) {
        openhour_element.innerText = openhours_text[current_day_string].closed;
    }
    else {
        // if its after closing time

        // if its a weekday
        if (current_hour > openhours_text[current_day_string].closeint && current_day >= 1 && current_day <= 5) {
            openhour_element.innerText = openhours_text.weekdayOpenTommorrow;
        }

        // if its a weekend
        else if (current_hour > openhours_text[current_day_string].closeint && current_day == 6) {
            openhour_element.innerText = openhours_text.weekendOpenTommorrow;
        }
    }
}
else {
    openhour_element.innerText = current_day
}