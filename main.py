# 导入FastAPI类
from fastapi import FastAPI,status,Request, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response, RedirectResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import aiofiles
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
app.mount("/images", StaticFiles(directory="images"), name="images")

logger = new_logger('IMAGE-MAIN', False)
r_logger = new_logger('REDIRECT', False)

@app.get("/")
async def root(request: Request):
    client_ip = get_client_ip(request)
    _url = f'{client_ip}'
    r_logger.info(f'Client:{_url} Redirecting To /IMAGE')
    return RedirectResponse(url="/IMAGE")

@app.get("/IMAGE")
async def get_image_data(request: Request,subfolder:str=None):
    client_ip = get_client_ip(request)
    _url = f'{client_ip}'
    logger.info(f'Client:{_url} GET Request /IMAGE?subfolder={subfolder}')
    if not subfolder or not subfolder.strip():
        _msg = "未指定文件夹，请检查api参数"
        logger.error(_msg)
        return reponse(data={'msg':_msg},code=500,message="error")
    else:
        image_data = await get_image(subfolder)
        if image_data['code'] == "success":
            image_path = f"/images/{subfolder}/{image_data['data']}"
            logger.info(f"已读取：{image_path}")
            r_logger.info(f'Client:{_url} Redirecting To {image_path}')
            return RedirectResponse(url=image_path)
        elif image_data['code'] == "error":
            _msg = image_data['msg']
            logger.error(_msg)
            raise HTTPException(
                status_code=500,
                detail=_msg,
                headers={"X-Error-Detail": "custom-file-not-found"}
            )
        else:
            _msg = '服务器未知错误'
            logger.error(_msg)
            raise HTTPException(
                status_code=500,
                detail='服务器未知错误',
                headers={"X-Error-Detail": "custom-file-not-found"}
            )
        

@app.get("/images/{filename}")
async def download_file(filename: str):
    file_path = f"images/{filename}"
    if not os.path.exists(file_path):
        _msg = f"{file_path}文件不存在"
        logger.error(_msg)
        raise HTTPException(404, detail="文件不存在")
    
    async def file_stream():
        async with aiofiles.open(file_path, "rb") as f:
            while chunk := await f.read(1024*1024):  # 1MB分块返回
                yield chunk
    
    return StreamingResponse(
        file_stream(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}",
                 "Cache-Control": "no-cache",
                 "Pragma": "no-cache"
                 }
    )

async def get_image(subfolder):
    folder_path = f"./images/{subfolder}"
    # 获取文件夹内所有图片文件
    try:
        img_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        images = [f for f in os.listdir(folder_path) 
                if f.lower().endswith(img_extensions)]
    except Exception as e:
        return {"code":"error","msg":f"{subfolder}文件夹不存在，{e}","data":None}

    if not images:
        return {"code":"error","msg":f"未读取到本地图片，请检查{subfolder}文件夹","data":None}
    
    # 随机选择一张图片
    selected_img = random.choice(images)
    return {"code":"success","msg":"success","data":selected_img}

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
