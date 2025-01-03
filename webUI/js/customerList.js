function fetchCustomerData() {
    //在這裡抓資料

    //先放假資料
    var customers = [
        {
            userId: "User#5",
            rfmGroup: "000",
            orderstatus: "finished", //最近一張訂單的status
            Email: "user5@gmail.com",
        },
    ];
    showOnTable(customers);
}

function showOnTable(customers) {
    const tbody = document.getElementById("output");
    tbody.innerHTML = "";
    console.log("clean");
    customers.forEach((customer) => {
        const newRow = document.createElement("tr");
        //button那行希望是帶去 orderListPage裡目前這位使用者的訂單的位置
        newRow.innerHTML = `
            <td>${customer.userId}</td>
            <td>${customer.rfmGroup}</td>
            <td>${customer.orderstatus}</td>
            <td><a href="orderListPage.html"><button value=${customer.userId}>前往</button></a></td>
            <td>${customer.Email}</td>`;
        tbody.appendChild(newRow);
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener("DOMContentLoaded", fetchCustomerData);
