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

        // 創建圖表容器
        const chartWrapper = document.createElement('div');
        chartWrapper.className = "chart-wrapper";

        // 創建 Canvas 元素
        const chartElement = document.createElement('canvas');

        // 使用 Chart.js 渲染長條圖
        new Chart(chartElement, {
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

        // 創建表格
        const tableElement = document.createElement('table');
        tableElement.className = "component-table";
        tableElement.innerHTML = `
            <thead>
                <tr>
                    <th>Expected Demand</th>
                    <th>Safety Stock</th>
                    <th>Reorder Point</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${componentData.expectedDemand}</td>
                    <td>${componentData.safetyStock}</td>
                    <td>${componentData.reorderPoint}</td>
                </tr>
            </tbody>
        `;

        // 添加圖表與表格
        chartWrapper.appendChild(chartElement);
        chartWrapper.appendChild(tableElement);

        // 添加至主區域
        chartsContainer.appendChild(chartWrapper);
    });

    console.log("Component charts and updated tables rendered successfully.");
}


// 瀏覽器載入時觸發
document.addEventListener('DOMContentLoaded', fetchComponentData);
