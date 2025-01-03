function fetchBomData(){
    //在這裡抓資料
    /* const response = await fetch('http://127.0.0.1:8000/api/get-bom', {  // 使用 API 路径
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product: "Product#6" }) // 替换为实际产品 ID
    });

    const data = await response.json();
    const boms = data.boms || [];
    showOnTable(boms); */
    //先放假資料
    var boms=[
        {
            "productId":"LaptopA",
            "componentId":"",
            "componentAmount":"",
            "forcastDemand":"0",//產品的，用算的
            "leadTime":"0"//產品的
        },
        {
            "productId":"",
            "componentId":"Component#1",
            "componentAmount":"2",
            "forcastDemand":"0",//零件的，用算的
            "leadTime":"0"//零件的，資料庫設計的時候漏了要補，零件存貨會用到
        }
    ];
   showOnTable(boms);
}
function showOnTable(boms){
    const tbody=document.getElementById('output');
    tbody.innerHTML="";
    console.log("clean");
    boms.forEach(bom => {
        const newRow =document.createElement('tr');    
        newRow.innerHTML=`
            <td>${bom.productId}</td>
            <td>${bom.componentId}</td>
            <td>${bom.componentAmount}</td>
            <td>${bom.forcastDemand}</td>
            <td>${bom.leadTime}</td>`;
            tbody.appendChild(newRow);
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchBomData);
