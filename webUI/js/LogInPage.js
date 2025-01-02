async function getData() {
    const emailAddress = document.getElementById("email-address").value;
    const password = document.getElementById("password").value;
    const baseUrl = "http://127.0.0.1:8000"; // 部署的時候要改

    try {
        const response = await fetch(`${baseUrl}/token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                username: emailAddress, // 後端要改成 email
                password: password,
            }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const access_token = data.access_token;
        // 把 JWT 儲存在 session
        sessionStorage.setItem("token", access_token);
        // 登入成功後跳轉頁面
        window.location.href = `${baseUrl}/mainPage`;
        console.log(data);
        return data;
    } catch (error) {
        console.error("Failed to call /token:", error);
    }
}
