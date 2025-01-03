from fastapi import FastAPI
from pydantic import BaseModel
import boto3 # type: ignore
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

table_name = "sysdata"
table = dynamodb.Table(table_name)

class ProductRequest(BaseModel):
    product: str

# 获取 ComponentCollection 的数据
def get_collection(product):
    try:
        response = table.get_item(Key={'id': product})
        if 'Item' in response:
            return response['Item'].get('componentCollection', None)
        return None
    except Exception as e:
        print(f"Error querying table: {e}")
        return None


# 从数据库获取 forcast_demand
def get_forcast_demand_from_db(component_id):
    try:
        response = table.get_item(Key={'id': component_id})
        if 'Item' in response:
            component = response['Item']
            # 直接获取数据库中的 forcastDemand 字段
            return component.get('forcastDemand', 0)
        else:
            print(f"Component {component_id} not found.")
            return 0
    except Exception as e:
        print(f"Error retrieving forcast demand for {component_id}: {e}")
        return 0


# 获取组件数据及其 forcast_demand
def get_components_from_collection(component_collection_id):
    try:
        # 查询指定 ComponentCollection ID
        response = table.get_item(
            Key={'id': component_collection_id}  # 主键查询
        )
        
        # 检查查询结果
        if 'Item' in response:
            item = response['Item']
            components = item.get('components', [])  # 获取 components 列表
            result = []
            for component in components:
                component_id = component.get('componentId', 'N/A')
                component_amount = component.get('componentAmount', 0)
                # 从数据库获取 forcast_demand
                forcast_demand = get_forcast_demand_from_db(component_id)
                result.append({
                    "ComponentID": component_id,
                    "Amount": component_amount,
                    "forcast_demand": forcast_demand
                })
            return result
        else:
            print(f"No item found with ComponentCollection ID: {component_collection_id}")
            return []
    except Exception as e:
        print(f"Error querying table: {e}")
        return []


if __name__ == "__main__":
    # 示例调用
    component_collection_id = "ComponentCollection#6"  # 替换为实际输入
    result_list = get_components_from_collection(component_collection_id)
    print(result_list)

# FastAPI 路由
@router.post("/get-bom")
async def fetch_bom(data: ProductRequest):
    component_collection = get_collection(data.product)
    if not component_collection:
        return {"boms": []}

    components = get_components_from_collection(component_collection)
    return {"boms": components}
