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

    if (userInput.toString().length !== 5) {
        document.getElementById("submitMessage").innerHTML = "Введений поштовий індекс недійсний!";
    } else if (postnumbers.includes(userInput)) {
        document.getElementById("submitMessage").innerHTML = "Доставляємо на ваш поштовий індекс!";
    } else {
        document.getElementById("submitMessage").innerHTML = "Ми не доставляємо на цей поштовий індекс!";
    }

}