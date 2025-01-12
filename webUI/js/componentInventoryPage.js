async function fetchComponentData() {
    try {
        // 呼叫後端 API 獲取組件數據
        const response = await fetch('http://127.0.0.1:8000/api/component-inventory/get-components-data');
        const data = await response.json();
        renderComponentCharts(data.components);
    } catch (error) {
        console.error("Failed to fetch component data:", error);
    }
}

function renderComponentCharts(componentDatas) {
    const chartsContainer = document.getElementById('charts');
    chartsContainer.innerHTML = ""; // 清空圖表區域

    componentDatas.forEach(componentData => {
        // 過濾數據：不顯示 inventoryLevel 全為 0 的組件
        if (!componentData.inventoryLevel || componentData.inventoryLevel.every(level => level === 0)) {
            return;
        }

        // 創建 Canvas 元素
        const chartElement = document.createElement('canvas');

        // 使用 Chart.js 渲染長條圖
        const newChart = new Chart(chartElement, {
            type: 'bar',
            data: {
                labels: componentData.times,
                datasets: [{
                    label: componentData.id,
                    data: componentData.inventoryLevel,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
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

    console.log("Component charts rendered successfully.");
}

// 瀏覽器載入時觸發
document.addEventListener('DOMContentLoaded', fetchComponentData);
