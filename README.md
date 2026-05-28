# Bisnis.com Crawler & Scraper

Proyek ini adalah sebuah web crawler dan scrape* yang dibangun menggunakan Python untuk mengekstrak artikel berita dari situs [bisnis.com](https://www.bisnis.com). Program ini berfungsi untuk memenuhi kebutuhan pengambilan data dengan keluaran format JSON yang berisi tautan (link), judul, isi artikel, dan tanggal terbit.

## Fungsi Dasar Crawler

Crawler ini beroperasi dalam dua mode utama:
1. Mode Backtrack: Mengambil dan menyaring daftar artikel berdasarkan rentang tanggal tertentu (start date hingga end date).
2. Mode Standard: Berjalan sebagai long-running process yang akan mengambil artikel terbaru secara berkala berdasarkan  waktu yang telah ditentukan, dan mencegah duplikasi data yang sudah diambil sebelumnya.

Semua hasil ekstraksi dari kedua mode akan disimpan ke dalam direktori /output_json.

## Cara Instalasi (Setup)

1. Install Python 3.
2. Clone repositori ini atau unduh kode sumber ke dalam satu direktori.
3. Buka terminal/command prompt dan arahkan ke direktori proyek.
4. Buat dan aktifkan virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
5. Instal pustaka (library) yang dibutuhkan:
   ```bash
   pip install -r requirements.txt

## Cara Menjalankan

1. Mode Backtrack:
   ```bash
   python run_backtrack.py --start [Tanggal mulai, format YYYY-MM-DD] --end [Tanggal akhir, format YYYY-MM-DD]

   Output: File JSON baru dengan format nama backtrack_YYYY-MM-DD_to_YYYY-MM-DD.json akan dibuat di dalam folder /output_json.
2. Mode Standard:
   ```bash
   python run_standard.py

   Tekan Ctrl + C di terminal untuk menghentikan proses.
   Output: Setiap kali ada artikel baru yang ditemukan pada siklus pengecekan, program akan membuat file JSON baru dengan format nama standard_latest_YYYYMMDD_HHMMSS.json di dalam folder /output_json.
3. Testing:
   ```bash
   python test_scraper.py

   Output: Akan muncul di terminal dengan struktur seperti JSON


## Penjelasan Arsitektur
Proyek ini menggunakan pola arsitektur Modular dengan pemisahan tugas (Separation of Concerns) yang jelas:
1. Modul Inti (base_scraper.py): Bertindak sebagai mesin penarik data (scraper) utama. Modul ini menangani semua interaksi dengan situs
   web, penguraian struktur HTML, logika pencarian elemen (link, title, content), dan fungsi konversi waktu ke format ISO 8601. Modul ini tidak mengeksekusi logika looping waktu atau filter tanggal secara mandiri.
2. run_backtrack.py: Bertugas mengatur input argumen terminal, memanggil modul inti, melakukan filterisasi artikel
   berdasarkan objek datetime, dan mengekspor hasilnya ke direktori output.
3. run_standard.py: Bertugas mengatur penjadwalan menggunakan modul schedule, menyimpan state sementara
   agar terhindar dari ekstraksi artikel yang berulang, memanggil modul inti, dan mengekspor data yang baru ke direktori output.
4. test_scraper.py: Berfungsi sebagai skrip validasi ringan selama tahap pengembangan. Modul ini memanggil fungsi utama dari 
   base_scraper.py dan mencetak sampel data langsung ke layar terminal menggunakan modul json. Tujuannya adalah untuk memverifikasi kelancaran request HTTP, keakuratan selektor HTML, dan format konversi tanggal tanpa perlu menjalankan logika perulangan atau penyimpanan file yang lebih kompleks.

## Link Video Technical Test
https://drive.google.com/file/d/1r4l58XpQUXL_JNYJ_prJnSPutNen0cYB/view?usp=sharing 