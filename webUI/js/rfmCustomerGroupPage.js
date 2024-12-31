function fetchCustomerData(){
   //在這裡抓資料

   //先放假資料
   var customers=[
        {
            "userId":"User#5",
            "recency":"2023-11-01 00:00",
            "frequency":"0",
            "monetaryValue":"0",
            "rfmGroup":"000"
            //呈現的時候sort by rfmGroup, [111,112,...,121,....,211,...,555]
            //其中1是最近期/最頻繁/花最多錢的
            //依據r=1~5分五組分配不同的稱號[“最優先”,"次優先","一般","次延後","最延後"]
            //時間夠的話會回來為各組加不同的表格底色
        }
    ];
    showOnTable(customers);
}

function showOnTable(customers){
    const tbody=document.getElementById('output');
    tbody.innerHTML="";
    console.log("clean");
    customers.forEach(customer => {
        const newRow =document.createElement('tr');    
        newRow.innerHTML=`
            <td>${customer.userId}</td>
            <td>${customer.recency}</td>
            <td>${customer.frequency}</td>
            <td>${customer.monetaryValue}</td>
            <td>${customer.rfmGroup}</td>`;
            tbody.appendChild(newRow);
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchCustomerData);