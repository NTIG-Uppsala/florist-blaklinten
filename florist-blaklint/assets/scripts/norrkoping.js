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
        document.getElementById("submitMessage").innerHTML = "Det angivna postnumret är inte giltigt!";
    } else if (postnumbers.includes(userInput)) {
        document.getElementById("submitMessage").innerHTML = "Vi kör ut till ditt postnummer!";
    } else {
        document.getElementById("submitMessage").innerHTML = "Vi kör inte ut till detta postnummer!";
    }

}