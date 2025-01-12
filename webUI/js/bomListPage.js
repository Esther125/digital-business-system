async function fetchBomData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/get-bom', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const boms = data.boms || [];
        showOnTable(boms);
    } catch (error) {
        console.error("Fetch BOM data failed:", error);
    }
}

function showOnTable(boms) {
    const tbody = document.getElementById('output');
    tbody.innerHTML = ""; // 清空表格

    boms.forEach(bom => {
        // 顯示 Product 行
        const productRow = document.createElement('tr');
        productRow.innerHTML = `
            <td>${bom.productId}</td>
            <td></td> <!-- 空白 Component -->
            <td>${bom.currentQuantity}</td>
            <td>${bom.forecastDemand}</td>
            <td>${bom.leadTime}</td>
        `;
        tbody.appendChild(productRow);

        // 顯示對應的 Component 行
        if (bom.components.length === 0) {
            const noComponentRow = document.createElement('tr');
            noComponentRow.innerHTML = `
                <td></td>
                <td>No Components</td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
            `;
            tbody.appendChild(noComponentRow);
        } else {
            bom.components.forEach(component => {
                const componentRow = document.createElement('tr');
                componentRow.innerHTML = `
                    <td></td> <!-- 空白 Product -->
                    <td>${component.componentId}</td>
                    <td>${component.inventoryLevel}</td>
                    <td>${component.forcastDemand}</td>
                    <td>${component.leadTime}</td>
                `;
                tbody.appendChild(componentRow);
            });
        }
    });
}

// 瀏覽器載入時自動執行
document.addEventListener('DOMContentLoaded', fetchBomData);
