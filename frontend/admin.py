from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.contrib import admin

from django import forms


# Register your models here.
# from frontend.models import Article
from django_ace import AceWidget
from frontend.models import Article, Tag, Category, Poll


# wordwrap=False, width="500px", height="300px", showprintmargin=True
class ArticleForm(forms.ModelForm):
    content_ru = forms.CharField(widget=AceWidget(mode='markdown', theme='twilight',
                                                  wordwrap=False, width='100%', height='300px'), required=False)
    content_en = forms.CharField(widget=AceWidget(mode='markdown', theme='twilight',
                                                  wordwrap=False, width='100%', height='300px'), required=False)

    class Meta:
        model = Article


class AdminArticle(admin.ModelAdmin):
    form = ArticleForm
    list_display = ['id', 'since', 'title_ru', 'slug_ru', 'title_en', 'slug_en']
    # list_editable = ['slug_ru', 'slug_en', 'title_ru', 'title_en']
    list_editable = ['title_ru', 'slug_ru']

    raw_id_fields = ['tag']
    # related_lookup_fields = {'m2m': ['tag']}
    autocomplete_lookup_fields = {
        'm2m': ['tag'],
    }


def admin_register(admin_instance):
    admin_instance.register(Category, list_display=['id', 'title_ru', 'slug_ru', 'title_en'],
                            list_editable=['title_ru', 'slug_ru'])
    # admin_instance.register(SimplePage, AdminSimplePage)
    # admin_instance.register(Slider, AdminSlider)
    # admin_instance.register(Order, AdminOrder)
    #
    # admin_instance.register(SiteTemplate, AdminSiteTemplate)
    #
    # admin_instance.register(SiteSettings, list_display=['id', 'name', 'value', 'value_txt', 'description'],
    # list_editable=['name', 'value'])
    # admin_instance.register(SiteTheme)

    admin_instance.register(User, UserAdmin)
    admin_instance.register(Group, GroupAdmin)
    admin_instance.register(Site, list_display=['id', 'domain', 'name'], list_editable=['domain', 'name'])
    admin_instance.register(Article, AdminArticle)
    admin_instance.register(Tag, list_display=['id', 'title_ru', 'slug_ru', 'title_en', 'slug_en', 'num'],
                            list_editable=['title_ru', 'slug_ru',])


    admin_instance.register(Poll, list_display=['id', 'title_ru', 'title_en', 'date_close', 'num_votes', 'state'],
                            list_editable=['title_ru', 'title_en', 'state'])

    # admin_instance.register(Delivery, AdminDelivery)
    # admin_instance.register(DeliveryGroup, AdminDeliveryGroup)