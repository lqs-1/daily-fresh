from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from dfresh import settings


class FastDFSStorage(Storage):

    def __init__(self):
        self.base_url = settings.FDFS_BASE_URL
        self.fdfs_client = settings.FDFS_CLIENT

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, max_length=None):
        client = Fdfs_client(self.fdfs_client)
        rst = client.upload_by_buffer(content.read())
        print(rst)

        if rst.get('Status') != 'Upload successed.':  # res.get()获取字典里的内容
            # 上传失败 抛出异常
            raise Exception('上传文件到fdfs失败')
            # 获取文件id
        filename = rst.get('Remote file_id')
        # 返回文件id
        return filename


    def exists(self, name):  # 调用_save()前会先调用exists()方法
        '''django判断文件名是否可用'''
        return False # False表示没有这个文件名 该文件名可用


    def url(self, name):  # 如果没有这个 在admin显示详情的时候会报url()的错
        '''返回文件url路径'''
        return self.base_url + name  # 一定要加上路径 不然会导致src导入图片的时候没有路径不显示