function fetchCustomerData(){
   //在這裡抓資料

   //先放假資料

   /*
    分組順序[111,112,...,121,....,211,...,555]
    稱號順序{
        1:[111, 112, 113, 121, 122, 211, 212, 221, 222, 311, ], //最優先-忠誠核心客戶
        2:[114, 115, 123, 124, 125, 213, 214, 215, 223, 224, 225, 312, 313, 321, 322, 323, 411, 412, 511, 512, 521, 522,   ], //次優先-忠誠邊陲客戶
        3:[131, 132, 133, 134, 135, 141, 142, 151, 152, 231, 232, 233, 234, 235, 241, 242, 251, 252, 314, 315, 324, 325, 331, 332, 333, 334, 335, 413, 421, 422, 431, 432, 523, 531, 532,], //一般-穩定客戶
        4:[143, 144, 145, 153, 154, 155, 243, 244, 245, 253, 254, 255, 341, 342, 351, 352, 414, 415, 423, 424, 425, 433, 434, 435, 441, 442, 443, 444, 445, 513, 514, 515, 524, 525, ], //次延後-低價值非活躍客戶 
        5:[343, 344, 345, 353, 354, 355, 451, 452, 453, 454, 455, 533, 534, 535,541, 542, 543, 544, 545, 551, 552, 553, 554, 555 ] //最延後-流失或無價值客戶
    }
    呈現的時候sort by 稱號, 
    其中1是最近期/最頻繁/花最多錢的
    時間夠的話會回來為各組加不同的表格底色
    */

    var customers=[
        {
            "userId":"User#5",
            "recency":"2024-12-21 11:09",
            "frequency":"2",
            "monetaryValue":"9,345",
            "rfmGroup":"最優先-忠誠核心客戶",
            "color":"red"
        },
        {
            "userId":"User#3",
            "recency":"2024-11-09 09:34",
            "frequency":"0",
            "monetaryValue":"6,943",
            "rfmGroup":"次優先-忠誠邊陲客戶",
            "color":"orange"
        },
        {
            "userId":"User#4",
            "recency":"2024-10-11 14:23",
            "frequency":"0",
            "monetaryValue":"3,234",
            "rfmGroup":"一般-穩定客戶",
            "color":"yellow"
        },
        {
            "userId":"User#1",
            "recency":"2024-09-27 17:32",
            "frequency":"0",
            "monetaryValue":"1,654",
            "rfmGroup":"次延後-低價值非活躍客戶",
            "color":"green"
        },
        {
            "userId":"User#2",
            "recency":"2024-09-04 10:54",
            "frequency":"0",
            "monetaryValue":"543",
            "rfmGroup":"最延後-流失或無價值客戶",
            "color":"gray"
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
            newRow.setAttribute("class",customer.color);
            tbody.appendChild(newRow);
        
    });
    console.log("push");
}
// 瀏覽器載入時呼叫
document.addEventListener('DOMContentLoaded', fetchCustomerData);