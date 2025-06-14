# 图片服务器

## 本地图片发送服务器（使用base64编码发送）

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
3. 使用接口为 http://host:11455/IMAGE ，替换host为宿主机内网ip地址
4. 在宿主机.../images/底下创建分类子文件夹，get请求参数名为subfolder，参数值为自定义的子文件夹名

## 调用方法
`GET`
## 参数说明
参数名|类型|含义
-|-|-
subfolder|string|图片分类子文件夹
空or未匹配参数|null|无返回数据

### 数据格式说明
参数值|含义
-|-
-|传递子文件夹名称
空or未匹配参数|无返回数据

## 返回base64编码格式图片数据

返回值示例
```json
{
    "code":200,
    "message":"success",
    "data":"base64://****"
}
```
