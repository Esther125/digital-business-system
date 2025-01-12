from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
import boto3
import os
from dotenv import load_dotenv
from src.service import get_current_user

# 載入環境變量
load_dotenv()

router = APIRouter()

# 配置 DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
table = dynamodb.Table("sysdata")

# 訂單狀態顏色映射
STATUS_COLORS = {
    "confirmed": "red",
    "processing": "green",
    "finished": "gray"
}

# API 路由：根據當前登入用戶提取訂單數據
@router.get("/orders", response_model=List[Dict])
def get_orders(current_user: str = Depends(get_current_user)):
    """
    根據目前登入的客戶 ID 篩選該客戶的訂單。
    """
    try:
        # 篩選 buyer 屬於當前使用者的訂單
        response = table.scan(
            FilterExpression="buyer = :customer",
            ExpressionAttributeValues={":customer": f"Customer#{current_user}"}
        )
        orders = response.get("Items", [])

        # 格式化數據
        formatted_orders = []
        for order in orders:
            product_info = order.get("productInfo", [])
            total_profit = sum([int(info[1]) for info in product_info])  # 計算訂單總利潤
            ddl = order.get("DDL", "N/A")
            formatted_orders.append({
                "userId": order.get("buyer", "N/A"),
                "id": order.get("id", "N/A"),
                "status": order.get("status", "N/A"),
                "color": STATUS_COLORS.get(order.get("status"), "gray"),
                "DDL": ddl,
                "productInfo": product_info,
                "orderProfit": total_profit
            })

        # 按 DDL (Deadline) 排序
        formatted_orders.sort(key=lambda x: x["DDL"])

        return formatted_orders
    except Exception as e:
        print(f"取得訂單資料時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail="無法取得訂單資料")
