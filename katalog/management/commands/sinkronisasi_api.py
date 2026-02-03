from django.core.management.base import BaseCommand
from katalog.models import Produk, Kategori, Status # Sesuaikan 'katalog' dengan nama app Anda
import requests
import hashlib
from datetime import datetime

class Command(BaseCommand):
    help = 'Mengambil data dari API FastPrint dan menyimpannya ke MySQL'

    def handle(self, *args, **kwargs):
        # 1. SETUP AUTHENTICATION
        now = datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        year = now.strftime("%y") # 2 digit tahun (26)
        hour = now.strftime("%H")

        # Username: tesprogrammer + ddMMyy + C + HH
        username = f"tesprogrammer{day}{month}{year}C{hour}"
        
        # Password Mentah: bisacoding-dd-mm-yy
        raw_pass = f"bisacoding-{day}-{month}-{year}"
        password_md5 = hashlib.md5(raw_pass.encode()).hexdigest()

        self.stdout.write(f"Connecting with User: {username}...")

        # 2. REQUEST KE API
        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        payload = {'username': username, 'password': password_md5}
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data_json = response.json()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error Koneksi: {e}"))
            return

        # 3. PROSES DATA
        if data_json.get('error') == 0:
            items = data_json.get('data', [])
            count = 0
            
            for item in items:
                # Validasi sederhana: Lewati jika tidak ada nama produk
                if not item.get('nama_produk'):
                    continue

                # A. Simpan/Get Kategori
                kategori_obj, _ = Kategori.objects.get_or_create(
                    nama_kategori=item['kategori']
                )

                # B. Simpan/Get Status
                status_obj, _ = Status.objects.get_or_create(
                    nama_status=item['status']
                )

                # C. Validasi Harga (Pastikan angka)
                try:
                    harga_clean = int(item['harga'])
                except (ValueError, TypeError):
                    harga_clean = 0

                # D. Simpan Produk (Update jika ID sudah ada)
                Produk.objects.update_or_create(
                    id_produk=item['id_produk'],
                    defaults={
                        'nama_produk': item['nama_produk'],
                        'harga': harga_clean,
                        'kategori': kategori_obj,
                        'status': status_obj
                    }
                )
                count += 1
            
            self.stdout.write(self.style.SUCCESS(f"Sukses! {count} produk berhasil disimpan/diupdate."))
        else:
            self.stdout.write(self.style.ERROR(f"Gagal Login API: {data_json.get('ket')}"))