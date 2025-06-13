# 导入FastAPI类
from fastapi import FastAPI,status,Request
from fastapi.responses import JSONResponse, Response, RedirectResponse
import base64
from typing import Union
import time
import os
import json
import random
import uvicorn
from distutils.util import strtobool
from log import new_logger

config = json.load(open('./config.json', 'r', encoding='utf8'))

def reponse(*, code=200,data: Union[list, dict, str],message="Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'message': message,
            'data': data
        }
    )

# 使用当前模块的名称构建FastAPI app
app = FastAPI()

logger = new_logger('IMAGE-MAIN', False)
r_logger = new_logger('REDIRECT', False)

@app.get("/")
async def root(request: Request):
    client_ip = get_client_ip(request)
    _url = f'{client_ip}'
    r_logger.info(f'Client:{_url} Redirecting To /IMAGE')
    return RedirectResponse(url="/IMAGE")

@app.get("/IMAGE", response_class=JSONResponse)
async def get_image_data(request: Request, data:str="json"):
    client_ip = get_client_ip(request)
    _url = f'{client_ip}'
    logger.info(f'Client:{_url} GET Request /IMAGE')
    image_data = image_to_base64()
    if image_data is not None:
        return reponse(data=image_data,code=200,message="success")
    else:
        _msg = "未读取到本地图片，请检查图片文件夹"
        logger.error(_msg)
        return reponse(data={'msg':_msg},code=500,message="error")

def image_to_base64():
    folder_path = ".\\images\\"
    # 获取文件夹内所有图片文件
    img_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    images = [f for f in os.listdir(folder_path) 
             if f.lower().endswith(img_extensions)]
    
    if not images:
        return None
    
    # 随机选择一张图片
    selected_img = random.choice(images)
    img_path = os.path.join(folder_path, selected_img)
    
    # 转换为base64
    with open(img_path, "rb") as img_file:
        base64_str = base64.b64encode(img_file.read()).decode('utf-8')
    logger.info(f"已读取：{img_file}")
    return {base64_str}

def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # x-forwarded-for 可能包含多个 IP 地址，以逗号分隔
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host
    return client_ip

if __name__ == '__main__':
    start = time.time()
    logger.info(f"初始化耗时：{time.time() - start}")
    uvicorn.run(app, host=str(config['host']), port=int(config['port']),access_log=strtobool(config['api_log']))
