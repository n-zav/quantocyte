from django.core.urlresolvers import reverse_lazy, reverse
from jqgrid import JqGrid
from .models import Item


class ItemGrid(JqGrid):
    model = Item  # could also be a queryset
    fields = ['id', 'name']  # optional
    url = reverse_lazy('grid_handler')
    caption = 'Items Grid'  # optional
    colmodel_overrides = {
        'id': {'editable': False, 'key': True, 'width': 10},
        'name': {'editable': True, },
    }

    def get_default_config(self):
        config = super(ItemGrid, self).get_default_config()
        config['editurl'] = str(reverse('grid_crud'))
        return config
