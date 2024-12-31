function fetchCustomerData(){
   //在這裡抓資料

   //先放假資料
   var orders=[
        {
            "userId":"User#5",
            "id":"Order#18",
            "status":"confirmed",
            "DDL":"2023-11-01 00:00",//處理過的 2023-11-01T22:00:00Z
            "productInfo":[["LaptopC","1"],["LaptopB","2"]],
            "orderProfit":"300" //加總整單的產品售價-成本
        }
    ];
    showOnTable(orders);
}

function showOnTable(orders){
    const tbody=document.getElementById('output');
    tbody.innerHTML="";
    console.log("clean");
    orders.forEach(order => {
        //將前五筆資料加入表格
        const newRow =document.createElement('tr');
        newRow.innerHTML=`
            <td>${order.userId}</td>
            <td>${order.id}</td>
            <td>${order.status}</td>
            <td>${order.DDL}</td>
            <td>${order.orderProfit}</td>`;

        //將訂單詳情加入每橫列的最後一格
        const newTd=document.createElement('td');
        newTd.innerHTML=`
            <tbody>
            </tbody>
        `;
        order.productInfo.forEach(info =>{
            const newRow2 =document.createElement('tbody');
            newRow2.innerHTML=`
                <tr>
                    <td>${info[0]}</td>
                    <td>${info[1]}</td>  
                </tr>
            `;
            newTd.appendChild(newRow2);
        });
        newRow.appendChild(newTd);

        tbody.appendChild(newRow);
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchCustomerData);