from django.contrib import admin

# Register your models here.
from simple_image_upload.models import Images


class ImageMixin(object):
    readonly_fields = ['inline_image']

    def inline_image(self, obj):
        return u'<img src="%s" style="height:128px"/>' % obj.image.url
    inline_image.short_description = 'Image'
    inline_image.allow_tags = True


@admin.register(Images)
class ImagesAdmin(ImageMixin, admin.ModelAdmin):
    pass
