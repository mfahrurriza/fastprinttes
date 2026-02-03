# File: katalog/views.py (Update isinya)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk
from .forms import ProdukForm
from django.db.models import Max

def daftar_produk(request):
    produk_list = Produk.objects.filter(status__nama_status='bisa dijual')
    return render(request, 'index.html', {'produk_list': produk_list})

def tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            # Jangan save dulu ke DB, kita mau selipkan ID
            produk_baru = form.save(commit=False)
            
            # Cari ID paling besar yang ada di database saat ini
            max_id = Produk.objects.aggregate(Max('id_produk'))['id_produk__max']
            
            # Jika database kosong, mulai dari 1. Jika ada, tambah 1.
            if max_id is None:
                next_id = 1
            else:
                next_id = max_id + 1
            
            # Assign ID baru ke produk
            produk_baru.id_produk = next_id
            
            # Baru simpan beneran
            produk_baru.save()
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