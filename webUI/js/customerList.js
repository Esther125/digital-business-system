async function fetchCustomerData() {
    try {
        // 呼叫後端 API 獲取客戶數據
        const response = await fetch('http://127.0.0.1:8000/api/customers');
        const data = await response.json();
        showOnTable(data.customers);
    } catch (error) {
        console.error("Failed to fetch customer data:", error);
    }
}

function showOnTable(customers) {
    const tbody = document.getElementById('output');
    tbody.innerHTML = ""; // 清空表格內容
    console.log("clean");

    customers.forEach(customer => {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${customer.userId}</td>
            <td>${customer.rfmGroup}</td>
            <td>${customer.orderstatus}</td>
            <td>
                <a href="/orderListPage?userId=${customer.userId}">
                    <button>前往</button>
                </a>
            </td>
            <td>${customer.Email}</td>`;
        newRow.setAttribute("class", customer.color);
        tbody.appendChild(newRow);
    });

    console.log("push");
}

// 瀏覽器載入時觸發
document.addEventListener('DOMContentLoaded', fetchCustomerData);
