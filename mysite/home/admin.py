from wagtail.contrib.modeladmin.options import ModelAdmin
from .models import SimulationExample


class SimulationAdmin(ModelAdmin):
    model = SimulationExample
    # menu_label = 'Simulation'  # ditch this to use verbose_name_plural from model
    menu_icon = 'code'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'universe', 'language', 'code')
    list_filter = ('universe', 'language')
    search_fields = ('name', 'universe', 'language', 'code')
