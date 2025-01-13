async function fetchOrders(customerId = "") {
    try {
        // 動態生成 API URL
        const url = customerId ? `/api/orders?customerId=${customerId}` : "/api/orders";

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

// 更新下拉選單的監聽邏輯
document.getElementById('userFilter').addEventListener('change', function(event) {
    const selectedCustomer = event.target.value; // 獲取選擇的客戶
    fetchOrders(selectedCustomer); // 發送 API 請求
});
