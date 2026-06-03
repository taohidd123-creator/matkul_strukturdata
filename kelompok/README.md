📊 Visualisasi Alokasi Dana Bulanan Berbasis Graf
Aplikasi berbasis web menggunakan Streamlit dan NetworkX untuk membantu pengguna mengelola serta memvisualisasikan alokasi dana bulanan dalam bentuk struktur graf (jaringan). Aplikasi ini juga dilengkapi dengan fitur Text-to-Speech (TTS) untuk memberikan ringkasan saldo secara audio.

🚀 Fitur Utama
1. Manajemen Dana Dinamis: Input total dana bulanan dan lacak sisa saldo secara real-time.
2. Visualisasi Graf Jaringan: Menampilkan hubungan antara total dana, tanggal transaksi, dan kategori pengeluaran menggunakan NetworkX dan Matplotlib.
3. Kalender Otomatis: Sistem mendeteksi jumlah hari dalam bulan dan tahun yang dipilih (termasuk tahun kabisat).
4. Output Audio (TTS): Menggunakan gTTS untuk memberikan pembaruan status sisa saldo secara suara setelah data ditambahkan.
5. Tabel Detail: Menampilkan rincian hubungan antar node dan nominal alokasi dana secara tabular.

🛠️ Teknologi yang Digunakan
1. Python: Bahasa pemrograman utama.
2. Streamlit: Framework untuk membangun antarmuka web.
3. NetworkX: Library untuk manipulasi dan visualisasi struktur graf.
4. Matplotlib: Rendering visualisasi graf ke dalam format gambar.
5. gTTS (Google Text-to-Speech): Mengubah teks laporan saldo menjadi suara.
6. Calendar & Datetime: Pengolahan logika penanggalan.

📂 Struktur File
1. frontend.py: File utama Streamlit yang menangani antarmuka pengguna (UI) dan logika interaksi.
2. kodingannya.py: Backend berupa class KebutuhanSehariHari yang mengelola struktur data graf menggunakan NetworkX.

⚙️ Cara Menjalankan
1. Instalasi Library Pastikan Anda sudah menginstal library yang diperlukan melalui terminal/command prompt: pip install streamlit networkx matplotlib gTTS
2. Menjalankan Aplikasi Jalankan perintah berikut di folder tempat file berada: streamlit run frontend.py

📖 Cara Penggunaan
1. Masukkan Total Dana Bulanan pada sidebar.
2. Pilih Tahun dan Bulan untuk menyesuaikan jumlah hari.
3. Di panel utama, masukkan Tanggal, Nama Kebutuhan, dan Nominal Dana.
4. Klik "Tambah ke Graf".
5. Graf akan terbentuk secara otomatis yang menghubungkan:
6. Pusat Dana ➔ Tanggal ➔ Kebutuhan.
7. Dengarkan status saldo melalui fitur audio di bagian bawah halaman.

📝 Catatan Pengembangan
Proyek ini memisahkan logika bisnis (Backend) dan tampilan (Frontend) untuk memastikan kode tetap rapi dan mudah dikembangkan di kemudian hari (seperti menambahkan fitur hapus node atau penyimpanan database).