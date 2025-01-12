from fastapi import APIRouter, HTTPException
import boto3
import os
from dotenv import load_dotenv
from typing import List, Dict

# 載入環境變數
load_dotenv()

# 初始化 FastAPI 路由
router = APIRouter()

# 配置 DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# 指定表名
table_name = "sysdata"
table = dynamodb.Table(table_name)

# 從 DynamoDB 提取所有客戶數據
def fetch_customers() -> List[Dict]:
    try:
        response = table.scan(
            FilterExpression="begins_with(id, :prefix)",
            ExpressionAttributeValues={":prefix": "Customer"}
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return []

# API 路由：返回客戶數據
@router.get("/customers")
def get_customers():
    """
    獲取所有客戶數據
    """
    customers = fetch_customers()
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    
    # 格式化數據以便前端使用
    formatted_customers = [
        {
            "userId": customer.get("userId", "N/A"),
            "rfmGroup": customer.get("rfmGroup", "未知"),
            "orderstatus": "confirmed",  # 模擬最近訂單狀態，需改成動態
            "Email": f"{customer.get('userId', 'N/A')}@example.com",
            "color": "red" if customer.get("rfmGroup") == "1" else "gray"  # 分組對應顏色
        }
        for customer in customers
    ]
    return {"customers": formatted_customers}
