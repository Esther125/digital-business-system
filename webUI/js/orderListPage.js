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

function showOnTable(orders) {
    const tbody = document.getElementById('output');
    tbody.innerHTML = ""; // 清空表格內容
    console.log("clean");

    // 按用戶分組顯示
    const groupedOrders = orders.reduce((acc, order) => {
        acc[order.userId] = acc[order.userId] || [];
        acc[order.userId].push(order);
        return acc;
    }, {});

    Object.keys(groupedOrders).forEach(userId => {
        const userOrders = groupedOrders[userId];

        // 插入用戶標題行
        const userRow = document.createElement('tr');
        userRow.innerHTML = `<td colspan="6"><strong>客戶: ${userId}</strong></td>`;
        tbody.appendChild(userRow);

        // 插入用戶的訂單數據
        userOrders.forEach(order => {
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${order.userId}</td>
                <td>${order.id}</td>
                <td>${order.status}</td>
                <td>${order.DDL}</td>
                <td>${order.orderProfit}</td>`;

            // 插入產品詳情
            const productTd = document.createElement('td');
            order.productInfo.forEach(info => {
                const productDetail = document.createElement('div');
                productDetail.textContent = `產品: ${info[0]}, 價格: ${info[1]}`;
                productTd.appendChild(productDetail);
            });

            newRow.appendChild(productTd);
            newRow.setAttribute("class", order.color);
            tbody.appendChild(newRow);
        });
    });

    console.log("push");
}

// 瀏覽器載入時觸發
document.addEventListener('DOMContentLoaded', fetchCustomerOrders);
