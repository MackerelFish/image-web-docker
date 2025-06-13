# 使用Python 3.10作为基础镜像 
FROM python:3.10.17-slim-bookworm
RUN pip install --upgrade pip
WORKDIR /image_web
COPY ./ /image_web
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
