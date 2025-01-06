function fetchProductData(){
    //在這裡抓資料
    //先放假資料
    var productDatas=[
        {
            "productId":"ServerA",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[1, 10, 15, 25, 5, 15, 10, 5, 1],//這個在設計資料結構的時候漏了要補
            "forcastDemand":"15",//= 從訂單列表中撈最近三個月的每月平均訂購量
            "safeLevel":"8",// =z*forcastDemand*0.1 ，設需求呈常態分布，服務水準為95%
            "reOrderPoint":"12"//＝forcastDemand*(leadTime/30)+safeLevel
        },
        {
            "productId":"ServerB",
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期'],
            "inventoryLevel":[10, 20, 15, 10, 5, 25, 15, 5, 10],
            "forcastDemand":"10",
            "safeLevel":"5",
            "reOrderPoint":"10"
        }
    ];
   showOnTable(productDatas);
}
function showOnTable(productDatas){
    const charts = document.getElementById('charts');
    productDatas.forEach(productData=>{
        //長條圖
        const chartElement=document.createElement('canvas');
        const newChart= new Chart(chartElement, {
            type: 'bar',
            data: {
                labels:productData.times,
                datasets: [{
                    label: productData.productId,
                    data:productData.inventoryLevel ,
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
                                        <th>預期需求（台/月）</th>
                                        <th>安全存量</th>
                                        <th>再訂購點</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>${productData.forcastDemand}</td>
                                        <td>${productData.safeLevel}</td>
                                        <td>${productData.reOrderPoint}</td>
                                    </tr>
                                </tbody>
                            </table>
        `;
        table.setAttribute("class","product-table ");
        charts.appendChild(table); 
        
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchProductData);
/* 
    try {
        // 调用后端 API 获取产品的九期库存数据
        const response = await fetch('http://127.0.0.1:8000/get-products-data');
        const productLevels = await response.json();

        // 渲染表格和图表
        showOnTable(productLevels);
    } catch (error) {
        console.error("Error fetching product data:", error);
    } */