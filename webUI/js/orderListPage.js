async function fetchOrders(customerId = "") {
    try {
        // 動態生成 API URL
        const url = customerId 
            ? `/api/orders?customerId=${encodeURIComponent(customerId)}`
            : "/api/orders";

        // 呼叫後端 API
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`獲取訂單失敗: ${response.statusText}`);
        }

        // 獲取分組訂單數據
        const groupedOrders = await response.json();
        renderOrders(groupedOrders);

        // 保存到全局變數以便篩選時使用
        window.groupedOrders = groupedOrders;
    } catch (error) {
        console.error('無法獲取訂單數據:', error);
    }
}

function renderOrders(groupedOrders) {
    const output = document.getElementById('output');
    output.innerHTML = ''; // 清空現有內容

    Object.keys(groupedOrders).forEach(customer => {
        const orders = groupedOrders[customer];
        orders.forEach(order => {
            const row = document.createElement('tr');

            // 根據訂單狀態設置行的 CSS 類名
            if (order.status === 'confirmed') {
                row.classList.add('red');
            } else if (order.status === 'processing') {
                row.classList.add('green');
            } else if (order.status === 'finished') {
                row.classList.add('gray');
            }

            // 顧客編號
            const customerCell = document.createElement('td');
            customerCell.textContent = customer;
            row.appendChild(customerCell);

            // 訂單編號
            const orderIdCell = document.createElement('td');
            orderIdCell.textContent = order.orderId;
            row.appendChild(orderIdCell);

            // 訂單狀態
            const statusCell = document.createElement('td');
            statusCell.textContent = order.status;
            row.appendChild(statusCell);

            // 訂單截止時間
            const deadlineCell = document.createElement('td');
            deadlineCell.textContent = order.deadline;
            row.appendChild(deadlineCell);

            // 預期收益
            const revenueCell = document.createElement('td');
            revenueCell.textContent = order.revenue;
            row.appendChild(revenueCell);

            // 訂單內容
            const productsCell = document.createElement('td');
            const productTable = document.createElement('table');
            order.products.forEach(product => {
                const productRow = document.createElement('tr');
                const productNameCell = document.createElement('td');
                productNameCell.textContent = product.productName;
                productRow.appendChild(productNameCell);

                const productAmountCell = document.createElement('td');
                productAmountCell.textContent = product.amount;
                productRow.appendChild(productAmountCell);

                productTable.appendChild(productRow);
            });
            productsCell.appendChild(productTable);
            row.appendChild(productsCell);

            // 添加行到表格
            output.appendChild(row);
        });
    });
}



// 更新下拉選單的監聽邏輯
document.getElementById('userFilter').addEventListener('change', function(event) {
    const selectedCustomer = event.target.value; // 獲取選擇的客戶
    fetchOrders(selectedCustomer); // 發送 API 請求
});
// 初始化顯示全部訂單
fetchOrders();
