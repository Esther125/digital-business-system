async function fetchCustomerData() {
    try {
        // 呼叫後端 API 獲取客戶數據
        const response = await fetch(
            `${window.ENV_CONFIG.BASE_URL}/api/customers`
        );
        const data = await response.json();
        showOnTable(data.customers);
    } catch (error) {
        console.error("Failed to fetch customer data:", error);
    }
}

function showOnTable(customers) {
    const tbody = document.getElementById("output");
    tbody.innerHTML = ""; // 清空表格內容

    // 定義 RFM 分組的排序優先級
    const rfmPriority = {
        "最優先-忠誠核心客戶": 1,
        "次優先-忠誠邊陲客戶": 2,
        "一般-穩定客戶": 3,
        "次延後-低價值非活躍客戶": 4,
        "最延後-流失或無價值客戶": 5,
    };

    // 定義 RFM 分組對應的顏色
    const rfmClassMapping = {
        "最優先-忠誠核心客戶": "red",
        "次優先-忠誠邊陲客戶": "orange",
        "一般-穩定客戶": "yellow",
        "次延後-低價值非活躍客戶": "green",
        "最延後-流失或無價值客戶": "gray",
    };

    // 如果後端返回的是數字 RFM 分組，轉換為描述
    customers.forEach((customer) => {
        switch (customer.rfmGroup) {
            case "1":
                customer.rfmGroup = "最優先-忠誠核心客戶";
                break;
            case "2":
                customer.rfmGroup = "次優先-忠誠邊陲客戶";
                break;
            case "3":
                customer.rfmGroup = "一般-穩定客戶";
                break;
            case "4":
                customer.rfmGroup = "次延後-低價值非活躍客戶";
                break;
            case "5":
                customer.rfmGroup = "最延後-流失或無價值客戶";
                break;
        }
    });

    // 按照 RFM 分組排序
    customers.sort((a, b) => rfmPriority[a.rfmGroup] - rfmPriority[b.rfmGroup]);

    // 渲染表格
    customers.forEach((customer) => {
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>${customer.userId}</td>
            <td>${customer.rfmGroup}</td>
            <td>${customer.orderstatus}</td>
            <td>
                <a href="/orderListPage?userId=${customer.userId}">
                    <button>前往</button>
                </a>
            </td>
            <td>${customer.Email}</td>`;

        // 根據 RFM 等級分組設置行的顏色
        const rfmClass = rfmClassMapping[customer.rfmGroup] || "gray"; // 預設為灰色
        newRow.classList.add(rfmClass);

        tbody.appendChild(newRow);
    });

    console.log("Table rendered with RFM group sorting and colors.");
}

// 瀏覽器載入時觸發
document.addEventListener("DOMContentLoaded", fetchCustomerData);
