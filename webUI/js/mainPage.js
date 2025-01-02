var baseUrl = "http://127.0.0.1:8000"; // 部署時需修改

document.addEventListener("DOMContentLoaded", function () {
    const loginLogoutLink = document.getElementById("loginLogoutLink");
    const linkText = document.getElementById("linkText");
    const token = sessionStorage.getItem("token");

    if (token) {
        linkText.textContent = "登出";
        loginLogoutLink.addEventListener("click", function (event) {
            event.preventDefault();
            sessionStorage.removeItem("token");
            window.location.href = `${baseUrl}/webUI/LogInPage.html`;
        });
    } else {
        linkText.textContent = "登入";
        loginLogoutLink.href = `${baseUrl}/webUI/LogInPage.html`;
    }
});
