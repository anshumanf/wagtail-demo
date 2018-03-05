from django.utils import translation
from wagtailtinymce.rich_text import TinyMCERichTextArea
from django.conf import settings


class MyTinyMCE(TinyMCERichTextArea):
    def __init__(self, *args, **kwargs):
        translation.trans_real.activate(settings.LANGUAGE_CODE)

        kwargs.update({
            'buttons': [
                [
                    ['undo', 'redo'],
                    ['styleselect'],
                    ['bold', 'italic'],
                    ['bullist', 'numlist', 'outdent', 'indent'],
                    ['table'],
                    ['link', 'unlink'],
                    ['wagtaildoclink'],
                    ['pastetext', 'code', 'fullscreen'],
                ]
            ],
            'menus': False,
            'options': {
                'browser_spellcheck': True,
                'noneditable_leave_contenteditable': True,
                'language_load': True,
                'plugins': ['code'],
            },
        })

        super(MyTinyMCE, self).__init__(*args, **kwargs)
