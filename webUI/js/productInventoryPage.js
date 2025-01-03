async function fetchProductData(){
    //在這裡抓資料
    try {
        // 调用后端 API 获取产品的九期库存数据
        const response = await fetch('http://127.0.0.1:8000/get-products-data');
        const productLevels = await response.json();

        // 渲染表格和图表
        showOnTable(productLevels);
    } catch (error) {
        console.error("Error fetching product data:", error);
    }
    //先放假資料
    var productLevels_test=[
        {
            "productId":"ServerA",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[1, 10, 15, 25, 5, 15, 10, 5, 1]//這個在設計資料結構的時候漏了要補
        },
        {
            "productId":"ServerB",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[10, 20, 15, 10, 5, 25, 15, 5, 10]
        }
    ];
}

function showOnTable(productLevels) {
    const charts = document.getElementById('charts');
    charts.innerHTML = ""; // 清空之前的图表

    productLevels.forEach(productLevel => {
        const chartElement = document.createElement('canvas');
        const newChart = new Chart(chartElement, {
            type: 'bar',
            data: {
                labels: productLevel.times,
                datasets: [{
                    label: productLevel.productId,
                    data: productLevel.inventoryLevel,
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
        charts.appendChild(chartElement);
    });
    console.log("Charts updated");
}

// 页面加载时调用 fetchProductData
document.addEventListener('DOMContentLoaded', fetchProductData);