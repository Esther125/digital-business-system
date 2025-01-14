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

def get_nine_periods_data(component_id: str) -> Dict:
    """
    從 DynamoDB 中提取指定組件的詳細數據，並進行計算
    """
    try:
        response = table.get_item(Key={'id': component_id})
        if 'Item' in response:
            component = response['Item']
            component_history_key = f"componentHistory#{component_id.split('#')[-1]}"
            history = component.get(component_history_key, {})

            # 計算庫存指標
            metrics = calculate_inventory_metrics(component)

            return {
                "id": component_id,
                "times": history.get('times', []),
                "inventoryLevel": history.get('inventoryLevel', []),
                **metrics  # 添加計算後結果
            }
        else:
            print(f"警告：組件 {component_id} 無法找到相關數據")
            return None
    except Exception as e:
        print(f"錯誤：提取組件 {component_id} 數據失敗 - {e}")
        return None

def calculate_inventory_metrics(component):
    """
    根據提取的數據動態計算預期需求、安全存量及再訂購點，並取整數
    """
    import math

    usage_per_month = float(component.get("usagePerMonth", 0))
    lead_time = float(component.get("leadTime", 0))

    # 提取歷史庫存數據
    history_key = f"componentHistory#{component['id'].split('#')[-1]}"
    inventory_levels = component.get(history_key, {}).get("inventoryLevel", [])

    # 計算需求的標準差
    if inventory_levels and len(inventory_levels) > 1:
        mean_inventory = sum(inventory_levels) / len(inventory_levels)
        squared_diffs = [(level - mean_inventory) ** 2 for level in inventory_levels]
        forecast_demand_std = math.sqrt(sum(squared_diffs) / (len(inventory_levels) - 1))  # 樣本標準差
    else:
        forecast_demand_std = 0  # 若無法計算，預設為 0

    z_value = 1.65  # 假設服務水準為 95%

    # 預期需求
    expected_demand = usage_per_month * lead_time

    # 安全存量計算
    if lead_time > 0 and forecast_demand_std > 0:
        safety_stock = z_value * forecast_demand_std * math.sqrt(lead_time)
    else:
        safety_stock = 0  # 當數據缺失時返回 0

    # 再訂購點計算
    reorder_point = expected_demand + safety_stock

    # 四捨五入取整
    return {
        "expectedDemand": round(expected_demand),
        "safetyStock": round(safety_stock),
        "reorderPoint": round(reorder_point)
    }




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
