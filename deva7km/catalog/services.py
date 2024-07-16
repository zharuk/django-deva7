# catalog/services.py

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import PreOrder
from .forms import PreOrderForm
from .utils import notify_preorder_change


def handle_preorder_form(request, pk=None):
    if pk:
        preorder = get_object_or_404(PreOrder, pk=pk)
    else:
        preorder = PreOrder()

    if request.method == 'POST':
        form = PreOrderForm(request.POST, instance=preorder)
        if form.is_valid():
            preorder = form.save(commit=False)
            if request.user.is_authenticated:
                preorder.last_modified_by = request.user
            preorder.save()
            notify_preorder_change(sender=PreOrder, instance=preorder,
                                   event_type='preorder_saved' if pk is None else 'preorder_updated')
            return redirect('preorder_list')
    else:
        form = PreOrderForm(instance=preorder)

    return form


def toggle_preorder_status(request, field):
    if request.method == 'POST':
        data = json.loads(request.body)
        preorder_id = data.get('id')
        status = data.get('status')

        preorder = get_object_or_404(PreOrder, id=preorder_id)
        setattr(preorder, field, status)
        preorder.save()

        notify_preorder_change(sender=PreOrder, instance=preorder, event_type='preorder_updated')
        return JsonResponse({'status': 'success'})
