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
def get_orders_grouped_by_user(userId: str = Query(default=None)):
    try:
        # 查詢 customer 表以找到 buyer
        buyer = None
        if userId:
            # 假設 customer 表的 Partition Key 是 id，並存儲 userId
            customer_response = sysdata_table.get_item(Key={"id": f"Customer#{userId}"})
            if "Item" in customer_response:
                buyer = customer_response["Item"].get("buyer", None)
                if not buyer:
                    raise HTTPException(status_code=404, detail=f"未找到與 userId {userId} 對應的 buyer")
            else:
                raise HTTPException(status_code=404, detail=f"未找到 userId {userId} 的客戶資料")

        # 根據 buyer 查詢訂單
        if buyer:
            response = sysdata_table.query(
                IndexName="buyer-index",  # 指定 GSI 名稱
                KeyConditionExpression=Key("buyer").eq(buyer)
            )
        else:
            response = sysdata_table.scan()

        orders = response.get("Items", [])
        if not orders:
            raise HTTPException(status_code=404, detail="未找到訂單數據")

        # 分組訂單
        grouped_orders = {}
        for order in orders:
            user_id = order.get("buyer", "Unknown")
            product_collection_id = order.get("productCollection", None)

            product_info = []
            if product_collection_id:
                try:
                    # 查詢產品集合
                    product_response = sysdata_table.get_item(Key={"id": product_collection_id})
                    if "Item" not in product_response:
                        continue
                    products = product_response["Item"].get("products", [])
                    product_info = [
                        {"productId": p["productId"], "amount": p["productAmount"]} for p in products
                    ]
                except Exception as e:
                    print(f"查詢產品集合時發生錯誤: {e}")
                    continue

            formatted_order = {
                "userId": user_id,
                "id": order.get("id", "N/A"),
                "status": order.get("status", "N/A"),
                "color": STATUS_COLORS.get(order.get("status"), "gray"),
                "DDL": order.get("DDL", "N/A"),
                "productInfo": product_info,
            }

            if user_id not in grouped_orders:
                grouped_orders[user_id] = []
            grouped_orders[user_id].append(formatted_order)

        return grouped_orders

    except Exception as e:
        print(f"取得訂單資料時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail="無法取得訂單資料")

