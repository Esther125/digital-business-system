function getData() {
    const passID = document.getElementById("passID").value;
    const emailAddress = document.getElementById("email-address").value;
    const setPassword = document.getElementById("set-password").value;
    const checkPassword = document.getElementById("check-password").value;
    console.log(
        passID + ";" + emailAddress + ";" + setPassword + ";" + checkPassword
    );
}
