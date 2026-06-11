📊 Visualisasi Alokasi Dana Bulanan Berbasis Graf Aplikasi berbasis web menggunakan Streamlit dan NetworkX untuk membantu pengguna mengelola serta memvisualisasikan alokasi dana bulanan dalam bentuk struktur graf (jaringan). Aplikasi ini juga dilengkapi dengan fitur Text-to-Speech (TTS) untuk memberikan ringkasan saldo secara audio.

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
frontend.py: File utama Streamlit yang menangani antarmuka pengguna (UI) dan logika interaksi.
kodingannya.py: Backend berupa class KebutuhanSehariHari yang mengelola struktur data graf menggunakan NetworkX.

⚙️ Cara Inisiasi dan Menjalankan
1. Clone Repositori​Buka terminal atau command prompt, lalu jalankan perintah berikut untuk mengkloning proyek ini ke komputer Anda: git clone https://github.com/username/nama-repositori.git cd nama-repositori
2. Instalasi Library​Pastikan Python sudah terinstal, lalu pasang semua dependencies yang diperlukan dengan menjalankan perintah: pip install streamlit networkx matplotlib gTTS
3. Menjalankan Aplikasi​Jalankan server Streamlit dengan perintah berikut di dalam folder proyek: streamlit run frontend.py Setelah perintah dijalankan, aplikasi akan otomatis terbuka di browser default Anda (biasanya di alamat http://localhost:8501).

​📖 Panduan Penggunaan Aplikasi​Setelah aplikasi terbuka di browser, Anda dapat mengikuti langkah-langkah berikut:
1. Pengaturan Awal (Sidebar)
​2. Masukkan Total Dana Bulanan yang Anda miliki pada kolom input di sidebar sebelah kiri.​- Pilih Tahun dan Bulan anggaran. Sistem akan otomatis menyesuaikan batas maksimum hari pada bulan tersebut.
3. Input Data Alokasi Dana (Panel Utama)​- Tentukan Tanggal transaksi/alokasi.
​4. Isi Nama Kebutuhan (misal: Makanan, Listrik, Kost).​- Masukkan Nominal Dana yang dialokasikan untuk kebutuhan tersebut.
​5. Klik tombol "Tambah ke Graf".
6. Membaca Hasil Visualisasi
7. Graf Jaringan: Perhatikan visualisasi graf yang terbentuk secara otomatis. Struktur hubungan akan mengalir dari: Pusat Dana (Total) ➔ Tanggal Transaksi ➔ Nama Kebutuhan
​8. Tabel Rincian: Lihat tabel di bagian bawah untuk melihat detail hubungan antar node beserta nominal pastinya dalam bentuk tabular.
9. Fitur Audio (TTS)
​10. Setiap kali Anda berhasil menambahkan data, sisa saldo akan dihitung ulang.​- Dengarkan pembaruan status sisa saldo Anda secara langsung melalui pemutar audio gTTS yang muncul di bagian bawah halaman.

📝 Catatan Pengembangan Proyek ini memisahkan logika bisnis (Backend) dan tampilan (Frontend) untuk memastikan kode tetap rapi dan mudah dikembangkan di kemudian hari (seperti menambahkan fitur hapus node atau penyimpanan database).
