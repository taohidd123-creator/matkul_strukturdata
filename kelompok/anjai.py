import io
from gtts import gTTS
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
from kodingannya import KebutuhanSehariHari

# Set halaman Streamlit
st.set_page_config(page_title="Visualisasi Kebutuhan Graf", layout="wide")
st.title("📊 Visualisasi Alokasi Dana Bulanan Berbasis Graf")

st.markdown(
    """
    **Penjelasan Fitur**
    - **Tambah Kebutuhan:** Masukkan nama kebutuhan, tanggal, dan nominal untuk menambah alokasi ke graf.
    - **Visualisasi Graf:** Menampilkan hubungan total dana -> tanggal -> kebutuhan beserta bobot nominal.
    - **Tabel Detail:** Menunjukkan daftar relasi dan jumlah alokasi untuk pengecekan cepat.
    - **Audio Status:** Mengeluarkan rekaman suara sisa dana setelah data ditambahkan.
    - **Hapus Kebutuhan:** Menghapus kebutuhan yang tidak dibutuhkan lagi beserta relasinya dari graf.
    """
)

# 1. Inisialisasi Class ke dalam Session State agar data tidak hilang saat refresh
if 'manajer_kebutuhan' not in st.session_state:
    st.session_state.manajer_kebutuhan = KebutuhanSehariHari()

manajer = st.session_state.manajer_kebutuhan

# Layout Input di Sidebar
st.sidebar.header("⚙️ Pengaturan Dana & Tanggal")

# Input Uang Bulanan
total_dana = st.sidebar.number_input("Total Dana Bulanan (Rp)", min_value=0, value=3000000, step=50000)

# Pilih Bulan dan Tahun untuk menentukan jumlah hari otomatis
tahun_sekarang = datetime.now().year
bulan_sekarang = datetime.now().month

pilihan_tahun = st.sidebar.selectbox("Pilih Tahun", range(tahun_sekarang, tahun_sekarang + 5), index=0)
pilihan_bulan = st.sidebar.selectbox(
    "Pilih Bulan", 
    range(1, 13), 
    index=bulan_sekarang - 1,
    format_func=lambda x: calendar.month_name[x]
)

# Hitung jumlah hari otomatis (menangani 28, 29, 30, 31 hari)
_, jumlah_hari = calendar.monthrange(pilihan_tahun, pilihan_bulan)
st.sidebar.info(f"📅 Jumlah hari pada bulan ini: {jumlah_hari} hari")

# --- HITUNG SISA DANA ---
total_terpakai = 0
for u, v, data in manajer.get_kebutuhan_dengan_bobot():
    # Hitung hanya untuk edge yang berhubungan dengan node kebutuhan
    # (node kebutuhan mengandung substring "(Tgl ") sehingga kita
    # memeriksa kedua ujung edge untuk menghindari ketergantungan
    # pada urutan (u, v) yang tidak deterministik.
    if "(Tgl " in str(u) or "(Tgl " in str(v):
        total_terpakai += data.get('weight', 0)

sisa_dana = total_dana - total_terpakai

# Tampilkan informasi sisa dana di sidebar
st.sidebar.metric(label="💰 Sisa Dana Bulanan", value=f"Rp {sisa_dana:,}")
if sisa_dana < 0:
    st.sidebar.error("⚠️ Alokasi dana melebihi total uang bulanan!")


# 2. Form Input Kebutuhan Harian
st.subheader("📍 Alokasikan Kebutuhan per Tanggal")
with st.form("form_kebutuhan"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tanggal_pilihan = st.selectbox("Pilih Tanggal", range(1, jumlah_hari + 1))
    with col2:
        kategori_kebutuhan = st.text_input("Nama Kebutuhan (cth: Makan, Bensin, Kost)", placeholder="Makan")
    with col3:
        dana_dialokasikan = st.number_input("Nominal Dana (Rp)", min_value=0, value=50000, step=5000)
        
    submit_button = st.form_submit_button(label="Tambah ke Graf")

# Proses ketika tombol form ditekan
if submit_button and kategori_kebutuhan:
    node_pusat = "Dana Bulanan"
    node_tanggal = f"Tgl {tanggal_pilihan}"
    node_kebutuhan_base = f"{kategori_kebutuhan} (Tgl {tanggal_pilihan})"
    node_kebutuhan = node_kebutuhan_base
    counter = 1

    # Jika kebutuhan sama sudah ada, buat label baru agar setiap input tetap ditambahkan.
    while node_kebutuhan in manajer.get_all_kebutuhan():
        counter += 1
        node_kebutuhan = f"{kategori_kebutuhan} ({counter}) (Tgl {tanggal_pilihan})"
    
    # Tambah node ke graf via class
    manajer.tambah_kebutuhan(node_pusat)
    manajer.tambah_kebutuhan(node_tanggal)
    manajer.tambah_kebutuhan(node_kebutuhan)
    
    # Hubungkan pusat ke tanggal dan tanggal ke kebutuhan
    manajer.add_hubungan(node_pusat, node_tanggal, bobot=dana_dialokasikan)
    manajer.add_hubungan(node_tanggal, node_kebutuhan, bobot=dana_dialokasikan)
    
    st.success(f"Berhasil menambahkan {kategori_kebutuhan} sebesar Rp {dana_dialokasikan:,} pada Tanggal {tanggal_pilihan}")
    # Tidak lagi memicu audio otomatis; audio hanya diputar lewat tombol manual


# 3. Hapus Kebutuhan
st.subheader("🗑️ Hapus Kebutuhan")
st.caption("Hapus item kebutuhan yang sudah tidak dibutuhkan lagi. Node tersebut akan dihapus dari graf beserta semua relasinya.")

kebutuhan_opsi = sorted([node for node in manajer.get_all_kebutuhan() if "(Tgl " in node])
if kebutuhan_opsi:
    pilihan_hapus_kebutuhan = st.selectbox("Pilih Kebutuhan untuk Dihapus", kebutuhan_opsi)
    if st.button("Hapus Kebutuhan"):
        if manajer.hapus_kebutuhan(pilihan_hapus_kebutuhan):
            st.success(f"Berhasil menghapus {pilihan_hapus_kebutuhan} dari alokasi dana.")
            # Gunakan experimental_rerun jika tersedia; jika tidak, hentikan eksekusi
            # agar Streamlit merender ulang di interaksi selanjutnya.
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.stop()
        else:
            st.warning("Kebutuhan tidak ditemukan atau sudah dihapus.")
else:
    st.info("Belum ada kebutuhan yang bisa dihapus. Tambahkan kebutuhan terlebih dahulu.")


# 4. Visualisasi Graf menggunakan Matplotlib
st.subheader("🌐 Network Graph Kebutuhan")

G = manajer.get_kebutuhan()

if len(G.nodes()) > 0:
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue", ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, edge_color="gray", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax)
    
    labels_bobot = nx.get_edge_attributes(G, 'weight')
    labels_formatted = {k: f"Rp {v:,}" for k, v in labels_bobot.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_formatted, font_size=9, font_color="red", ax=ax)
    
    plt.axis('off')
    st.pyplot(fig)
else:
    st.info("Belum ada data yang dimasukkan. Silakan isi form di atas untuk membentuk graf.")


# 5. Tabel Detail Data & Audio Output di Paling Bawah
if len(G.nodes()) > 0:
    st.subheader("📋 Daftar Hubungan & Bobot")
    data_tabel = []
    for u, v, data in manajer.get_kebutuhan_dengan_bobot():
        data_tabel.append({"Dari": u, "Ke": v, "Alokasi Dana": f"Rp {data['weight']:,}"})
    st.table(data_tabel)

    # --- BAGIAN PALING BAWAH: AUDIO REKAP SISA SALDO ---
    st.write("---")
    st.subheader("🔊 Audio Status Saldo")
    
    # Tombol manual jika user ingin mendengarkan ulang sisa saldo kapan saja
    if st.button("📢 Dengarkan Sisa Saldo"):
        teks_suara = f"Sisa dana bulanan anda saat ini adalah {sisa_dana} rupiah."
        fp = io.BytesIO()
        tts = gTTS(teks_suara, lang='id')
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3", autoplay=True)
        
    # Audio hanya diputar bila pengguna menekan tombol di atas.