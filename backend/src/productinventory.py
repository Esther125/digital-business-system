import math
from fastapi import APIRouter, HTTPException
import boto3
import os
from dotenv import load_dotenv
from typing import List, Dict
from decimal import Decimal

# 環境變量載入
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

# 計算產品數據的核心指標
def calculate_inventory_metrics(product):
    """
    根據產品數據計算 expectedDemand, safetyStock, 和 reorderPoint
    """
    # 提取 Lead Time，確保轉換為 float
    lead_time = float(product.get("leadTime", 0))

    # 提取 Usage Per Month
    history_key = f"productHistory#{product['id'].split('#')[-1]}"
    inventory_levels = product.get(history_key, {}).get("inventoryLevel", [])

    # 確保所有數值轉換為 float
    inventory_levels = [float(level) for level in inventory_levels]

    # 計算 Usage Per Month
    if inventory_levels and len(inventory_levels) > 1:
        usage_per_month = abs(inventory_levels[-1] - inventory_levels[0]) / len(inventory_levels)
    else:
        usage_per_month = 0  # 若數據不足，預設為 0

    # 預期需求
    expected_demand = usage_per_month * lead_time

    # 假設服務水準的安全存量計算
    z_value = 1.65
    if lead_time > 0 and usage_per_month > 0:
        safety_stock = z_value * usage_per_month * math.sqrt(lead_time)
    else:
        safety_stock = 0

    # 再訂購點計算
    reorder_point = expected_demand + safety_stock

    return {
        "expectedDemand": round(expected_demand),
        "safetyStock": round(safety_stock),
        "reorderPoint": round(reorder_point)
    }

# 提取單個產品的九期數據
def get_nine_periods_product_data(product_id: str) -> Dict:
    """
    從 DynamoDB 獲取指定產品的九期數據，並包含計算結果
    """
    try:
        response = table.get_item(Key={'id': product_id})
        if 'Item' in response:
            product = response['Item']
            product_history_key = f"productHistory#{product_id.split('#')[-1]}"
            history = product.get(product_history_key, {})

            # 計算三項指標
            metrics = calculate_inventory_metrics(product)

            return {
                "productId": product_id,
                "times": history.get('times', []),
                "inventoryLevel": history.get('inventoryLevel', []),
                **metrics  # 包含計算結果
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving data for {product_id}: {e}")
        return None

@router.get("/get-products-data")
def fetch_all_products_data():
    """
    獲取所有產品的九期數據
    """
    products = [f"Product#{i}" for i in range(1, 7)]  # 假設共有 6 個產品
    result = []
    for product in products:
        data = get_nine_periods_product_data(product)
        if data:
            result.append(data)
    if not result:
        raise HTTPException(status_code=404, detail="No products found.")
    return {"products": result}
