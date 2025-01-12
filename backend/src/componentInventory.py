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
    從 DynamoDB 中提取指定組件的九期數據
    """
    try:
        response = table.get_item(Key={'id': component_id})
        if 'Item' in response:
            component = response['Item']
            component_history_key = f"componentHistory#{component_id.split('#')[-1]}"
            history = component.get(component_history_key, {})
            inventory_levels = history.get('inventoryLevel', [])

            # 過濾：如果數據全為 0，則不返回
            if not inventory_levels or all(level == 0 for level in inventory_levels):
                return None

            return {
                "id": component_id,
                "times": history.get('times', []),
                "inventoryLevel": inventory_levels
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving nine periods data for {component_id}: {e}")
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
