function fetchComponentData(){
    //在這裡抓資料
    //先放假資料
    var componentDatas=[
        {
            "id":"Component#1",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[1, 10, 15, 25, 5, 15, 10, 5, 1],//這個要想一下怎麼撈往期的資料
            "forcastDemand":"15",//= SUM（從訂單列表中撈需要它的產品們最近三個月的每月平均訂購量*BOM裡各自的零件需求）
            "safeLevel":"8",// =z*forcastDemand*0.1 ，設需求呈常態分布，服務水準為95%
            "reOrderPoint":"12"//＝forcastDemand*(leadTime/30)+safeLevel
        },
        {
            "id":"Component#2",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[10, 20, 15, 10, 5, 25, 15, 5, 10],
            "forcastDemand":"10",
            "safeLevel":"5",
            "reOrderPoint":"10"
        }
    ];
   showOnTable(componentDatas);
}
function showOnTable(componentDatas){
    const charts = document.getElementById('charts');

    componentDatas.forEach(componentData=>{
        //長條圖
        const chartElement=document.createElement('canvas');
        const newChart= new Chart(chartElement, {
            type: 'bar',
            data: {
                labels:componentData.times,
                datasets: [{
                    label: componentData.id,
                    data:componentData.inventoryLevel ,
                }]
            }
        })
        charts.appendChild(chartElement);

        //table
        const table=document.createElement('table');
        table.innerHTML=`
            <table>
                                <thead>
                                    <tr>
                                        <th>預期需求（個/月）</th>
                                        <th>安全存量</th>
                                        <th>再訂購點</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>${componentData.forcastDemand}</td>
                                        <td>${componentData.safeLevel}</td>
                                        <td>${componentData.reOrderPoint}</td>
                                    </tr>
                                </tbody>
                            </table>
        `;
        table.setAttribute("class","component-table ");
        charts.appendChild(table); 
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchComponentData);
/* 
    try {
        // 调用后端 API 获取所有组件的九期库存数据
        const response = await fetch('http://127.0.0.1:8000/get-components-data');
        const componentLevels = await response.json();

        // 渲染表格和图表
        showOnTable(componentLevels);
    } catch (error) {
        console.error("Error fetching component data:", error);
    } */