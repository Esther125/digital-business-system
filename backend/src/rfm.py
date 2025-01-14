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

# 配置表名
table_name = "sysdata"
table = dynamodb.Table(table_name)

# RFM 分組定義
RFM_GROUPS = {
    1: "最優先-忠誠核心客戶",
    2: "次優先-忠誠邊陲客戶",
    3: "一般-穩定客戶",
    4: "次延後-低價值非活躍客戶",
    5: "最延後-流失或無價值客戶"
}

COLORS = {
    1: "red",
    2: "orange",
    3: "yellow",
    4: "green",
    5: "gray"
}

# 提取所有有效的客戶資料
def fetch_all_customers() -> List[Dict]:
    try:
        response = table.scan(
            FilterExpression="attribute_exists(rfmGroup) AND begins_with(id, :prefix)",
            ExpressionAttributeValues={":prefix": "Customer"}
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return []

# 處理 RFM 分組邏輯
def process_rfm_groups(customers: List[Dict]) -> List[Dict]:
    result = []
    for customer in customers:
        rfm_group = int(customer.get("rfmGroup", 5))  # 默認為組 5
        result.append({
            "userId": customer.get("userId", "N/A"),
            "recency": customer.get("recency", "N/A"),
            "frequency": customer.get("frequency", 0),
            "monetaryValue": customer.get("monetaryValue", 0),
            "rfmGroup": RFM_GROUPS.get(rfm_group, "未知分組"),
            "color": COLORS.get(rfm_group, "gray"),
            "groupOrder": rfm_group  # 用於排序的關鍵字段
        })

    # 按 groupOrder 升序排序，然後反轉列表
    result.sort(key=lambda x: x["groupOrder"])
    result.reverse()  # 顛倒順序
    return result

@router.get("/rfm-customers")
def fetch_rfm_customers():
    """
    提取 RFM 分組的客戶數據，並顛倒順序
    """
    customers = fetch_all_customers()
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")

    grouped_customers = process_rfm_groups(customers)

    # 過濾無效客戶數據
    grouped_customers = [customer for customer in grouped_customers if customer["rfmGroup"] != "未知分組"]

    # 返回已顛倒的數據
    return {"customers": grouped_customers}
