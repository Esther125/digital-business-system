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
def get_all_orders_grouped_by_customer():
    try:
        # 獲取所有訂單
        response = sysdata_table.scan()
        orders = response.get("Items", [])

        if not orders:
            raise HTTPException(status_code=404, detail="未找到訂單數據")

        # 分組訂單
        grouped_orders = {}
        for order in orders:
            buyer = order.get("buyer", "Unknown")  # 如果缺少 buyer，設置為 Unknown
            formatted_order = {
                "orderId": order.get("id", "N/A"),
                "status": order.get("status", "N/A"),
                "deadline": order.get("DDL", "N/A"),
                "products": order.get("productCollection", "N/A"),
            }

            # 分組
            if buyer not in grouped_orders:
                grouped_orders[buyer] = []
            grouped_orders[buyer].append(formatted_order)

        return grouped_orders

    except Exception as e:
        print(f"取得訂單資料時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail="無法取得訂單資料")
