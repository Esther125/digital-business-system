var baseUrl = "http://127.0.0.1:8000";

async function getData() {
    const passID = document.getElementById("passID").value;
    const emailAddress = document.getElementById("email-address").value;
    const setPassword = document.getElementById("set-password").value;
    const checkPassword = document.getElementById("check-password").value;

    const response = await fetch(`${baseUrl}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            passID,
            emailAddress,
            setPassword,
            checkPassword,
        }),
    });

    const result = await response.json();
    if (response.ok) {
        alert(result.message);
    } else {
        alert(result.detail);
    }

    console.log(
        passID + ";" + emailAddress + ";" + setPassword + ";" + checkPassword
    );
}
