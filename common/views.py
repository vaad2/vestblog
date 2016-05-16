import ujson

from django.core.urlresolvers import resolve
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import View

from . import utils

class BaseMixin(View):
    breadcrumbs = []

    def permission_check(self, request, *args, **kwargs):
        return None

    def get_breadcrumbs(self):
        return self.breadcrumbs

    def render_to_response(self, context, **response_kwargs):
        context['breadcrumbs'] = self.get_breadcrumbs()

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

    def get_template_names(self):
        if hasattr(self, 'template_name') and self.template_name:
            tn = self.template_name
        else:
            namespace = resolve(self.request.path).namespace
            base = utils.camel_to_underline(self.__class__.__name__)
            tn = '%s/%s.html' % (namespace, base)

        if self.request.is_ajax():
            tna = tn.split('.')
            tna[-2] = '%s_ajax' % tna[-2]
            return ['.'.join(tna)]

        return [tn]

    def json_handler_get(self):
        return ujson.dumps

    def _pre_init(self, request, *args, **kwargs):
        pass

    def _post_init(self, request, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        result = self.permission_check(request, *args, **kwargs)

        self.paginator_data = {}

        if not result is None:
            return result

        if 'pk' in request.REQUEST:
            kwargs['pk'] = request.REQUEST

        if 'slug' in request.REQUEST:
            kwargs['slug'] = request.REQUEST['slug']

        self._pre_init(request, *args, **kwargs)

        if 'cmd' in request.REQUEST:
            try:
                handler = getattr(self, 'cmd_%s' % request.REQUEST['cmd'].lower())
                result = handler(request, *args, **kwargs)
            except Exception, e:
                if request.is_ajax():
                    return self.json_handler_get()({'success': False, 'data': None, 'errors': e})
                else:
                    raise Http404(e)

        else:
            result = super(BaseMixin, self).dispatch(request, *args, **kwargs)

        # for ajax response
        if request.is_ajax() or 'cmd' in request.REQUEST:
            if isinstance(result, TemplateResponse):
                if not result.is_rendered:
                    result.render()
                success = True
                data = result.rendered_content
            elif isinstance(result, (list, tuple)):
                success, data = result
            else:
                success = result
                data = None

            errors = getattr(self, 'ajax_errors', {})

            return HttpResponse(self.json_handler_get()({'success': success,
                                            'data': data,
                                            'meta': getattr(self, 'meta', {}),
                                            'errors': errors}), content_type='application/json')

        return result