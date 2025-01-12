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

# 提取產品數據
def fetch_products() -> List[Dict]:
    try:
        response = table.scan(
            FilterExpression="begins_with(id, :prefix)",
            ExpressionAttributeValues={":prefix": "Product"}
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

# API 路由：獲取產品庫存數據
@router.get("/get-products-data")
def get_products_data():
    products = fetch_products()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    # 格式化產品數據，添加計算邏輯
    formatted_products = []
    for product in products:
        forecast_demand = 15  # 模擬值，應基於歷史訂單計算
        safe_level = int(forecast_demand * 0.1)  # 假設 95% 服務水準
        lead_time = product.get("leadTime", 30)  # 預設交貨週期為 30 天
        re_order_point = int(forecast_demand * (lead_time / 30) + safe_level)

        formatted_products.append({
            "productId": product.get("id"),
            "inventoryLevel": product.get("inventoryLevel", [0] * 9),
            "forecastDemand": forecast_demand,
            "safeLevel": safe_level,
            "reOrderPoint": re_order_point,
            "times": ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期']
        })

    return {"products": formatted_products}
