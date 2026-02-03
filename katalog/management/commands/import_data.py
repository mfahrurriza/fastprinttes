import requests
import hashlib
from datetime import datetime
from django.core.management.base import BaseCommand
from katalog.models import Produk, Kategori, Status # Sesuaikan nama app

class Command(BaseCommand):
    help = 'Mengambil data dari API FastPrint'

    def handle(self, *args, **kwargs):
        # 1. Generate Username & Password Dinamis
        now = datetime.now()
        
        # Format Password: bisacoding-d-m-yy (contoh: bisacoding-2-2-26)
        # Note: Pastikan format tanggal sesuai timezone server jika perlu
        password_raw = f"bisacoding-{now.day:02d}-{now.month:02d}-{str(now.year)[-2:]}"
        password_md5 = hashlib.md5(password_raw.encode()).hexdigest()

        # Format Username: tesprogrammerddMMyyCHH
        # Contoh: tesprogrammer020226C09 (C lalu Jam format 24)
        username = f"tesprogrammer{now.strftime('%d%m%y')}C{now.strftime('%H')}"

        self.stdout.write(f"Mencoba login dengan User: {username}")

        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        payload = {
            'username': username,
            'password': password_md5
        }

        # 2. Request ke API
        try:
            response = requests.post(url, data=payload)
            print(response.json())
            
            if response.status_code == 200:
                data = response.json()
                
                # Cek apakah response error
                if data.get('error') == 1: # Asumsi struktur error
                    self.stdout.write(self.style.ERROR(f"API Error: {data.get('ket')}"))
                    return

                # 3. Simpan Data (Soal No. 3)
                # API ini biasanya me-return list produk campur
                # Kita harus handle Kategori & Status dulu agar tidak Error ForeignKey
                
                items = data.get('data', []) # Sesuaikan key JSON nanti
                
                # Ganti baris ini:
                # for item in item: 

                # Menjadi ini:
                for item in items:
                    # 1. Pastikan Kategori & Status ada
                    kat_obj, _ = Kategori.objects.get_or_create(nama_kategori=item['kategori'])
                    stat_obj, _ = Status.objects.get_or_create(nama_status=item['status'])

                    # 2. Simpan Produk (Gunakan update_or_create agar tidak duplikat)
                    Produk.objects.update_or_create(
                        id_produk=item['id_produk'],
                        defaults={
                            'nama_produk': item['nama_produk'],
                            'harga': item['harga'],
                            'kategori': kat_obj,
                            'status': stat_obj,
                        }
                    )
                                
                self.stdout.write(self.style.SUCCESS(f'Berhasil import {len(items)} data!'))
            
            else:
                self.stdout.write(self.style.ERROR('Gagal connect ke API'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Terjadi kesalahan: {e}"))