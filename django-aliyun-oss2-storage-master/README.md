# Django Aliyun OSS2 Storage


### Django storage for [阿里云 OSS2](https://www.aliyun.com/product/oss/?spm=5176.383338.201.42.WB7sGd)

## Install

    pip install django-aliyun-oss2-storage

## Configurations

Django Aliyun OSS2 Storage 需要以下几个配置才能正常工作。这些配置通过可以环境变量或 settings.py 来设置。环境变量的优先级要高于 settings.py 。`BUCKET_NAME`是Bucket的名字，如果该bucket不存在，程序会自动创建。`BUCKET_ACL_TYPE`用于设置Bucket的权限，可以设置为`private`, `public-read`和 `public-read-write`。

```python
ACCESS_KEY_ID = "40ZhE1HyuWdllpMh"
ACCESS_KEY_SECRET = "KbxtlKSvKyuyuymTiQvrxhsYFMguXy"
END_POINT = "oss-us-west-1.aliyuncs.com"
BUCKET_NAME = "XXXX"
ALIYUN_OSS_CNAME = "" # 自定义域名，如果不需要可以不填写
BUCKET_ACL_TYPE = "private" # private, public-read, public-read-write
```

## Usage

在 settings.py 里设置 `DEFAULT_FILE_STORAGE` :

```python
# mediafile将自动上传
DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
# staticfile将自动上传
STATICFILES_STORAGE = 'aliyun_oss2_storage.backends.AliyunStaticStorage'
```

## License

基于MIT许可证发布
