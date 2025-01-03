async function fetchBomData(){
    //在這裡抓資料
    const response = await fetch('http://127.0.0.1:8000/get-bom', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product: "Product#6" }) // 修改为实际产品 ID
    });

    const data = await response.json();
    const boms = data.boms || []; // 获取后端返回的 BOM 数据

    showOnTable(boms);
    //先放假資料
    var boms_test=[
        {
            "productId":"LaptopA",//呈現的時候 Group by productId
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
        },
        {
            "productId":"LaptopA",//呈現的時候 Group by productId
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

function showOnTable(boms) {
    const tbody = document.getElementById('output');
    tbody.innerHTML = ""; // 清空表格内容
    console.log("Table cleared");

    // 遍历 BOM 数据并填充表格
    boms.forEach(bom => {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${bom.productId || ''}</td>
            <td>${bom.componentId || ''}</td>
            <td>${bom.componentAmount || ''}</td>
            <td>${bom.forcastDemand || ''}</td>
            <td>${bom.leadTime || ''}</td>`;
        tbody.appendChild(newRow);
    });
    console.log("Table updated");
}

// 页面加载时调用 fetchBomData
document.addEventListener('DOMContentLoaded', fetchBomData);