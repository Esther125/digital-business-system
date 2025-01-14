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

# 提取九期數據
def get_nine_periods_data(component_id: str) -> Dict:
    """
    從 DynamoDB 中提取指定組件的詳細數據，包括額外字段
    """
    try:
        response = table.get_item(Key={'id': component_id})
        if 'Item' in response:
            component = response['Item']
            component_history_key = f"componentHistory#{component_id.split('#')[-1]}"
            history = component.get(component_history_key, {})

            return {
                "id": component_id,
                "times": history.get('times', []),
                "inventoryLevel": history.get('inventoryLevel', []),
                "forcastDemand": component.get("forcastDemand", "N/A"),
                "holdingCostPerMonth": component.get("holdingCostPerMonth", "N/A"),
                "leadTime": component.get("leadTime", "N/A"),
                "orderAmount": component.get("orderAmount", "N/A"),
                "orderCost": component.get("orderCost", "N/A"),
                "safeLevel": component.get("safeLevel", "N/A"),
                "unitCost": component.get("unitCost", "N/A"),
                "usagePerMonth": component.get("usagePerMonth", "N/A")
                
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving data for {component_id}: {e}")
        return None

# 提取所有組件數據
def get_all_components_data() -> List[Dict]:
    """
    從 DynamoDB 中提取所有組件的九期數據
    """
    components = [f"Component#{i}" for i in range(1, 31)]  # 假設有 30 個組件
    result = []
    for component in components:
        data = get_nine_periods_data(component)
        if data:  # 過濾不存在或數據全為 0 的組件
            result.append(data)
    return result

@router.get("/get-components-data")
def fetch_all_components_data():
    """
    提供所有組件的九期數據 API
    """
    data = get_all_components_data()
    if not data:
        raise HTTPException(status_code=404, detail="No valid component data found.")
    return {"components": data}
