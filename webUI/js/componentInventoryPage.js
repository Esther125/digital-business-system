async function fetchComponentData(){
    //在這裡抓資料
    try {
        // 调用后端 API 获取所有组件的九期库存数据
        const response = await fetch('http://127.0.0.1:8000/get-components-data');
        const componentLevels = await response.json();

        // 渲染表格和图表
        showOnTable(componentLevels);
    } catch (error) {
        console.error("Error fetching component data:", error);
    }
    //先放假資料
    var componentLevels=[
        {
            "id":"Component#1",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[1, 10, 15, 25, 5, 15, 10, 5, 1]//這個要想一下怎麼撈往期的資料
        },
        {
            "id":"Component#2",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[10, 20, 15, 10, 5, 25, 15, 5, 10]
        }
    ];
   showOnTable(componentLevels);
}

function showOnTable(componentLevels) {
    const charts = document.getElementById('charts');
    charts.innerHTML = ""; // 清空之前的图表

    componentLevels.forEach(componentLevel => {
        const chartElement = document.createElement('canvas');
        const newChart = new Chart(chartElement, {
            type: 'bar',
            data: {
                labels: componentLevel.times,
                datasets: [{
                    label: componentLevel.id,
                    data: componentLevel.inventoryLevel,
                }]
            }
        });
        charts.appendChild(chartElement);
    });
    console.log("Charts updated");
}