async function fetchCustomerOrders() {
    const token = sessionStorage.getItem("token"); // 從 session 中獲取登入時存的 token

    try {
        // 向後端發送請求，帶上 JWT token
        const response = await fetch('http://127.0.0.1:8000/orders', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // 設置 Authorization 標頭
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error(`錯誤代碼: ${response.status}`);
        }

        const orders = await response.json(); // 解析回傳的 JSON 訂單資料
        showOnTable(orders); // 將訂單資料渲染到頁面表格中
    } catch (error) {
        console.error("無法獲取訂單資料:", error);
    }
}
   /* //先放假資料
   var orders=[
        {
            "userId":"User#5",//呈現的時候同使用者的放一起, Group by userId
            "id":"Order#18",
            "status":"confirmed",
            "color":"red",//因為訂單狀態=confirmed
            "DDL":"2025-03-21 12:00",//處理過的 2023-11-01T22:00:00Z,呈現的時候以DDL近到遠排序
            "productInfo":[["LaptopC","1000"],["LaptopB","2000"]],
            "orderProfit":"532" //加總整單的產品售價-成本
        },
        {
            "userId":"User#3",//呈現的時候同使用者的放一起, Group by userId
            "id":"Order#17",
            "status":"processing",
            "color":"green",//因為訂單狀態=processing
            "DDL":"2025-02-09 12:00",//處理過的 2023-11-01T22:00:00Z,呈現的時候以DDL近到遠排序
            "productInfo":[["ServerA","90"],["ServerD","150"]],
            "orderProfit":"267" //加總整單的產品售價-成本
        },
        {
            "userId":"User#5",//呈現的時候同使用者的放一起, Group by userId
            "id":"Order#16",
            "status":"finished",
            "color":"gray",//因為訂單狀態=finished
            "DDL":"2024-12-09 12:00",//處理過的 2023-11-01T22:00:00Z,呈現的時候以DDL近到遠排序
            "productInfo":[["LaptopC","1000"],["LaptopB","2000"]],
            "orderProfit":"532" //加總整單的產品售價-成本
        }
    ];
    showOnTable(orders);
} */

function showOnTable(orders){
    const tbody=document.getElementById('output');
    tbody.innerHTML="";
    console.log("clean");
    orders.forEach(order => {
        //將前五筆資料加入表格
        const newRow =document.createElement('tr');
        newRow.innerHTML=`
            <td>${order.userId}</td>
            <td>${order.id}</td>
            <td>${order.status}</td>
            <td>${order.DDL}</td>
            <td>${order.orderProfit}</td>`;

        //將訂單詳情加入每橫列的最後一格
        const newTd=document.createElement('td');
        newTd.innerHTML=`
            <tbody>
            </tbody>
        `;
        order.productInfo.forEach(info =>{
            const newRow2 =document.createElement('tbody');
            newRow2.innerHTML=`
                <tr>
                    <td>${info[0]}</td>
                    <td>${info[1]}</td>  
                </tr>
            `;
            newTd.appendChild(newRow2);
        });
        newRow.appendChild(newTd);
        newRow.setAttribute("class",order.color);
        tbody.appendChild(newRow);
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchCustomerData);