from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
import boto3
import os
from dotenv import load_dotenv
from src.service import get_current_user

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

@router.get("/orders", response_model=List[Dict])
def get_orders(current_user: str = Depends(get_current_user)):
    """
    根據目前登入的客戶 ID 篩選該客戶的訂單。
    """
    try:
        # 篩選 buyer 屬於當前使用者的訂單
        response = table.scan(
            FilterExpression="buyer = :customer",
            ExpressionAttributeValues={":customer": f"Customer#{current_user}"}
        )
        orders = response.get("Items", [])
        return orders
    except Exception as e:
        print(f"取得訂單資料時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail="無法取得訂單資料")
