from fastapi import FastAPI
from pydantic import BaseModel
import boto3
from boto3.dynamodb.conditions import Attr
import random

from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# DynamoDB 配置
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-1',
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY'
)

table_name = "sysdata"
table = dynamodb.Table(table_name)

def generate_nine_periods_data(product_id):
    """
    为指定产品生成九期随机库存数据并更新到数据库
    """
    try:
        times = [f"第{i}期" for i in range(1, 10)]
        inventory_levels = [random.randint(10, 50) for _ in range(9)]

        product_history_key = f"productHistory#{product_id.split('#')[-1]}"

        # 使用 ExpressionAttributeNames 映射键
        table.update_item(
            Key={'id': product_id},
            UpdateExpression="SET #history_key = :history",
            ExpressionAttributeNames={
                '#history_key': product_history_key
            },
            ExpressionAttributeValues={
                ':history': {
                    "times": times,
                    "inventoryLevel": inventory_levels
                }
            }
        )
        print(f"Updated {product_id} with nine periods data.")
        return {"productId": product_id, "times": times, "inventoryLevel": inventory_levels}
    except Exception as e:
        print(f"Error updating nine periods data for {product_id}: {e}")
        return None

def update_all_products():
    """
    为 Product#1 到 Product#6 生成九期随机库存数据并更新到数据库
    """
    products = [f"Product#{i}" for i in range(1, 7)]
    result = []
    for product in products:
        data = generate_nine_periods_data(product)
        if data:
            result.append(data)
    return result

def get_nine_periods_product_data(product_id):
    """
    从数据库中获取指定产品的九期库存数据
    """
    try:
        # 查询 DynamoDB，获取指定产品的数据
        response = table.get_item(Key={'id': product_id})
        if 'Item' in response:
            # 获取产品数据
            product = response['Item']
            
            # 动态生成历史记录键，例如 "productHistory#1"
            product_history_key = f"productHistory#{product_id.split('#')[-1]}"
            
            # 获取历史数据
            history = product.get(product_history_key, {})
            times = history.get('times', [])  # 时间周期
            inventory_levels = history.get('inventoryLevel', [])  # 库存数据
            
            # 返回结果
            return {
                "productId": product_id,
                "times": times,
                "inventoryLevel": inventory_levels
            }
        else:
            print(f"Product {product_id} not found.")
            return None
    except Exception as e:
        print(f"Error retrieving nine periods data for {product_id}: {e}")
        return None

if __name__ == "__main__":
    # 更新所有产品，生成九期随机数据
    print("Updating all products with nine periods data...")
    update_results = update_all_products()
    print("Update Results:")
    for result in update_results:
        print(result)

    # 测试获取单个产品的九期库存数据
    print("\nFetching data for Product#1:")
    product_data = get_nine_periods_product_data("Product#1")
    print(product_data)

@app.get("/get-products-data")
def fetch_all_products_data():
    """
    获取所有产品的九期库存数据
    """
    products = [f"Product#{i}" for i in range(1, 7)]
    result = []
    for product in products:
        data = get_nine_periods_product_data(product)
        if data:
            result.append(data)
    return result
