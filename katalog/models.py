from django.db import models

class Kategori(models.Model):
    # AutoField 'id_kategori' otomatis dibuat Django (sebagai primary key)
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        db_table = 'Kategori'

    def __str__(self):
        return self.nama_kategori

class Status(models.Model):
    # AutoField 'id_status' otomatis dibuat Django
    nama_status = models.CharField(max_length=100)

    class Meta:
        db_table = 'Status'
    
    def __str__(self):
        return self.nama_status

class Produk(models.Model):
    # Kita gunakan id_produk dari API sebagai Primary Key agar sinkron
    id_produk = models.IntegerField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=15, decimal_places=0)
    
    # Relasi ke tabel Kategori dan Status (Foreign Key)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='produk')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='produk')

    class Meta:
        db_table = 'Produk'

    def __str__(self):
        return self.nama_produk