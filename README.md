# Tes Junior Programmer - FastPrint Indonesia

Aplikasi web manajemen produk sederhana yang dibangun menggunakan **Django** (Python) dan **MySQL**, mengintegrasikan data dari API FastPrint dengan autentikasi dinamis.

**Dibuat Oleh:** [Nama Lengkap Anda]

## 📋 Fitur Utama

1.  **Integrasi API Dinamis:**
    - Mengambil data dari API FastPrint.
    - Menangani autentikasi username/password berbasis waktu (MD5 Generator).
2.  **Manajemen Data (CRUD):**
    - **Create:** Tambah produk baru dengan validasi form (ID otomatis Safe Range mulai 12223).
    - **Read:** Menampilkan daftar produk dengan filter status "bisa dijual".
    - **Update:** Edit data produk (Harga & Nama).
    - **Delete:** Hapus produk dengan konfirmasi alert Javascript.
3.  **Tampilan Responsif:**
    - Menggunakan Bootstrap 5.
    - Format mata uang Rupiah (IDR).

## 🛠️ Teknologi yang Digunakan

- **Backend:** Django 4.x, Python 3.x
- **Database:** MySQL
- **Frontend:** HTML5, Bootstrap 5, Javascript
- **Tools:** Postman (Testing API), Git

## ⚙️ Cara Instalasi & Menjalankan

1.  **Clone Repository**

    ```bash
    git clone [https://github.com/username-anda/nama-repo.git](https://github.com/username-anda/nama-repo.git)
    cd nama-repo
    ```

2.  **Buat Virtual Environment**

    ```bash
    python -m venv env
    # Windows
    env\Scripts\activate
    # Mac/Linux
    source env/bin/activate
    ```

3.  **Install Library**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Database**
    - Buat database baru di MySQL (misal: `fastprint_db`).
    - Sesuaikan setting `DATABASES` di file `settings.py` (User/Password MySQL Anda).

5.  **Migrasi Database**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Jalankan Script Sinkronisasi API** (Untuk mengisi data awal)

    ```bash
    python manage.py sinkronisasi_api
    ```

7.  **Jalankan Server**
    ```bash
    python manage.py runserver
    ```
    Buka browser di `http://127.0.0.1:8000`

## 📸 Struktur Database

- **Produk:** (id_produk, nama_produk, harga, kategori_id, status_id)
- **Kategori:** (id_kategori, nama_kategori)
- **Status:** (id_status, nama_status)

---

_Dikembangkan untuk keperluan Tes Seleksi Programmer FastPrint._
