# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template.defaultfilters import striptags
from common.fields import ExImageField
from common.models import AbstractTree, AbstractDefaultModel, AbstractSimplePage, AbstractMailTemplate_v_1_00, \
    AbstractUserDefaultModel, LocaleModelMixin, BaseAbstractTree

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common import utils
from django.conf import settings

import logging
from common.thread_locals import get_current_request

from common.utils import lang_get

logger = logging.getLogger('vestblog.models')

# Create your models here.
class Category(LocaleModelMixin, BaseAbstractTree):
    title_ru = models.CharField(verbose_name=_('title ru'), max_length=255, default='')
    title_en = models.CharField(verbose_name=_('title en'), max_length=255, null=True, blank=True, default='')

    name = models.CharField(verbose_name=_('name'), max_length=255, blank=True)

    slug_ru = models.SlugField(verbose_name=_('slug ru'), max_length=255, null=True, blank=True, db_index=True)
    slug_en = models.SlugField(verbose_name=_('slug en'), max_length=255, null=True, blank=True, db_index=True)

    perms = 0  # 1 - user, 2 - site, 3 - user and site. 0 - no check

    link = models.ForeignKey('self', blank=True, null=True, related_name='category_link')

    image = ExImageField(upload_to=utils.UploadPath(sub_path='category_icon', field_name='self', name_gen=True),
                         blank=True, null=True)
    # @property

    @property
    def url(self):
        lang = lang_get()
        url = reverse('frontend:CategoryArticleList', kwargs={'slug': self.slug})

        if lang == settings.LANGUAGE_CODE:
            return url

        return '/%s%s' % (lang, url)

    def __unicode__(self):
        return '%s:::%s' % (self.title_ru, self.title_en)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['site', 'inner_pos', 'pos', 'title_ru']


class SimplePage(AbstractSimplePage):
    pass
    # category = models.ManyToManyField(Category, verbose_name=_('category'), blank=True, null=True)
    # slider = models.ForeignKey('Slider', verbose_name=_('slider'), blank=True, null=True)
    # slider = models.ForeignKey(Slider)

    # is_content_template = models.BooleanField(verbose_name = _('is content template'), default = False)


class Slider(AbstractUserDefaultModel):
    slug = models.CharField(verbose_name=_('slug'), max_length=255, unique=True)
    title = models.CharField(verbose_name=_('title'), max_length=255, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.title, self.slug)

    def sliders(self):
        return self.sliderimage_set.filter(state=True)

    class Meta:
        verbose_name = _('slider')
        verbose_name_plural = _('sliders')


class Tag(LocaleModelMixin, models.Model):
    title_ru = models.CharField(verbose_name=_('title ru'), max_length=255)
    title_en = models.CharField(verbose_name=_('title en'), max_length=255)

    slug_ru = models.SlugField(verbose_name=_('slug ru'), max_length=255, null=True, blank=True, db_index=True)
    slug_en = models.SlugField(verbose_name=_('slug en'), max_length=255, null=True, blank=True, db_index=True)

    num = models.PositiveIntegerField(verbose_name=_('num'), default=0)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'title_ru__icontains', 'title_en__icontains',)

    @property
    def url(self):
        lang = lang_get()
        url = reverse('frontend:TagArticleList', kwargs={'slug': self.slug})

        if lang == settings.LANGUAGE_CODE:
            return url

        return '/%s%s' % (lang, url)

    def __unicode__(self):
        return '%s ::: %s' % (self.title_ru, self.title_en)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Article(LocaleModelMixin, AbstractUserDefaultModel):
    title_ru = models.CharField(verbose_name=_('title ru'), max_length=255, blank=True)
    slug_ru = models.SlugField(verbose_name=_('slug ru'), max_length=255, unique=True)
    content_ru = models.TextField(verbose_name=_('content ru'), blank=True)
    preview_ru = models.TextField(verbose_name=_('preview ru'), blank=True, null=True, default='')

    title_en = models.CharField(verbose_name=_('title en'), max_length=255, blank=True)
    slug_en = models.SlugField(verbose_name=_('slug en'), max_length=255, unique=True)
    content_en = models.TextField(verbose_name=_('content en'), blank=True)
    preview_en = models.TextField(verbose_name=_('preview ru'), blank=True, null=True, default='')

    github_url = models.CharField(verbose_name=_('github link'), max_length=255, blank=True, null=True)

    category = models.ForeignKey(Category, verbose_name=_('category'), blank=True, null=True, default=None)

    tag = models.ManyToManyField(Tag, verbose_name=_('tag'), blank=True, null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.title_ru, self.title_en)

    # @staticmethod
    # def autocomplete_search_fields():
    # return ('tag__id__iexact', 'tag__title_ru__icontains','tag__title_en__icontains',)


    @property
    def url(self):
        lang = lang_get()
        url = reverse('frontend:ArticleDetail', kwargs={'slug': self.slug})

        if lang == settings.LANGUAGE_CODE:
            return url

        return '/%s%s' % (lang, url)

    def save(self, **kwargs):
        import markdown

        if not self.slug_en:
            self.slug_en = self.slug_ru

        if not self.preview_ru:
            self.preview_ru = striptags(markdown.markdown(self.content_ru, ['extra']))[0:400]

        if not self.preview_en:
            self.preview_en = striptags(markdown.markdown(self.content_en, ['extra']))[0:400]

        super(Article, self).save(**kwargs)

        for tag in self.tag.all():
            tag.num = Article.tag.through.objects.filter(tag=tag).count()
            tag.save()

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-id']


class Poll(LocaleModelMixin, AbstractDefaultModel):
    article = models.ForeignKey(Article, verbose_name=_('article'), blank=True, null=True)

    title_ru = models.CharField(verbose_name=_('title ru'), max_length=255)
    title_en = models.CharField(verbose_name=_('title en'), max_length=255, blank=True)

    date_close = models.DateTimeField(verbose_name=_('date close'), blank=True, null=True)

    content_ru = models.TextField(verbose_name=_('content ru'))
    content_en = models.TextField(verbose_name=_('content ru'), blank=True)

    num_votes = models.PositiveIntegerField(verbose_name=_('num votes'), default=0)

    def save(self, **kwargs):
        self.num_votes = self.vote_set.all().count()
        super(Poll, self).save(**kwargs)

    class Meta:
        verbose_name = _('poll')
        verbose_name_plural = _('polls')
        ordering = ['-state', '-id']


class Vote(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_('poll'))
    session_id = models.CharField(verbose_name=_('session id'), max_length=255)

    def save(self, **kwargs):
        if not self.session_id:
            self.session_id = get_current_request().session.session_key

        super(Vote, self).save(**kwargs)
        self.poll.save()

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')

        unique_together = [['poll', 'session_id']]
