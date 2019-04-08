from django.contrib import admin
from .models import Category, Keyword, PTArticle, UserInfo

# Register your models here.

admin.AdminSite.site_title = 'KBS平台管理系统'
admin.AdminSite.site_header = '旅行者Ⅰ号'
admin.AdminSite.index_title = 'KBS-平台管理'


class KeywordInline(admin.StackedInline):
    model = Keyword
    extra = 3


@admin.register(Category)
class Category(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name', 'listKeyword']
    inlines = [KeywordInline]


@admin.register(PTArticle)
class PTArticle(admin.ModelAdmin):
    exclude = []
    list_display = ['title', 'c', 'a', 'k', 'c_time', 'u_time']
    # add_form_template = 'admin/adminPTArticle.html'
    # radio_fields = {'a': admin.HORIZONTAL}
    list_per_page = 5
    search_fields = ['c']
    date_hierarchy = 'u_time'
    list_filter = ['title', 'k', 'c_time']

    class Media:

        js = ['/static/blogs/js/adminPTArticle.js']

    def release(self, request, queryset):
        queryset.update(statue=True)

    def recall(self, request, queryset):
        queryset.update(statue=False)
    recall.short_description = '撤回发布'
    release.short_description = '发布'
    actions = [release, recall]
