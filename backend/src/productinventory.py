from fastapi import APIRouter, HTTPException
import boto3
import os
from dotenv import load_dotenv
from typing import List, Dict

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

# 提取所有產品數據的 API
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

# 提取單個產品的九期庫存數據
def get_nine_periods_product_data(product_id: str) -> Dict:
    """
    從 DynamoDB 中獲取指定產品的九期數據
    """
    try:
        response = table.get_item(Key={'id': product_id})
        if 'Item' in response:
            product = response['Item']
            product_history_key = f"productHistory#{product_id.split('#')[-1]}"
            history = product.get(product_history_key, {})
            return {
                "productId": product_id,
                "times": history.get('times', []),
                "inventoryLevel": history.get('inventoryLevel', [])
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving data for {product_id}: {e}")
        return None
