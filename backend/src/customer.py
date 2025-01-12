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
table = dynamodb.Table("sysdata")

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

# 格式化客戶數據
def format_customers(customers: List[Dict]) -> List[Dict]:
    formatted = []
    for customer in customers:
        rfm_group = customer.get("rfmGroup", "未知")
        formatted.append({
            "userId": customer.get("userId", "N/A"),
            "rfmGroup": rfm_group,
            "orderstatus": customer.get("lastOrderStatus", "N/A"),  # 取最近訂單狀態
            "Email": f"{customer.get('userId', 'N/A')}@example.com",
            "color": "red" if rfm_group == "最優先-忠誠核心客戶" else "gray"
        })
    return formatted

# API 路由：返回客戶數據
@router.get("/customers")
def get_customers():
    """
    提取所有客戶數據
    """
    customers = fetch_customers()
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    
    formatted_customers = format_customers(customers)
    return {"customers": formatted_customers}
