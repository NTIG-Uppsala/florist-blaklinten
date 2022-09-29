let pageLang = document.getElementsByTagName('html')[0].getAttribute('lang');

let iframe_data = `
    <iframe 
        id="mapiframe" 
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2072.472099087858!2d15.768257516460107!3d58.70529006794066!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46594feedcca3b1d%3A0x6c778af446b70e00!2sDe%20Wijks%20v%C3%A4g%2029%2C%20612%2030%20Finsp%C3%A5ng!5e0!3m2!1sen!2sse!4v1664435816938!5m2!1sen!2sse"
        style="border:1;"
        allowfullscreen=""
        width="400"
        height="300"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        >
    </iframe>
`;
let map_div = document.querySelector("#map")
map_div.innerHTML = iframe_data;

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
let closed_days, openhours_text;

if (pageLang == 'uk') {
    /* sort closed days relative to today */
    closed_days = [
        { title: 'Новий рік', month_worded: "січня", month: 1, day: 1 },
        { title: 'Тринадцятий день Різдва', month_worded: "січня", month: 1, day: 6 },
        { title: '1 травня', month_worded: "травня", month: 5, day: 1  },
        { title: 'Національний день Швеції', month_worded: "червня", month: 6, day: 6 },
        { title: 'Святвечір', month_worded: "грудня", month: 12, day: 24 },
        { title: 'Різдво', month_worded: "грудня", month: 12, day: 25 },
        { title: 'День подарунків Різдва', month_worded: "грудня", month: 12, day: 26 },
        { title: 'Переддень Нового року', month_worded: "грудня", month: 12, day: 31 }
    ];

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
else {
    /* sort closed days relative to today */
    closed_days = [
        { title: 'Nyårsdagen', month_worded: "Januari", month: 1, day: 1 },
        { title: 'Trettondedag jul', month_worded: "Januari", month: 1, day: 6 },
        { title: 'Första maj', month_worded: "Maj", month: 5, day: 1  },
        { title: 'Sveriges nationaldag', month_worded: "Juni", month: 6, day: 6 },
        { title: 'Julafton', month_worded: "December", month: 12, day: 24 },
        { title: 'Juldagen', month_worded: "December", month: 12, day: 25 },
        { title: 'Annandag jul', month_worded: "December", month: 12, day: 26 },
        { title: 'Nyårsafton', month_worded: "December", month: 12, day: 31 }
    ];

    openhours_text = {
        "closed": "Vi har stängt idag",
        "closing_soon": "Vi stänger snart",
        "weekdayopenuntil": "Vi har öppet till klockan 16",
        "weekdayopen": "Vi öppnar klockan 10",
        "weekdayclosed": "Vi öppnar klockan 10 imorgon",
        "weekdayclosed2": "Vi öppnar klockan 12 imorgon",
        "weekendopenuntil": "Vi har öppet till klockan 15",
        "weekendopen": "Vi öppnar klockan 12",
        "weekendclosed": "Vi öppnar igen på Måndag klockan 10",
    }
    console.log("Svenska sidan")
}


openhour_element = document.querySelector('#live-openhours');

const current_date = new Date();
const current_day = current_date.getDay();
const current_hour = current_date.getHours();
const current_minute = current_date.getMinutes();

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




/* Sort closing days */
let closed_days_element = document.querySelector('.holidays');
closed_days_element.innerHTML = ''; // Clear inner table

let currentMonth = parseInt(current_date.getMonth() + 1); //get month returns a value between 0 and 11. setting +1 gets the real month number.
let currentDay = parseInt(current_date.getDate());

let dateArr = [];

let pastDates = [];
let futureDates = [];

for(let i = 0; i < closed_days.length; i++)
{
        if(closed_days[i].month <= currentMonth)
        {
            if(closed_days[i].day >= currentDay && closed_days[i].month == currentMonth)
            {
                dateArr.push(closed_days[i])
            }
            else 
            {
                pastDates.push(closed_days[i]);
            }
        }
        else 
        {
        dateArr.push(closed_days[i]);
        
        console.log("past")
        }
}
dateArr = dateArr.concat(pastDates);
for(let i = 0; i < dateArr.length; i++){
    closed_days_element.innerHTML += `
        <tr>
            <th>${dateArr[i].title}</th>
            <td></td>
            <td>${dateArr[i].day} ${dateArr[i].month_worded}</td>
        </tr>
    `
}