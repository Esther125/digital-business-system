var baseUrl = window.ENV_CONFIG.BASE_URL; // 部署時需修改

document.addEventListener("DOMContentLoaded", function () {
    const loginLogoutLink = document.getElementById("loginLogoutLink");
    const linkText = document.getElementById("linkText");
    const token = sessionStorage.getItem("token");

    if (token) {
        linkText.textContent = "登出";
        loginLogoutLink.addEventListener("click", function (event) {
            event.preventDefault();
            sessionStorage.removeItem("token");
            window.location.href = `${baseUrl}/LogInPage`;
        });
    } else {
        linkText.textContent = "登入";
        loginLogoutLink.href = `${baseUrl}/LogInPage`;
    }
});
