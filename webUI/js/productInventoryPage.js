async function fetchProductData() {
    try {
        // 調用後端 API 獲取產品數據
        const response = await fetch('http://127.0.0.1:8000/api/product-inventory/get-products-data');
        const data = await response.json();
        renderCharts(data.products);
    } catch (error) {
        console.error("Failed to fetch product data:", error);
    }
}

function renderCharts(productDatas) {
    const chartsContainer = document.getElementById('charts');
    chartsContainer.innerHTML = ""; // 清空圖表區域

    productDatas.forEach(productData => {
        // 創建 Canvas 元素
        const chartElement = document.createElement('canvas');

        // 使用 Chart.js 渲染長條圖
        const newChart = new Chart(chartElement, {
            type: 'bar',
            data: {
                labels: productData.times,
                datasets: [{
                    label: productData.productId,
                    data: productData.inventoryLevel,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // 添加圖表到容器
        chartsContainer.appendChild(chartElement);
    });

    console.log("Charts rendered successfully.");
}

// 瀏覽器載入時觸發
document.addEventListener('DOMContentLoaded', fetchProductData);
