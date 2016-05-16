# from django.db.models.fields.files import FieldFile
from django.forms import  widgets
from django.forms.widgets import ClearableFileInput, CheckboxInput, FILE_INPUT_CONTRADICTION

from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

from sorl.thumbnail.fields import ImageField, ImageFormField
from common.utils import image_from_url_get_2
#class ExTextInput(TextInput):
#    def render(self, name, value, attrs=None):
#        if value is None:
#            value = ''
#        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
#        if value != '':
#            # Only add the 'value' attribute if a value is non-empty.
#            final_attrs['value'] = force_unicode(self._format_value(value))
#        return mark_safe(u'<input style="width:250" %s />' % flatatt(final_attrs))


class ExClearableFileInput(ClearableFileInput):
    template_with_initial = u'''<span class="ex-image-form-field">
        <span class="block-initial">%(initial)s %(clear_template)s</span>
        <span class="block-inputs">%(input_text)s: %(input)s</span>
    </span>'''
    template_with_clear = u'''&nbsp; %(clear)s %(clear_checkbox_label)s'''

    def image_url_name(self, name):
        return '%s-image-url' % name

    def render(self, name, value, attrs = None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = u'%(input)s or url: %(input_img_url)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)
        substitutions['input_img_url'] = widgets.TextInput(attrs = {'style' : 'width:320px'}).render(conditional_escape(self.image_url_name(name)), '')

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            #            substitutions['initial'] = (u'<a href="%s">%s</a>'
            #                                        % (escape(value.url),
            try:
                from django.conf import settings
#                img_url = get_thumbnail('%s/../%s' % (settings.PROJECT_ROOT, value.url), '140x140', crop = 'center top').url
                img_url = get_thumbnail('%s/../%s' % (settings.PROJECT_ROOT, value.url), '140x140').url
                substitutions['initial'] = (u'<a href="%s" class="image-href"><img class="image" src="%s" width="140"/></a>'
                                            % (escape(value.url),
                                               escape(img_url)))
            except BaseException, e:
                substitutions['initial'] = (u'<a href="%s" class="image-href"><img class="image" src="%s" width="140"/></a>'
                                            % (escape(value.url),
                                               escape(value.url)))

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                #                substitutions['img_url_name'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        upload = super(ClearableFileInput, self).value_from_datadict(data, files, name)
        #        InMemoryUploadedFile
        image_url = widgets.TextInput().value_from_datadict(data, files, self.image_url_name(name))

        if not upload and image_url:
            try:
                upload = image_from_url_get_2(image_url)
            except BaseException,e:
                uplod = ''
        if not self.is_required and CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
                # False signals to clear any existing value, as opposed to just None
            return False
        return upload


class ExImageFormField(ImageFormField):
    widget = ExClearableFileInput


#class ExFieldFile(FieldFile):
#    def __unicode__(self):
#        if hasattr(self, 'url'):
#            try:
#                from django.conf import settings
#                img_url = get_thumbnail('%s/../%s' % (settings.PROJECT_ROOT, self.url), '140x140').url
#                return mark_safe('<img url="%s"/>' % img_url)
#            except BaseException, e:
#                return self.url
#        return ''

class ExImageField(ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': ExImageFormField}
        defaults.update(kwargs)
        return super(ExImageField, self).formfield(**defaults)


class AdminExImageFieldMixin(object):
    formfield_overrides = {
        ExImageField: {'widget': ExClearableFileInput},
        }
    class Media:
        css = {
            'all': ['/static/css/ex_widgets.css']
        }
