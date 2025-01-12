async function fetchCustomerData() {
    try {
        // 呼叫後端 API 獲取客戶數據
        const response = await fetch('http://127.0.0.1:8000/api/customers');
        const data = await response.json();
        showOnTable(data.customers);
    } catch (error) {
        console.error("Failed to fetch customer data:", error);
    }
}
    /* //先放假資料
    var customers=[
         {
             "userId":"User#5",
             "rfmGroup":"最優先-忠誠核心客戶",
             "color":"red",
             "orderstatus":"confirmed",//最近一張訂單的status
             "Email":"user5@gmail.com"
         },
         {
             "userId":"User#3",
             "rfmGroup":"次優先-忠誠邊陲客戶",
             "color":"green",
             "orderstatus":"processing",//最近一張訂單的status
             "Email":"user3@gmail.com"
         },
         {
             "userId":"User#4",
             "rfmGroup":"一般-穩定客戶",
             "color":"gray",
             "orderstatus":"finished",//最近一張訂單的status
             "Email":"user4@gmail.com"
         },
         {
             "userId":"User#1",
             "rfmGroup":"次延後-低價值非活躍客戶",
             "color":"gray",
             "orderstatus":"finished",//最近一張訂單的status
             "Email":"user1@gmail.com"
         },
         {
             "userId":"User#2",
             "rfmGroup":"最延後-流失或無價值客戶",
             "color":"gray",
             "orderstatus":"finished",//最近一張訂單的status
             "Email":"user2@gmail.com"
         }
     ];
     showOnTable(customers);
 } */
 
 function showOnTable(customers){
     const tbody=document.getElementById('output');
     tbody.innerHTML="";
     console.log("clean");
     customers.forEach(customer => {
         const newRow =document.createElement('tr');
         //button那行希望是帶去 orderListPage裡目前這位使用者的訂單的位置   
         newRow.innerHTML=`
             <td>${customer.userId}</td>
             <td>${customer.rfmGroup}</td>
             <td>${customer.orderstatus}</td>
             <td><a href="/orderListPage"><button value=${customer.userId}>前往</button></a></td>
             <td>${customer.Email}</td>`;
             newRow.setAttribute("class",customer.color);
             tbody.appendChild(newRow);
     });
     console.log("push");
 }
 // 瀏覽器載入時呼叫
 document.addEventListener('DOMContentLoaded', fetchCustomerData);