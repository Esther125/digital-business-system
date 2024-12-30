function fetchCustomerData(){
   //在這裡抓資料

   //先放假資料
   var customers=[
        {
            "userId":"User#5",
            "recency":"0",
            "frequency":"0",
            "monetaryValue":"0",
            "rfmGroup":"0"
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