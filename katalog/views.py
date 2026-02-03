# File: katalog/views.py (Update isinya)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk
from .forms import ProdukForm

def daftar_produk(request):
    produk_list = Produk.objects.filter(status__nama_status='bisa dijual')
    return render(request, 'index.html', {'produk_list': produk_list})

def tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daftar_produk')
    else:
        form = ProdukForm()
    
    return render(request, 'form_produk.html', {'form': form, 'title': 'Tambah Produk'})

def edit_produk(request, id_produk):
    produk = get_object_or_404(Produk, id_produk=id_produk)
    
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('daftar_produk')
    else:
        form = ProdukForm(instance=produk)
        
    return render(request, 'form_produk.html', {'form': form, 'title': 'Edit Produk'})

def hapus_produk(request, id_produk):
    produk = get_object_or_404(Produk, id_produk=id_produk)
    produk.delete()
    return redirect('daftar_produk')