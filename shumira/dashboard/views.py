from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, AboutUs
from .forms import NewItemForm, EditItemForm
from django.contrib.auth.decorators import login_required



# Dashboard View
@login_required
def dashboard(request):
    items = Item.objects.filter(is_expired=False).order_by('-date_created')[:3]
    return render(request, 'dashboard/dashboard.html', {'items': items})



# Item detail view
@login_required
def item_details(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'dashboard/item_details.html', {'item': item})


# Add new item view
@login_required
def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.creator = request.user
            item.save()
            return redirect('item-details', pk=item.id)
    else:
        form = NewItemForm()
    return render(request, 'dashboard/new_item.html', {'form': form, 'title': 'New Item'})


# Edit an item view
@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item-details', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'dashboard/edit_item.html', {'form': form, 'title': 'Edit Item'})


# Delete an Item view
@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        item.delete()
        return redirect('dashboard')
    return render(request, 'dashboard/delete_item.html', {'item': item})


# About Us page
def about_us(request):
    abouts = AboutUs.objects.all()
    return render(request, 'dashboard/about_us.html', {'abouts': abouts})