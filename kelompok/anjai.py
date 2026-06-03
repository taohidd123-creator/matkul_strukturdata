# INI KODINGAN SAYA TAOHID
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
    if "(Tgl " in v:  # Filter agar tidak dobel hitung nominalnya
        total_terpakai += data['weight']

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
    node_pusat = f"Dana: Rp {total_dana:,}"
    node_tanggal = f"Tgl {tanggal_pilihan}"
    node_kebutuhan = f"{kategori_kebutuhan} (Tgl {tanggal_pilihan})" 
    
    # Tambah node ke graf via class
    manajer.tambah_kebutuhan(node_pusat)
    manajer.tambah_kebutuhan(node_tanggal)
    manajer.tambah_kebutuhan(node_kebutuhan)
    
    # Hubungkan pusat ke tanggal dan tanggal ke kebutuhan
    manajer.add_hubungan(node_pusat, node_tanggal, bobot=dana_dialokasikan)
    manajer.add_hubungan(node_tanggal, node_kebutuhan, bobot=dana_dialokasikan)
    
    st.success(f"Berhasil menambahkan {kategori_kebutuhan} sebesar Rp {dana_dialokasikan:,} pada Tanggal {tanggal_pilihan}")
    # Simpan status bahwa data baru saja dimasukkan untuk trigger suara di bawah
    st.session_state.pemicu_suara = True

# INI PUNYA SI DAPIT ANJAII
# 3. Visualisasi Graf menggunakan Matplotlib
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


# 4. Tabel Detail Data & Audio Output di Paling Bawah
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
        
    # Trigger otomatis hanya jika baru saja menekan tombol 'Tambah ke Graf'
    elif st.session_state.get('pemicu_suara', False):
        teks_suara = f"Data berhasil diperbarui. Sisa dana bulanan anda saat ini adalah {sisa_dana} rupiah."
        fp = io.BytesIO()
        tts = gTTS(teks_suara, lang='id')
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3", autoplay=True)
        
        # Matikan pemicu setelah audio dimainkan agar tidak autoplay terus menerus saat berinteraksi dengan widget lain
        st.session_state.pemicu_suara = False