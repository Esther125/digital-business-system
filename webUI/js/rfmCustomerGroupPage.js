async function fetchCustomerData() {
    try {
        // 呼叫後端 API 獲取 RFM 數據
        const response = await fetch(
            `${window.ENV_CONFIG.BASE_URL}/api/rfm-customers`
        );
        const data = await response.json();
        showOnTable(data.customers);
    } catch (error) {
        console.error("Failed to fetch RFM customer data:", error);
    }
}

function showOnTable(customers) {
    const tbody = document.getElementById("output");
    tbody.innerHTML = ""; // 清空表格內容
    console.log("clean");

    // 過濾無效數據並排序
    customers
        .filter((customer) => customer.rfmGroup !== "未知分組")
        .sort((a, b) => a.rfmGroup.localeCompare(b.rfmGroup)) // 按分組排序
        .reverse() // 顛倒順序
        .forEach((customer) => {
            const newRow = document.createElement("tr");
            newRow.innerHTML = `
                <td>${customer.userId}</td>
                <td>${customer.recency}</td>
                <td>${customer.frequency}</td>
                <td>${customer.monetaryValue}</td>
                <td>${customer.rfmGroup}</td>`;
            newRow.setAttribute("class", customer.color); // 分組顏色
            tbody.appendChild(newRow);
        });

    console.log("push");
}

// 瀏覽器載入時觸發
document.addEventListener("DOMContentLoaded", fetchCustomerData);
