import boto3 # type: ignore
import random
from dotenv import load_dotenv
import os
from fastapi import APIRouter

load_dotenv()
router = APIRouter()

# DynamoDB 配置
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

component_table = dynamodb.Table('sysdata')


def calculate_and_update_component_demand(component_id):
    """
    计算组件的需求量并将结果更新回 DynamoDB 表，仅更新 forcastDemand，正确解析历史使用量。
    """
    try:
        # 查询组件数据
        response = component_table.get_item(Key={'id': component_id})
        if 'Item' in response:
            component = response['Item']
            safe_level = component.get('safeLevel', 0)
            inventory_level = component.get('inventoryLevel', 0)

            # 获取历史使用量（从 componentHistory#n 中解析）
            component_history_key = f"componentHistory#{component_id.split('#')[-1]}"
            history = component.get(component_history_key, {})
            usage_history = history.get('inventoryLevel', [])  # 获取历史库存数据列表
            print(f"Usage history for {component_id}: {usage_history}")

            # 如果没有历史数据，默认使用 usagePerMonth
            if len(usage_history) == 0:
                usage_per_month = component.get('usagePerMonth', 10)  # 默认值设为 10
            else:
                # 使用移动平均法预测未来使用量（简单平均）
                usage_per_month = sum(usage_history[-3:]) / min(len(usage_history), 3)

            # 四舍五入到整数
            usage_per_month = max(round(usage_per_month), 1)  # 确保预测使用量至少为 1
            print(f"Predicted usage per month for {component_id}: {usage_per_month}")

            # 计算需求量（考虑库存和安全水平）
            demand = max(1, (safe_level + usage_per_month) - inventory_level)  # 确保需求量至少为 1

            # 四舍五入需求量
            demand = round(demand)

            # 更新表中的 forcastDemand 字段
            component_table.update_item(
                Key={'id': component_id},
                UpdateExpression="SET forcastDemand = :demand",
                ExpressionAttributeValues={':demand': demand}
            )

            print(f"Component {component_id} updated with forcastDemand: {demand}")
            return {"componentId": component_id, "forcastDemand": demand}
        else:
            print(f"Component {component_id} not found.")
            return {"componentId": component_id, "forcastDemand": None}
    except Exception as e:
        print(f"Error calculating or updating component demand: {e}")
        return {"componentId": component_id, "forcastDemand": None}
    
def generate_linear_inventory(start_level, steps, fluctuation):
    """
    生成线性变化并随机波动的库存数据
    :param start_level: 起始库存量
    :param steps: 线性变化的步长
    :param fluctuation: 每期随机波动范围 ± fluctuation
    :return: 包含 9 期库存数据的列表
    """
    inventory_levels = [start_level]
    for _ in range(8):  # 生成后续 8 期数据，总共 9 期
        next_level = inventory_levels[-1] + steps
        fluctuated_level = max(0, next_level + random.randint(-fluctuation, fluctuation))  # 保证库存不为负数
        inventory_levels.append(fluctuated_level)
    return inventory_levels


def update_component_history(component_id):
    """
    为指定组件生成九期数据并更新到 DynamoDB 表中
    """
    try:
        times = ['第一期', '第二期', '第三期', '第四期', '第五期', '第六期', '第七期', '第八期', '第九期']

        # 配置起始库存、线性步长和波动范围
        start_level = random.randint(100, 150)  # 起始库存量在 10 到 20 之间随机生成
        steps = random.randint(-10, 10)        # 每期线性变化步长
        fluctuation = 5                      # 随机波动范围 ±5

        # 生成线性变化的库存数据
        inventory_levels = generate_linear_inventory(start_level, steps, fluctuation)

        # 更新表中的 componentHistory 数据
        component_table.update_item(
            Key={'id': component_id},
            UpdateExpression="SET #history = :history",
            ExpressionAttributeNames={'#history': f"componentHistory#{component_id.split('#')[-1]}"},
            ExpressionAttributeValues={
                ':history': {
                    "times": times,
                    "inventoryLevel": inventory_levels
                }
            }
        )
        print(f"Updated component history for {component_id}")
        return {"id": component_id, "times": times, "inventoryLevel": inventory_levels}
    except Exception as e:
        print(f"Error updating component history for {component_id}: {e}")
        return None

def update_lead_time(component_id):
    """
    为指定组件添加 leadTime 字段，并随机设置值为 1-3。
    """
    try:
        lead_time = random.randint(1, 3)  # 随机生成 1 到 3 的 leadTime 值
        component_table.update_item(
            Key={'id': component_id},
            UpdateExpression="SET leadTime = :leadTime",
            ExpressionAttributeValues={':leadTime': lead_time}
        )
        print(f"Component {component_id} updated with leadTime: {lead_time}")
        return {"componentId": component_id, "leadTime": lead_time}
    except Exception as e:
        print(f"Error updating leadTime for {component_id}: {e}")
        return {"componentId": component_id, "leadTime": None}

# 动态生成组件列表
components = [f"Component#{i}" for i in range(1, 31)]

# 为每个组件更新九期数据并添加 leadTime
for component in components:
    # 更新组件的预测需求量
    data = calculate_and_update_component_demand(component)
    print("Updated Data:", data)
    
    # 为组件添加 leadTime 字段
    lead_time_data = update_lead_time(component)
    print("Lead Time Data:", lead_time_data)

def get_nine_periods_data(component_id):
    """
    从数据库中获取指定组件的九期库存数据
    """
    try:
        response = component_table.get_item(Key={'id': component_id})
        if 'Item' in response:
            component = response['Item']
            component_history_key = f"componentHistory#{component_id.split('#')[-1]}"
            history = component.get(component_history_key, {})
            times = history.get('times', [])
            inventory_levels = history.get('inventoryLevel', [])
            return {
                "id": component_id,
                "times": times,
                "inventoryLevel": inventory_levels
            }
        else:
            print(f"Component {component_id} not found.")
            return None
    except Exception as e:
        print(f"Error retrieving nine periods data for {component_id}: {e}")
        return None

def get_all_components_data():
    """
    获取所有组件的九期库存数据
    """
    components = [f"Component#{i}" for i in range(1, 31)]
    result = []
    for component in components:
        data = get_nine_periods_data(component)
        if data:
            result.append(data)
    return result

from fastapi import FastAPI
from typing import List

app = FastAPI()

@router.get("/get-components-data")
def fetch_all_components_data():
    return get_all_components_data()
