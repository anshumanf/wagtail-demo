from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import allow_without_attributes

from wagtail.contrib.modeladmin.options import modeladmin_register
from .admin import SimulationAdmin


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'code': allow_without_attributes,
    }


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(SimulationAdmin)
