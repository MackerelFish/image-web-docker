# 图片服务器

## 使用须知
## 自建本地图片发送服务器

## 使用方法

1.拉取docker镜像
```
docker pull mackerelfish/image-web:latest
```
国内用户连不上官方docker源可使用腾讯云镜像仓库下载并添加镜像别名
```
docker pull ccr.ccs.tencentyun.com/mackerel/wows:image
docker tag ccr.ccs.tencentyun.com/mackerel/wows:image mackerelfish/image-web:latest
```
2.启动docker容器，-v映射你自己的文件路径
```
docker run -d \
-p 11455:11455 \
--name image-web \
-v /{your own path}/image_web/images/:/image_web/images/ \
--restart=always \
mackerelfish/image-web:latest
```
3. 使用接口为 http://host:11455/HITOKOTO ，替换host为宿主机内网ip地址
4. 建议一种分类图片单独使用一个容器，多开容器自行命名容器，替换外部端口映射和外部文件夹映射

## 调用方法
`GET`

## 返回base64格式图片数据

返回值示例
```json
{
    "code":200,
    "message":"success",
    "data":{"base64://****"}
}
```
