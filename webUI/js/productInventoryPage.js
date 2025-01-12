async function fetchProductData() {
    try {
        // 呼叫後端 API 獲取產品數據
        const response = await fetch('http://127.0.0.1:8000/api/product-inventory/get-products-data');
        const data = await response.json();
        showOnTable(data.products);
    } catch (error) {
        console.error("Failed to fetch product data:", error);
    }
}

function showOnTable(productDatas) {
    const charts = document.getElementById('charts');
    charts.innerHTML = ""; // 清空圖表區域

    productDatas.forEach(productData => {
        // 渲染長條圖
        const chartElement = document.createElement('canvas');
        const newChart = new Chart(chartElement, {
            type: 'bar',
            data: {
                labels: productData.times,
                datasets: [{
                    label: productData.productId,
                    data: productData.inventoryLevel,
                }]
            }
        });
        charts.appendChild(chartElement);

        // 渲染表格
        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>產品 ID</th>
                    <th>預期需求（台/月）</th>
                    <th>安全存量</th>
                    <th>再訂購點</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${productData.productId}</td>
                    <td>${productData.forecastDemand}</td>
                    <td>${productData.safeLevel}</td>
                    <td>${productData.reOrderPoint}</td>
                </tr>
            </tbody>
        `;
        table.setAttribute("class", "product-table");
        charts.appendChild(table);
    });

    console.log("Data rendered successfully.");
}

// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchProductData);
