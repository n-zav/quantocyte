from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from .grids import ItemGrid
from .models import Item


class HomePageView(TemplateView):
    template_name = "home.html"


@login_required
def grid_handler(request):
    # handles pagination, sorting and searching
    grid = ItemGrid()
    return HttpResponse(grid.get_json(request), content_type="application/json")


@login_required
def grid_config(request):
    # build a config suitable to pass to jqgrid constructor
    grid = ItemGrid()
    return HttpResponse(grid.get_config(), content_type="application/json")


@login_required
def grid_crud(request):
    operation = request.POST.get('oper', '')
    name = request.POST.get('name', '')
    id = request.POST.get('id', '')
    if operation == 'add':
        item = Item(name=name)
        item.save()
    elif operation == 'del':
        item = Item.objects.get(id=id)
        if item is not None:
            item.delete()
    elif operation == 'edit':
        item = Item.objects.get(id=id)
        if item is not None:
            item.name = name
            item.save()
    return HttpResponse({}, content_type="application/json")


@login_required
def grid_view(request):
    return render_to_response('grid.html', {},
                              context_instance=RequestContext(request))
