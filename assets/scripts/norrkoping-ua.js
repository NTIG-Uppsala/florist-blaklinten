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

    if (userInput.toString().length !== 5) {
        document.getElementById("submitMessage").innerHTML = "Введений поштовий індекс недійсний!";
    } else if (postnumbers.includes(userInput)) {
        document.getElementById("submitMessage").innerHTML = "Доставляємо на ваш поштовий індекс!";
    } else {
        document.getElementById("submitMessage").innerHTML = "Ми не доставляємо на цей поштовий індекс!";
    }

}