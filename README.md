# Sistem Manajemen Inventaris - PT Telkom Indonesia
![screenshot](https://github.com/user-attachments/assets/f41c567c-fb3d-4b99-9570-1914279976aa)

## Fitur Utama
-  Authentikasi Pengguna (Login & Registrasi)
- Dashboard dengan ringkasan statistik
- Manajemen Penuh (CRUD) untuk Data Barang dan Kategori
- Pelacakan Barang Masuk dan Barang Keluar
- Log Aktivitas untuk semua perubahan data
- Pencarian dan Filter data barang
- Desain Responsif dengan Sidebar "Push Content"

## Teknologi yang Digunakan
- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite
- **Manajemen Sesi**: Flask-Login
- **Formulir**: Flask-WTF

## Cara Menjalankan Proyek
1.  **Clone repository ini:**
    ```bash
    git clone [URL_GITHUB_ANDA]
    ```
2.  **Masuk ke direktori proyek:**
    ```bash
    cd [NAMA_FOLDER_PROYEK]
    ```
3.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Mac/Linux
    .\venv\Scripts\activate  # Untuk Windows
    ```
4.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Jalankan aplikasi:**
    ```bash
    python main.py
    ```
Aplikasi akan berjalan di `http://127.0.0.1:5000`.
