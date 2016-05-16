import datetime
import logging

from django.core.urlresolvers import resolve
from django.http import Http404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View, TemplateView, DetailView, ListView
from django.conf import settings

from common import utils
from common.utils import lang_get, qset_to_dict
from common.views import BaseMixin
from frontend.models import Article, Tag, Category, Vote, Poll

logger = logging.getLogger('views')


class J2MixinBase(BaseMixin):
    def get_template_names(self):
        if hasattr(self, 'template_name') and self.template_name:
            tn = self.template_name
        else:
            namespace = resolve(self.request.path).namespace
            base = utils.camel_to_underline(self.__class__.__name__)
            tn = '%s/%s%s' % (namespace, base, getattr(settings, 'DEFAULT_TEMPLATE_EXT', '.html'))

        if self.request.is_ajax():
            tna = tn.split('.')
            tna[-2] = '%s_ajax' % tna[-2]
            return ['.'.join(tna)]

        return [tn]


class IndexView(J2MixinBase, TemplateView):
    def cmd_vote(self, request, *args, **kwargs):
        try:
            # poll = Poll.active_objects.get(date_close__gte=datetime.datetime.now(), state=True, pk=request.POST['pk'])
            poll = Poll.active_objects.get(state=True, pk=request.POST['pk'])

            if request.POST['method'] == 'vote':
                Vote.objects.create(poll=poll, session_id=self.request.session.session_key)
            else:
                Vote.objects.filter(poll=poll, session_id=self.request.session.session_key).delete()
                poll.save()

            return True, render_to_string('frontend/inc_polls.j2', self._context_populate())

        except Exception, e:
            logger.debug('vote error %s' % e)

        return False

    def _context_populate(self, context={}):
        # poll_qset = qset_to_dict(Poll.active_objects.filter(date_close__gte=datetime.datetime.now()))
        poll_qset = qset_to_dict(Poll.active_objects.all())

        for vote in Vote.objects.filter(session_id=self.request.session.session_key, poll__in=poll_qset.keys()):
            poll_qset[vote.poll.pk].is_voted = True

        context['poll_list'] = poll_qset.values()

        return context

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['article_list'] = Article.active_objects.all()[0:10]
        context['tag_list'] = Tag.objects.filter(num__gt=0)

        self._context_populate(context)

        return context

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

class ArticleDetail(J2MixinBase, DetailView):
    def get_object(self, queryset=None):
        try:
            return Article.active_objects.get(**{'slug_%s' % lang_get(): self.kwargs['slug']})
        except Exception, e:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['tag_list'] = context['object'].tag.all()

        return context


class TagArticleList(J2MixinBase, ListView):
    def get_queryset(self):
        return Article.objects.filter(tag=self.tag)

    def dispatch(self, request, *args, **kwargs):
        self.tag = Tag.objects.get(**{'slug_%s' % lang_get(): kwargs['slug']})

        return super(TagArticleList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TagArticleList, self).get_context_data(**kwargs)
        context['tag'] = self.tag

        return context


class CategoryArticleList(J2MixinBase, ListView):
    def get_queryset(self):
        return Article.objects.filter(category=self.category)

    def dispatch(self, request, *args, **kwargs):
        self.category = Category.objects.get(**{'slug_%s' % lang_get(): kwargs['slug']})
        return super(CategoryArticleList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryArticleList, self).get_context_data(**kwargs)

        context['category'] = self.category

        return context
