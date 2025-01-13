from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict
from boto3.dynamodb.conditions import Key
import boto3
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

router = APIRouter()

# 配置 DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-northeast-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
sysdata_table = dynamodb.Table("sysdata")

STATUS_COLORS = {
    "confirmed": "red",
    "processing": "green",
    "finished": "gray",
}


@router.get("/orders", response_model=Dict[str, List[Dict]])
def get_all_orders_grouped_by_customer(customerId: str = Query(None, description="客戶編號, 如 Customer#1")):
    try:
        # 獲取所有訂單
        response = sysdata_table.scan()
        orders = response.get("Items", [])

        if not orders:
            raise HTTPException(status_code=404, detail="未找到訂單數據")

        # 只允許的顧客編號
        allowed_customers = [f"Customer#{i}" for i in range(1, 6)]

        # 分組訂單
        grouped_orders = {customer: [] for customer in allowed_customers}

        for order in orders:
            # 提取 buyer
            buyer = order.get("buyer", "Unknown")

            # 過濾不在範圍內的顧客
            if buyer not in allowed_customers:
                continue

            # 提取 ProductCollection 的詳細內容
            products_collection_id = order.get("productCollection", "N/A")
            detailed_products = []
            revenue = 0  # 初始化 revenue

            if products_collection_id.startswith("ProductCollection#"):
                # 查詢 ProductCollection 中的產品
                product_collection_data = sysdata_table.get_item(Key={"id": products_collection_id}).get("Item", {})
                products = product_collection_data.get("products", [])

                # 遍歷 products 列表，生成詳細內容並計算 revenue
                for product in products:
                    product_id = product.get("productId")
                    product_amount = product.get("productAmount", 0)

                    if product_id:
                        # 查詢產品價格
                        product_data = sysdata_table.get_item(Key={"id": product_id}).get("Item", {})
                        product_price = product_data.get("price", 0)

                        # 累加 revenue
                        revenue += product_amount * product_price

                        # 添加詳細產品內容
                        detailed_products.append({
                            "productName": product_data.get("productId", "Unknown"),
                            "amount": product_amount
                        })

            # 格式化訂單資料
            formatted_order = {
                "orderId": order.get("id", "N/A"),
                "status": order.get("status", "N/A"),
                "deadline": order.get("DDL", "N/A"),
                "revenue": revenue,  # 計算出的 revenue
                "products": detailed_products,  # 更新 products 為詳細產品內容
            }

            # 添加到對應的顧客分組
            grouped_orders[buyer].append(formatted_order)

        # 如果客戶編號為空，返回所有數據
        if not customerId:
            return grouped_orders

        # 如果指定了客戶編號，只返回該客戶的數據
        if customerId in grouped_orders:
            return {customerId: grouped_orders[customerId]}

        # 如果客戶編號無效，返回空數據
        return {}

    except Exception as e:
        print(f"取得訂單資料時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail="無法取得訂單資料")
