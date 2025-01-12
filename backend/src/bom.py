from fastapi import APIRouter, HTTPException
import boto3
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

# DynamoDB 配置
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

table_name = "sysdata"
table = dynamodb.Table(table_name)


# 計算產品的所需數量和下期預期需求
def calculate_product_requirements(product_id):
    try:
        response = table.get_item(Key={'id': product_id})
        if 'Item' not in response:
            # 返回默認值，確保表格顯示
            return {
                "productId": product_id,
                "currentQuantity": 0,
                "forecastDemand": 0,
                "leadTime": 0,
                "price": 0,
                "componentCollection": None,
            }

        product = response['Item']
        product_history = product.get('productHistory#1', {}).get('inventoryLevel', [])

        # 確保數據充足，避免越界
        if len(product_history) < 9:
            print(f"Warning: Insufficient history data for {product_id}.")
            current_quantity = 0
            forecast_quantity = 0
        else:
            current_quantity = product_history[8]  # 第 9 期數據
            forecast_quantity = sum(product_history[5:8]) / 3 if len(product_history) >= 8 else 0

        return {
            "productId": product_id,
            "currentQuantity": current_quantity,
            "forecastDemand": round(forecast_quantity, 2),
            "leadTime": product.get("leadTime", 0),
            "price": product.get("price", 0),
            "componentCollection": product.get("componentCollection", None),
        }
    except Exception as e:
        print(f"Error calculating product requirements for {product_id}: {e}")
        return {
            "productId": product_id,
            "currentQuantity": 0,
            "forecastDemand": 0,
            "leadTime": 0,
            "price": 0,
            "componentCollection": None,
        }


# 獲取組件的需求數據
def calculate_component_requirements(component_id):
    try:
        response = table.get_item(Key={'id': component_id})
        if 'Item' not in response:
            return {
                "componentId": component_id,
                "forcastDemand": 0,
                "leadTime": 0,
                "inventoryLevel": 0,
            }

        component = response['Item']
        return {
            "componentId": component_id,
            "forcastDemand": component.get("forcastDemand", 0),
            "leadTime": component.get("leadTime", 0),
            "inventoryLevel": component.get("inventoryLevel", 0),
        }
    except Exception as e:
        print(f"Error calculating component requirements for {component_id}: {e}")
        return None


# 獲取產品及組件的完整數據
def get_bom_data():
    try:
        boms = []
        for i in range(1, 7):  # 確保返回 Product#1 到 Product#6
            product_id = f"Product#{i}"
            product_data = calculate_product_requirements(product_id)
            if not product_data:
                continue

            component_collection_id = product_data.get("componentCollection", None)
            components = []

            # 獲取組件數據
            if component_collection_id:
                collection_response = table.get_item(Key={'id': component_collection_id})
                if 'Item' in collection_response:
                    collection = collection_response['Item']
                    for component in collection.get("components", []):
                        component_data = calculate_component_requirements(
                            component.get("componentId", "N/A")
                        )
                        if component_data:
                            components.append(component_data)

            product_data["components"] = components
            boms.append(product_data)

        return boms
    except Exception as e:
        print(f"Error retrieving BOM data: {e}")
        return []


# FastAPI 路由
@router.get("/get-bom")
async def fetch_bom():
    data = get_bom_data()
    if not data:
        raise HTTPException(status_code=404, detail="No BOM data found.")
    return {"boms": data}
