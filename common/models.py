from django.db import models

from django.contrib.sites.models import Site
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _, get_language
from thread_locals import get_current_request, get_current_user, get_current_site
from django.db.models import Max
from django.views.generic.list import ListView, MultipleObjectMixin

from django.db.models import F
from django.conf import settings

from .utils import UploadPath, lang_get

if hasattr(settings, 'AUTH_USER_MODEL'):
    User = settings.AUTH_USER_MODEL
else:
    from django.contrib.auth.models import User


class SiteManager(models.Manager):
    def get_queryset(self):
        from django.conf import settings

        try:
            return super(SiteManager, self).get_queryset().filter(site=get_current_site)
        except BaseException, e:
            return super(SiteManager, self).get_queryset().filter(site__id=settings.SITE_ID)


class UserManager(models.Manager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(user=get_current_user)


class DefaultManager(models.Manager):
    def get_queryset(self):
        return super(DefaultManager, self).get_queryset().filter(state=True)


class SiteDefaultManager(DefaultManager):
    def get_queryset(self):
        from django.conf import settings

        try:
            return super(SiteDefaultManager, self).get_queryset().filter(site=get_current_site)
        except BaseException, e:
            return super(SiteDefaultManager, self).get_queryset().filter(site__id=settings.SITE_ID)


class UserSiteManager(SiteManager):
    def get_queryset(self):
        return super(UserSiteManager, self).get_queryset().filter(user=get_current_user)


class UserDefaultManager(UserManager):
    def get_queryset(self):
        return super(UserDefaultManager, self).get_queryset().filter(state=True)


class UserSiteDefaultManager(UserSiteManager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(state=True)


class AbstractDefaultModel(models.Model):
    state = models.BooleanField(verbose_name=_('state'), default=True)
    pos = models.PositiveIntegerField(verbose_name=_('pos'), default=0)
    since = models.DateTimeField(auto_now_add=True, verbose_name=_('since'))
    objects = models.Manager()
    active_objects = DefaultManager()

    class Meta:
        abstract = True
        ordering = ['pos']


class AbstractUserModel(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), default=get_current_user)
    objects = models.Manager()
    user_objects = UserManager()
    active_objects = DefaultManager()

    class Meta:
        abstract = True


class AbstractUserDefaultModel(AbstractDefaultModel):
    user = models.ForeignKey(User, verbose_name=_('user'), default=get_current_user)
    objects = models.Manager()
    user_objects = UserManager()
    user_active_objects = UserDefaultManager()

    class Meta:
        abstract = True
        ordering = ['pos']


class AbstractUserSiteDefaultModel(AbstractUserDefaultModel):
    site = models.ForeignKey(Site, verbose_name=_('site'), default=get_current_site, blank=True, null=True)

    objects = models.Manager()
    user_objects = UserManager()
    site_objects = SiteManager()
    active_objects = DefaultManager()
    active_site_objects = SiteDefaultManager()
    user_site_objects = UserSiteManager()
    user_site_active_objects = UserSiteDefaultManager()

    class Meta:
        abstract = True
        ordering = ['pos']


class SiteTheme(AbstractUserSiteDefaultModel):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    title = models.CharField(verbose_name=_('title'), max_length=255)

    class Meta:
        ordering = ['pos']
        verbose_name = _('site theme')
        verbose_name_plural = _('site themes')

    def __unicode__(self):
        return '%s - %s' % (unicode(self.name), unicode(self.title))


class SiteTemplate(AbstractUserSiteDefaultModel):
    name = models.CharField(verbose_name=_('site template'), max_length=255)
    site_theme = models.ForeignKey(SiteTheme, verbose_name=_('site theme'), blank=True, null=True)
    content = models.TextField(verbose_name=_('content'))

    class Meta:
        ordering = ['pos']
        verbose_name = _('site template')
        verbose_name_plural = _('site templates')

    def __unicode__(self):
        return '%s - %s' % (unicode(self.site_theme), self.name) if self.site_theme else self.name


class AbstractFile(AbstractDefaultModel, AbstractUserModel):
    site_template = models.ForeignKey(SiteTemplate, verbose_name=_('site template'))

    class Meta:
        abstract = True

    def __unicode__(self):
        from django.conf import settings

        return '%s%s' % (settings.MEDIA_URL, unicode(self.file))




class FileJs(AbstractFile):
    file = models.FileField(_('file'), upload_to=UploadPath(sub_path='uploads/%s/js/%s', field_name='user'))


class FileCss(AbstractFile):
    file = models.FileField(_('file'), upload_to=UploadPath(sub_path='uploads/%s/css/%s', field_name='user'))


class FileImg(AbstractFile):
    file = models.FileField(_('file'), upload_to=UploadPath(sub_path='uploads/%s/img/%s', field_name='user'))


class File(AbstractFile):
    file = models.FileField(_('file'), upload_to=UploadPath(sub_path='uploads/%s/file/%s', field_name='user'))


class SiteSettings(AbstractUserSiteDefaultModel):
    name = models.CharField(verbose_name=_('name'), max_length=255, unique=True)
    value = models.CharField(verbose_name=_('value'), max_length=255, blank=True, null=True)
    value_txt = models.TextField(verbose_name=_('text value'), blank=True, null=True)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.name, self.value)

    class Meta:
        verbose_name = _('site setting')
        verbose_name_plural = _('site settings')
        ordering = ['name']


    @classmethod
    def cls_value_get(cls, name, default=None):
        try:
            obj = cls.site_objects.get(name=name, state=True)
            return obj.value_get()
        except cls.DoesNotExist:
            return default

    def value_get(self):
        return self.value if self.value and len(self.value) else self.value_txt



    @classmethod
    def robots_get(cls):
        robot = cls.objects.get(name='robots.txt')
        robots_str = robot.value or robot.value_txt
        return robots_str if robots_str and len(robots_str) else '''User-agent: *
        Disallow:'''


class AbstractMailTemplate(AbstractUserSiteDefaultModel):
    name = models.CharField(_('name'), max_length=255)
    from_email = models.CharField(_('from email'), max_length=255, blank=True)
    subject = models.CharField(_('Subject'), max_length=255, blank=True)
    recipients = models.CharField(_('recipients'), max_length=255, blank=True)
    html_content = models.TextField(_('html content'))
    text_content = models.TextField(_('text content'), null=True, blank=True)

    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('mail template')
        verbose_name_plural = _('mail templates')
        abstract = True


class AbstractMailTemplate_v_1_00(AbstractUserSiteDefaultModel):
    name = models.CharField(_('name'), max_length=255)
    from_email = models.CharField(_('from email'), max_length=255, blank=True)
    subject = models.CharField(_('Subject'), max_length=255, blank=True)
    recipients = models.CharField(_('recipients'), max_length=255, blank=True)

    template_html = models.ForeignKey(SiteTemplate, verbose_name=_('html template'), blank=True, null=True,
                                      related_name='template_html_set')
    template_text = models.ForeignKey(SiteTemplate, verbose_name=_('text template'), blank=True, null=True,
                                      related_name='template_text_set')

    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('mail template')
        verbose_name_plural = _('mail templates')
        abstract = True


class AbstractList(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=255, blank=True, null=True)
    pos = models.PositiveIntegerField(verbose_name=_('pos'), default=0)
    primary = models.BooleanField(verbose_name=_('primary'), default=False)

    def save(self, **kwargs):
        if self.primary:
            self.__class__.objects.filter(primary=True).update(primary=False)

        if not self.pk:
            max_pos = self.__class__.objects.aggregate(Max('pos'))['pos__max']
            if not max_pos is None:
                self.pos = max_pos + 1

        return super(AbstractList, self).save(**kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-primary', 'pos', 'title']
        abstract = True


class BaseAbstractTree(AbstractUserSiteDefaultModel):
    parent = models.ForeignKey('self', related_name='parent_node', null=True, blank=True, verbose_name=_('parent'))
    level = models.PositiveIntegerField(verbose_name=_('level'), default=0)
    path = models.TextField(verbose_name=_('path'), blank=True)

    inner_pos = models.CharField(verbose_name=_('inner pos'), max_length=255, default='', blank=True)

    def save(self, **kwargs):
        if self.parent:
            if self.path:
                self.descendants_get().update(level=F('level') - self.level + self.parent.level + 1)

            self.level = self.parent.level + 1
            if not self.pk:
                max_pos = self.__class__.site_objects.filter(parent=self.parent).aggregate(Max('pos'))['pos__max']
                if not max_pos is None:
                    self.pos = max_pos + 1
        else:
            self.level = 0

        super(BaseAbstractTree, self).save(**kwargs)
        self.__class__.path_update()


    @classmethod
    def tree_get(cls, active_pk=None, params={}):
        queryset = cls.site_objects.filter(**params).order_by('-level', 'pos')
        dic = SortedDict()
        for item in queryset:
            if item.pk == active_pk:
                item.active = True
            parent_pk = 0

            if item.parent:
                parent_pk = item.parent.pk

            if not parent_pk in dic:
                dic[parent_pk] = SortedDict()
            dic[parent_pk][item.pk] = item

            if item.pk in dic:
                dic[parent_pk].update(dic[item.pk])
                del (dic[item.pk])

        if len(dic):
            return dic.popitem()[1].values()
        return []

    @classmethod
    def path_update(cls):
        dic = cls.tree_get()
        nm = 'site'
        ind = 0
        path = []
        curr_level = 0

        for item in dic:

            if item.level == curr_level:
                if len(path):
                    path.pop()
                path.append(str(item.pk))

            if item.level > curr_level:
                path.append(str(item.pk))

            if item.level < curr_level:
                for i in range(item.level, curr_level + 1):
                    if len(path):
                        path.pop()
                path.append(str(item.pk))

            item.inner_pos = '%s-%030d' % (nm, ind)
            item.path = '%s,' % ','.join(path)

            ind += 1

            curr_level = item.level

            super(BaseAbstractTree, item).save()

    def descendants_get(self, with_parent=False, **kwargs):
        kwargs['path__istartswith'] = self.path
        if not 'level__gte' in kwargs:
            kwargs['level__gte'] = self.level
        queryset = self.__class__.site_objects.filter(**kwargs)
        if not with_parent:
            queryset = queryset.exclude(pk=self.pk)
        return queryset

    def children_get(self):
        return self.__class__.site_objects.filter(parent=self)

    def path_get(self):
        return self.path.split(',')[:-1]

    def parents_get(self, include_self=False, min_level=0, max_level=100):
        if len(self.path) > 1:
            qset = self.__class__.site_objects.filter(pk__in=self.path_get(), level__gte=min_level,
                                                      level__lte=max_level)
            if not include_self:
                qset = qset.exclude(pk=self.pk)
            return qset
        return []

    def delete(self, using=None):
        cls = self.__class__
        for obj in self.descendants_get():
            super(BaseAbstractTree, obj).delete(using=using)

        super(BaseAbstractTree, self).delete(using=using)
        cls.path_update()

    class Meta:
        verbose_name = _('tree')
        verbose_name_plural = _('tree')
        ordering = ['site', 'inner_pos', 'pos']
        abstract = True


class AbstractTree(BaseAbstractTree):
    title = models.CharField(verbose_name=_('title'), max_length=255)
    name = models.CharField(verbose_name=_('name'), max_length=255, blank=True)
    url = models.CharField(verbose_name=_('url'), max_length=255, null=True, blank=True)

    perms = 0 #1 - user, 2 - site, 3 - user and site. 0 - no check

    class Meta:
        verbose_name = _('tree')
        verbose_name_plural = _('tree')
        ordering = ['site', 'inner_pos', 'pos', 'title']
        abstract = True


    def __unicode__(self):
        return '%s%s' % ('..' * self.level, self.title)


CHOICES_PAGE_POS = (
    (1, _('top')),
    (2, _('bottom')),
    (4, _('left')),
    (8, _('right')),
    (16, _('free')),
    (127, _('all')),
)


class AbstractSimplePage(AbstractUserSiteDefaultModel):
    url = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(_('title'), max_length=255, null=True, blank=True)
    site_template = models.ForeignKey('SiteTemplate', verbose_name=_('site template'), null=True, blank=True)

    content = models.TextField(_('content'), blank=True)

    is_content_template = models.BooleanField(verbose_name=_('is content template'), default=False)

    position_nav = models.PositiveSmallIntegerField(_('navigation position'), choices=CHOICES_PAGE_POS, default=1)
    position_content = models.PositiveSmallIntegerField(_('content position'), choices=CHOICES_PAGE_POS, default=1)

    nav_title = models.CharField(_('nav title'), max_length=255, blank=True)
    nav_show = models.BooleanField(_('nav show'), default=True)

    extra_pos = models.PositiveIntegerField(_('extra pos'), default=0, blank=True)

    seo_keywords = models.CharField(_('seo keywords'), max_length=255, blank=True)
    seo_description = models.CharField(_('seo description'), max_length=255, blank=True)
    seo_title = models.CharField(_('seo title'), max_length=255, blank=True)

    def __unicode__(self):
        return 'url:%s title:%s nav:%s content:%s' % (
            self.title, self.url, self.get_position_nav_display(), self.get_position_content_display())

    class Meta:
        verbose_name = _('simple page')
        verbose_name_plural = _('simple pages')
        ordering = ('position_nav', 'pos', 'position_content', 'seo_title')
        abstract = True

    def save(self, **kwargs):
        if not len(self.seo_title):
            self.seo_title = self.title
        if not len(self.nav_title):
            self.nav_title = self.title
        return super(AbstractSimplePage, self).save(**kwargs)



class LocaleModelMixin(object):
    """
    Mixin model for getting locale field value - product.name => product.name_[en, es, it]
    """
    def __getattr__(self, item):
        local_name = '%s_%s' % (item, lang_get())
        if local_name in self.__dict__:
            return self.__dict__[local_name]

        raise AttributeError
