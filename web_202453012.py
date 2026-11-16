"""
Form Audit Sistem Informasi - COBIT 5 (Streamlit)
PT Dagang Nusantara Digital
Nama : Muhamad Ulil Absor | NIM : 202453012 | Kelas : B
Jalankan dengan:  streamlit run web_202453012.py
"""
import io
import base64

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---------------------------------------------------------------------------
# DATA FORMULIR AUDIT
# ---------------------------------------------------------------------------
PROFIL = {
    "nama": "Muhamad Ulil Absor",
    "nim": "202453012",
    "kelas": "B",
    "mata_kuliah": "Audit Sistem Informasi",
    "perusahaan": "PT Dagang Nusantara Digital",
    "industri": "E-Commerce / Marketplace Online",
    "deskripsi": (
        "Platform marketplace yang mempertemukan jutaan penjual dan pembeli, dilengkapi "
        "layanan pembayaran digital dan logistik terintegrasi. Sistem beroperasi 24/7, "
        "menangani puluhan ribu transaksi per jam (lonjakan saat promo besar seperti "
        "Harbolnas), serta mengelola data pribadi dan data pembayaran pelanggan skala besar."
    ),
    "fokus_audit": (
        "Mengevaluasi tata kelola TI, ketersediaan dan keandalan platform, serta kepatuhan "
        "keamanan data pelanggan terhadap regulasi (UU PDP, ketentuan sistem pembayaran, "
        "dan standar keamanan data)."
    ),
}

DOMAIN = {
    "EDM": "Evaluate, Direct and Monitor",
    "APO": "Align, Plan and Organize",
    "BAI": "Build, Acquire and Implement",
    "DSS": "Deliver, Service and Support",
    "MEA": "Monitor, Evaluate and Assess",
}
URUTAN_DOMAIN = ["EDM", "APO", "BAI", "DSS", "MEA"]

# ---------------------------------------------------------------------------
# 2. SKALA PENILAIAN (1-5)
# ---------------------------------------------------------------------------
LABEL_SKOR = {1: "Sangat Buruk", 2: "Buruk", 3: "Cukup", 4: "Baik", 5: "Sangat Baik"}

SKALA_TEMPLATE = {
    1: "{t} tidak ada atau sama sekali tidak sesuai dengan tujuan organisasi.",
    2: "{t} belum sepenuhnya mendukung tujuan organisasi dan standar perusahaan.",
    3: "{t} sesuai sebagian dengan tujuan organisasi namun belum konsisten.",
    4: "{t} selaras dengan sebagian besar tujuan organisasi dan dilakukan konsisten.",
    5: "{t} sepenuhnya mendukung dan mengarahkan organisasi mencapai tujuannya.",
}

# Jawaban tiap pertanyaan audit dan bobot nilainya
OPSI_JAWABAN = ["Belum dinilai", "Tidak", "Sebagian", "Ya"]
NILAI_JAWABAN = {"Tidak": 0.0, "Sebagian": 0.5, "Ya": 1.0}

# ---------------------------------------------------------------------------
# 3. KOMPONEN AUDIT (15 komponen) beserta pertanyaan audit
# ---------------------------------------------------------------------------
KOMPONEN = {
    "EDM01": {
        "nama": "Evaluasi dan Pengarahan Tata Kelola TI", "domain": "EDM",
        "topik": "Pengelolaan kerangka tata kelola TI",
        "fokus": "Memastikan tata kelola TI selaras dengan tujuan perusahaan, efektif, efisien, dan mendukung pertumbuhan bisnis marketplace.",
        "pertanyaan": [
            "Apakah perusahaan memiliki kerangka tata kelola TI formal (misalnya komite pengarah TI atau IT Steering Committee) yang terdokumentasi dan disahkan direksi?",
            "Apakah peran, tanggung jawab, dan wewenang pengambilan keputusan TI antara direksi, manajemen, dan tim TI telah didefinisikan dengan jelas?",
            "Seberapa sering direksi meninjau keselarasan strategi TI dengan tujuan bisnis perusahaan?",
            "Apakah terdapat mekanisme untuk menyelesaikan konflik prioritas antara kebutuhan bisnis dan kemampuan TI?",
            "Apakah efektivitas kerangka tata kelola TI dievaluasi secara berkala dan hasilnya ditindaklanjuti?",
        ],
    },
    "EDM02": {
        "nama": "Evaluasi Penyampaian Nilai Investasi TI", "domain": "EDM",
        "topik": "Evaluasi investasi TI",
        "fokus": "Memastikan setiap alokasi anggaran TI memberikan nilai maksimal dan manfaat strategis bagi layanan marketplace.",
        "pertanyaan": [
            "Apakah setiap usulan investasi TI disertai business case yang memuat biaya, manfaat, dan risiko?",
            "Apakah terdapat indikator yang terukur (misalnya ROI, peningkatan konversi, atau penurunan biaya operasional) untuk menilai manfaat investasi TI?",
            "Apakah investasi TI yang telah berjalan ditinjau ulang untuk memastikan manfaat yang dijanjikan benar-benar tercapai?",
            "Apakah proses persetujuan anggaran TI melibatkan pihak bisnis dan keuangan secara transparan?",
            "Apakah investasi TI yang tidak memberikan nilai dapat dihentikan atau dialihkan sesuai prosedur yang jelas?",
        ],
    },
    "EDM03": {
        "nama": "Evaluasi dan Pengarahan Manajemen Risiko TI", "domain": "EDM",
        "topik": "Manajemen risiko TI",
        "fokus": "Mengidentifikasi, menganalisis, dan memitigasi risiko terhadap data pelanggan dan ketersediaan platform.",
        "pertanyaan": [
            "Apakah perusahaan memiliki kebijakan dan kerangka manajemen risiko TI yang disetujui direksi?",
            "Apakah penilaian risiko TI (risk assessment) dilakukan secara berkala, termasuk risiko kebocoran data dan gangguan layanan saat lonjakan transaksi?",
            "Apakah selera risiko (risk appetite) dan toleransi risiko TI telah ditetapkan dan dikomunikasikan?",
            "Apakah terdapat risk register yang diperbarui dan setiap risiko memiliki pemilik serta rencana mitigasi?",
            "Apakah risiko TI berdampak tinggi dilaporkan kepada direksi secara tepat waktu?",
        ],
    },
    "APO01": {
        "nama": "Pendefinisian Kebijakan dan Prosedur TI", "domain": "APO",
        "topik": "Pendefinisian kebijakan TI",
        "fokus": "Memastikan seluruh prosedur manajemen operasional dan keamanan TI terdefinisi dengan jelas.",
        "pertanyaan": [
            "Apakah perusahaan memiliki dokumen kebijakan TI dan keamanan informasi yang lengkap, mutakhir, dan disahkan manajemen?",
            "Apakah kebijakan dan prosedur TI telah dikomunikasikan kepada seluruh karyawan dan pihak ketiga terkait?",
            "Apakah kebijakan ditinjau dan diperbarui secara berkala atau saat terjadi perubahan regulasi dan teknologi?",
            "Apakah terdapat prosedur operasional baku (SOP) untuk proses kritis seperti pengelolaan akses, pencadangan, dan penanganan insiden?",
            "Apakah kepatuhan karyawan terhadap kebijakan TI dipantau dan pelanggarannya ditindak?",
        ],
    },
    "APO02": {
        "nama": "Perencanaan Strategi TI", "domain": "APO",
        "topik": "Perencanaan strategi TI",
        "fokus": "Menyusun peta jalan (roadmap) teknologi yang proaktif untuk mendukung visi dan misi jangka panjang perusahaan.",
        "pertanyaan": [
            "Apakah perusahaan memiliki rencana strategis TI (IT Strategic Plan) yang terdokumentasi dan selaras dengan strategi bisnis?",
            "Apakah terdapat roadmap teknologi jangka menengah dan panjang (misalnya migrasi cloud, personalisasi berbasis AI, dan penguatan keamanan)?",
            "Apakah rencana strategis TI disusun dengan melibatkan unit bisnis dan manajemen puncak?",
            "Apakah perkembangan teknologi dan tren pasar e-commerce dipantau untuk memperbarui strategi TI?",
            "Apakah pencapaian rencana strategis TI diukur dan ditinjau secara berkala?",
        ],
    },
    "APO03": {
        "nama": "Pengelolaan Arsitektur Sistem Informasi", "domain": "APO",
        "topik": "Pengelolaan arsitektur sistem",
        "fokus": "Memastikan interoperabilitas dan integrasi antar sistem informasi melalui standarisasi arsitektur data dan aplikasi.",
        "pertanyaan": [
            "Apakah perusahaan memiliki dokumentasi arsitektur enterprise (bisnis, data, aplikasi, dan infrastruktur) yang terkini?",
            "Apakah integrasi antar sistem (katalog produk, pembayaran, logistik, dan layanan pelanggan) menggunakan standar yang konsisten, seperti API terdokumentasi?",
            "Apakah terdapat standar pengelolaan dan klasifikasi data agar data pelanggan konsisten di seluruh sistem?",
            "Apakah arsitektur sistem dirancang agar dapat diskalakan (scalable) dan tahan gangguan?",
            "Apakah setiap perubahan atau penambahan sistem baru dikaji kesesuaiannya dengan arsitektur yang telah ditetapkan?",
        ],
    },
    "BAI01": {
        "nama": "Pengelolaan Proyek Sistem Informasi", "domain": "BAI",
        "topik": "Pengelolaan proyek TI",
        "fokus": "Memastikan proyek pengembangan aplikasi selesai tepat waktu, sesuai ruang lingkup, dan anggaran.",
        "pertanyaan": [
            "Apakah perusahaan menggunakan metodologi manajemen proyek yang baku (misalnya Agile, Scrum, atau PMBOK) untuk proyek TI?",
            "Apakah setiap proyek memiliki rencana yang memuat ruang lingkup, jadwal, anggaran, dan penanggung jawab yang jelas?",
            "Apakah kemajuan proyek, penyimpangan jadwal, dan biaya dipantau serta dilaporkan secara berkala?",
            "Apakah risiko proyek diidentifikasi dan dikelola sejak tahap awal?",
            "Apakah dilakukan tinjauan pasca-proyek (lessons learned) untuk meningkatkan proyek berikutnya?",
        ],
    },
    "BAI02": {
        "nama": "Identifikasi Kebutuhan Bisnis", "domain": "BAI",
        "topik": "Identifikasi kebutuhan bisnis",
        "fokus": "Memastikan kebutuhan bisnis dianalisis secara akurat sebelum perangkat lunak baru diadakan atau dibangun.",
        "pertanyaan": [
            "Apakah terdapat prosedur baku untuk mengumpulkan dan mendokumentasikan kebutuhan bisnis dari pengguna (penjual, pembeli, dan tim internal)?",
            "Apakah kebutuhan fungsional, kebutuhan keamanan, dan kepatuhan regulasi dimasukkan dalam spesifikasi sistem?",
            "Apakah spesifikasi kebutuhan disetujui oleh pemilik proses bisnis sebelum pengembangan atau pengadaan dimulai?",
            "Apakah dilakukan analisis kelayakan (teknis, biaya, dan risiko) sebelum memutuskan membangun sendiri atau membeli solusi?",
            "Apakah setiap perubahan kebutuhan tercatat dan dapat ditelusuri hingga ke hasil akhir sistem?",
        ],
    },
    "BAI03": {
        "nama": "Pembangunan dan Pengujian Solusi TI", "domain": "BAI",
        "topik": "Pembangunan dan pengujian sistem",
        "fokus": "Mencegah bug atau celah keamanan sebelum solusi TI diluncurkan ke produksi.",
        "pertanyaan": [
            "Apakah pengembangan aplikasi mengikuti standar pengodean aman (secure coding) yang terdokumentasi?",
            "Apakah setiap rilis melalui pengujian fungsional, pengujian keamanan (misalnya penetration test), dan pengujian beban sebelum diluncurkan?",
            "Apakah lingkungan pengembangan, pengujian, dan produksi dipisahkan?",
            "Apakah data pelanggan asli dilindungi atau dianonimkan saat digunakan di lingkungan pengujian?",
            "Apakah terdapat persetujuan formal (user acceptance test) sebelum solusi dipindahkan ke produksi?",
        ],
    },
    "DSS01": {
        "nama": "Pengelolaan Operasi Harian Sistem", "domain": "DSS",
        "topik": "Operasional harian sistem",
        "fokus": "Memastikan ketersediaan layanan dan infrastruktur berjalan tanpa hambatan.",
        "pertanyaan": [
            "Apakah terdapat prosedur operasional harian yang terdokumentasi, termasuk penjadwalan pekerjaan sistem dan pemantauan server?",
            "Apakah ketersediaan platform (uptime) diukur dan dibandingkan dengan target tingkat layanan (SLA)?",
            "Apakah dilakukan pemantauan otomatis 24/7 dengan peringatan dini atas gangguan performa dan kapasitas?",
            "Apakah proses pencadangan (backup) data berjalan terjadwal dan hasilnya diverifikasi?",
            "Apakah keamanan fisik dan lingkungan pusat data atau penyedia cloud (kontrol akses, listrik, pendingin) dikelola dan diperiksa secara berkala?",
        ],
    },
    "DSS02": {
        "nama": "Penanganan Insiden dan Permintaan Layanan", "domain": "DSS",
        "topik": "Penanganan insiden TI",
        "fokus": "Kecepatan dan keakuratan dalam menangani keluhan, gangguan sistem, dan permintaan layanan pengguna.",
        "pertanyaan": [
            "Apakah terdapat sistem pencatatan (ticketing) untuk seluruh insiden dan permintaan layanan?",
            "Apakah insiden diklasifikasikan berdasarkan tingkat dampak dan prioritas, dengan batas waktu respons dan penyelesaian yang jelas?",
            "Apakah waktu rata-rata penyelesaian insiden diukur dan memenuhi target yang ditetapkan?",
            "Apakah terdapat jalur eskalasi yang jelas untuk insiden berdampak tinggi, misalnya gangguan pembayaran atau checkout?",
            "Apakah kepuasan pengguna terhadap penanganan insiden diukur dan ditindaklanjuti?",
        ],
    },
    "DSS03": {
        "nama": "Analisis dan Penyelesaian Masalah (Root Cause)", "domain": "DSS",
        "topik": "Penyelesaian akar masalah",
        "fokus": "Menganalisis akar penyebab gangguan sistem yang berulang agar dapat diselesaikan secara permanen.",
        "pertanyaan": [
            "Apakah terdapat proses manajemen masalah yang terpisah dari penanganan insiden?",
            "Apakah insiden berulang atau berdampak besar dianalisis untuk menemukan akar penyebabnya (misalnya dengan metode 5 Whys atau fishbone)?",
            "Apakah hasil analisis akar masalah didokumentasikan dalam laporan pasca-insiden (postmortem)?",
            "Apakah solusi permanen diberikan pemilik, tenggat, dan dipantau hingga selesai?",
            "Apakah terdapat basis pengetahuan (knowledge base) untuk solusi sementara dan permanen yang dapat dipakai ulang oleh tim?",
        ],
    },
    "MEA01": {
        "nama": "Pemantauan dan Evaluasi Kinerja TI", "domain": "MEA",
        "topik": "Pemantauan kinerja TI",
        "fokus": "Memastikan manajemen rutin meninjau dasbor indikator kinerja utama (KPI) layanan sistem informasi.",
        "pertanyaan": [
            "Apakah perusahaan telah menetapkan KPI dan target kinerja TI yang terukur, seperti uptime, waktu respons halaman, dan tingkat keberhasilan transaksi?",
            "Apakah data kinerja dikumpulkan secara otomatis dan disajikan dalam dasbor yang dapat diakses manajemen?",
            "Apakah manajemen meninjau hasil kinerja TI secara rutin dalam rapat yang terjadwal?",
            "Apakah penyimpangan dari target dianalisis dan ditindaklanjuti dengan tindakan perbaikan?",
            "Apakah KPI ditinjau berkala agar tetap relevan dengan tujuan bisnis?",
        ],
    },
    "MEA02": {
        "nama": "Penilaian Efektivitas Kontrol Internal", "domain": "MEA",
        "topik": "Penilaian kontrol internal",
        "fokus": "Memastikan prosedur kontrol berjalan efektif untuk mencegah kecurangan dan kelemahan operasional.",
        "pertanyaan": [
            "Apakah perusahaan memiliki kerangka kontrol internal TI yang terdokumentasi, mencakup kontrol pencegahan, deteksi, dan korektif?",
            "Apakah terdapat pemisahan tugas (segregation of duties) pada proses kritis seperti pengembangan, persetujuan, dan operasional?",
            "Apakah efektivitas kontrol diuji atau dinilai secara berkala (self-assessment atau audit internal)?",
            "Apakah terdapat mekanisme deteksi kecurangan, misalnya pemantauan transaksi mencurigakan, penyalahgunaan akun penjual, atau manipulasi ulasan?",
            "Apakah kelemahan kontrol yang ditemukan dicatat dan diperbaiki dalam waktu yang ditentukan?",
        ],
    },
    "MEA03": {
        "nama": "Evaluasi Kepatuhan Terhadap Regulasi Eksternal", "domain": "MEA",
        "topik": "Evaluasi kepatuhan regulasi",
        "fokus": "Pemenuhan regulasi perlindungan data pribadi, perdagangan melalui sistem elektronik, dan standar keamanan data pembayaran.",
        "pertanyaan": [
            "Apakah perusahaan telah mengidentifikasi seluruh regulasi yang berlaku, seperti UU Pelindungan Data Pribadi, UU ITE, regulasi PSE, dan ketentuan sistem pembayaran?",
            "Apakah terdapat petugas atau unit yang bertanggung jawab atas kepatuhan, termasuk Pejabat Pelindungan Data Pribadi (DPO)?",
            "Apakah persetujuan (consent) pengguna atas pengumpulan dan pemrosesan data pribadi dikelola dan dapat dibuktikan?",
            "Apakah perusahaan memenuhi standar keamanan data pembayaran yang relevan, misalnya PCI DSS, dan memiliki bukti sertifikasinya?",
            "Apakah kepatuhan dinilai secara berkala dan perubahan regulasi segera diterjemahkan menjadi perubahan kebijakan dan sistem?",
        ],
    },
}

TARGET_DEFAULT = 4  # target skor: 4 = Baik

REKOMENDASI_SKOR = {
    1: "Bangun fondasi: tetapkan kebijakan, penanggung jawab, dan proses dasar secara tertulis.",
    2: "Formalkan dan dokumentasikan proses, tetapkan standar, lalu mulai pantau pelaksanaannya.",
    3: "Konsistenkan penerapan di seluruh unit, sosialisasikan, dan lakukan evaluasi berkala.",
    4: "Ukur kinerja dengan metrik, tindak lanjuti penyimpangan, dan dorong perbaikan berkelanjutan.",
    5: "Pertahankan capaian, lakukan benchmarking, dan cari inovasi.",
}

# ---------------------------------------------------------------------------
# 4. DATA ILUSTRASI (SIMULASI) - GANTI dengan hasil wawancara/observasi/dokumen
# ---------------------------------------------------------------------------
# Urutan jawaban = pertanyaan 1..5. Ya / Sebagian / Tidak
CONTOH_JAWABAN = {
    "EDM01": ["Ya", "Sebagian", "Sebagian", "Sebagian", "Tidak"],
    "EDM02": ["Sebagian", "Tidak", "Tidak", "Sebagian", "Tidak"],
    "EDM03": ["Ya", "Sebagian", "Sebagian", "Ya", "Sebagian"],
    "APO01": ["Ya", "Sebagian", "Sebagian", "Ya", "Sebagian"],
    "APO02": ["Ya", "Sebagian", "Ya", "Sebagian", "Sebagian"],
    "APO03": ["Sebagian", "Ya", "Sebagian", "Sebagian", "Sebagian"],
    "BAI01": ["Ya", "Ya", "Ya", "Sebagian", "Sebagian"],
    "BAI02": ["Ya", "Sebagian", "Ya", "Sebagian", "Sebagian"],
    "BAI03": ["Sebagian", "Ya", "Ya", "Tidak", "Sebagian"],
    "DSS01": ["Ya", "Ya", "Ya", "Ya", "Sebagian"],
    "DSS02": ["Ya", "Ya", "Sebagian", "Ya", "Sebagian"],
    "DSS03": ["Sebagian", "Tidak", "Tidak", "Sebagian", "Sebagian"],
    "MEA01": ["Ya", "Ya", "Sebagian", "Sebagian", "Sebagian"],
    "MEA02": ["Sebagian", "Sebagian", "Sebagian", "Ya", "Sebagian"],
    "MEA03": ["Sebagian", "Sebagian", "Tidak", "Tidak", "Sebagian"],
}


# Skala umum 1-5 (sesuai formulir)
SKALA_UMUM = {
    1: "Sangat Buruk - tidak ada atau sama sekali tidak sesuai dengan tujuan organisasi",
    2: "Buruk - belum sepenuhnya mendukung tujuan organisasi dan standar perusahaan",
    3: "Cukup - sesuai sebagian dengan tujuan organisasi namun belum konsisten",
    4: "Baik - selaras dengan sebagian besar tujuan organisasi dan dilakukan konsisten",
    5: "Sangat Baik - sepenuhnya mendukung dan mengarahkan organisasi mencapai tujuannya",
}


# ---------------------------------------------------------------------------
# FUNGSI PERHITUNGAN, GRAFIK, DAN EKSPOR
# ---------------------------------------------------------------------------
def skala_komponen(kode):
    """Deskripsi skala 1-5 untuk satu komponen."""
    t = KOMPONEN[kode]["topik"]
    return {n: teks.format(t=t) for n, teks in SKALA_TEMPLATE.items()}


def hitung_skor_saran(jawaban):
    """Skor saran 1-5 = 1 + 4 x rata-rata (Tidak=0, Sebagian=0.5, Ya=1)."""
    nilai = [NILAI_JAWABAN[j] for j in jawaban if j in NILAI_JAWABAN]
    if not nilai:
        return None
    return int(1 + 4 * (sum(nilai) / len(nilai)) + 0.5)


def hitung_hasil(jawaban, skor_akhir, target=TARGET_DEFAULT):
    """Tabel hasil per komponen. skor_akhir = skor 1-5 yang ditetapkan auditor."""
    baris = []
    for kode, k in KOMPONEN.items():
        skor = skor_akhir.get(kode)
        baris.append({
            "Kode": kode,
            "Komponen": k["nama"],
            "Domain": k["domain"],
            "Skor Saran": hitung_skor_saran(jawaban.get(kode, [])),
            "Skor Akhir": skor,
            "Kategori": LABEL_SKOR.get(skor, "-"),
            "Target": target,
            "Gap": (target - skor) if skor is not None else None,
            "Status": ("Tercapai" if skor >= target else "Belum tercapai") if skor is not None else "-",
        })
    return pd.DataFrame(baris)


def ringkasan_domain(df):
    """Rata-rata skor akhir per domain (urut EDM, APO, BAI, DSS, MEA)."""
    r = (df.groupby("Domain")
           .agg(**{"Rata-rata Skor": ("Skor Akhir", "mean"), "Target": ("Target", "mean")})
           .reindex(URUTAN_DOMAIN).reset_index())
    r["Gap"] = r["Target"] - r["Rata-rata Skor"]
    return r.round(2)


def detail_jawaban(jawaban):
    """Detail seluruh pertanyaan dan jawabannya."""
    baris = []
    for kode, k in KOMPONEN.items():
        for i, (q, a) in enumerate(zip(k["pertanyaan"], jawaban.get(kode, [None] * 5)), start=1):
            baris.append({"Domain": k["domain"], "Kode": kode, "Komponen": k["nama"],
                          "No": i, "Pertanyaan": q, "Jawaban": a})
    return pd.DataFrame(baris)


def temuan_semua(jawaban):
    """Pertanyaan yang dijawab Tidak/Sebagian = temuan audit."""
    d = detail_jawaban(jawaban)
    return d[d["Jawaban"].isin(["Tidak", "Sebagian"])].reset_index(drop=True)


def rekomendasi(skor, target=TARGET_DEFAULT):
    if skor is None:
        return "Lengkapi penilaian terlebih dahulu."
    if skor >= target:
        return "Pertahankan capaian dan lakukan review berkala."
    return REKOMENDASI_SKOR[skor]


def tabel_prioritas(df):
    """Komponen yang belum mencapai target, gap terbesar di atas."""
    p = df[df["Gap"] > 0].sort_values(["Gap", "Kode"], ascending=[False, True]).copy()
    p["Rekomendasi"] = p.apply(lambda r: rekomendasi(r["Skor Akhir"], r["Target"]), axis=1)
    return p[["Kode", "Komponen", "Skor Akhir", "Target", "Gap", "Rekomendasi"]].reset_index(drop=True)


def grafik_domain(ring, target=TARGET_DEFAULT):
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(ring["Domain"], ring["Rata-rata Skor"], color="#4A90E2", edgecolor="black")
    ax.axhline(target, color="#ed8936", linestyle="--", label=f"Target ({target})")
    ax.set_ylim(0, 5.5)
    ax.set_ylabel("Rata-rata Skor Akhir (1-5)")
    ax.set_title("Rata-rata Skor per Domain COBIT 5", fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper right")
    for bar in bars:
        y = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, y + 0.08, f"{y:.2f}",
                ha="center", va="bottom", fontweight="bold")
    fig.tight_layout()
    return fig


def grafik_komponen(df, target=TARGET_DEFAULT):
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(df["Kode"], df["Skor Akhir"], color="#4A90E2", edgecolor="black")
    ax.axhline(target, color="#ed8936", linestyle="--", label=f"Target ({target})")
    ax.set_ylim(0, 5.5)
    ax.set_ylabel("Skor Akhir (1-5)")
    ax.set_title("Skor Akhir per Komponen COBIT 5", fontweight="bold")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper right")
    for bar in bars:
        y = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, y + 0.05, f"{int(y)}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    return fig


def fig_ke_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def buat_excel(df, ring, jawaban):
    """Membuat berkas Excel (BytesIO) berisi 5 sheet."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Rekap Komponen", index=False)
        ring.to_excel(writer, sheet_name="Rekap Domain", index=False)
        tabel_prioritas(df).to_excel(writer, sheet_name="Prioritas Perbaikan", index=False)
        temuan_semua(jawaban).to_excel(writer, sheet_name="Temuan", index=False)
        detail_jawaban(jawaban).to_excel(writer, sheet_name="Detail Jawaban", index=False)
        for ws in writer.book.worksheets:          # lebar kolom otomatis sederhana
            for kolom in ws.columns:
                panjang = max(len(str(c.value)) if c.value is not None else 0 for c in kolom)
                ws.column_dimensions[kolom[0].column_letter].width = min(panjang + 2, 70)
    output.seek(0)
    return output


# ---------------------------------------------------------------------------
# ANTARMUKA STREAMLIT
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Form Audit COBIT 5", page_icon="📊", layout="centered")

st.title("FORM AUDIT SISTEM INFORMASI")
st.subheader(f"{PROFIL['perusahaan']} – COBIT 5")
st.caption(f"Auditor: {PROFIL['nama']} ({PROFIL['nim']}) | Kelas {PROFIL['kelas']} | {PROFIL['industri']}")

with st.expander("📖 Lihat Skala Skor (Klik untuk Buka/Tutup)"):
    for n, teks in SKALA_UMUM.items():
        st.markdown(f"* **{n}. {teks.split(' - ')[0]}** - {teks.split(' - ', 1)[1]}")

with st.expander("ℹ️ Petunjuk Pengisian"):
    st.markdown(
        "Untuk setiap komponen, jawab kelima pertanyaan audit (**Ya / Sebagian / Tidak**) "
        "berdasarkan hasil wawancara, observasi, dan pemeriksaan dokumen. "
        "Setelah itu tentukan **satu skor akhir (1-5)** sesuai skala komponen tersebut. "
        "Semua isian wajib diisi sebelum hasil dapat dilihat."
    )

uji = st.checkbox("Isi otomatis dengan data uji (hanya untuk mencoba program)", value=False)
if uji:
    st.warning("Data uji hanya untuk percobaan, bukan temuan audit yang sebenarnya.")

st.markdown("---")

OPSI = ["Ya", "Sebagian", "Tidak"]
tab_list = st.tabs([f"Domain {d}" for d in URUTAN_DOMAIN])
jawaban, skor_akhir = {}, {}

with st.form("form_audit_cobit5"):
    for i, dom in enumerate(URUTAN_DOMAIN):
        with tab_list[i]:
            st.header(f"Domain: {dom}")
            st.caption(DOMAIN[dom])
            for kode, k in KOMPONEN.items():
                if k["domain"] != dom:
                    continue
                st.markdown(f"#### 🔹 {kode}: {k['nama']}")
                st.caption(k["fokus"])
                with st.expander(f"Skala skor {kode}"):
                    for n, teks in skala_komponen(kode).items():
                        st.markdown(f"* **{n} ({LABEL_SKOR[n]}):** {teks}")

                hasil = []
                for idx, q in enumerate(k["pertanyaan"], start=1):
                    awal = CONTOH_JAWABAN[kode][idx - 1] if uji else None
                    hasil.append(st.radio(
                        f"Q{idx}: {q}", OPSI,
                        index=OPSI.index(awal) if awal else None,
                        horizontal=True, key=f"{kode}_q{idx}_{uji}",
                    ))
                jawaban[kode] = hasil

                saran_uji = hitung_skor_saran(CONTOH_JAWABAN[kode]) if uji else None
                skor_akhir[kode] = st.selectbox(
                    f"Skor akhir {kode} (1-5)",
                    options=[None, 1, 2, 3, 4, 5],
                    index=saran_uji or 0,
                    format_func=lambda x: "-- Pilih skor akhir (1-5) --" if x is None else f"{x} - {LABEL_SKOR[x]}",
                    key=f"{kode}_skor_{uji}",
                )
                st.markdown("---")

    submitted = st.form_submit_button("🔍 Selesaikan Audit & Lihat Hasil")

if submitted:
    jwb_kosong = sum(1 for v in jawaban.values() for x in v if x is None)
    skor_kosong = [k for k, v in skor_akhir.items() if v is None]
    komponen_belum = [k for k in KOMPONEN
                      if None in jawaban[k] or skor_akhir[k] is None]
    if jwb_kosong or skor_kosong:
        st.session_state.pop("hasil", None)
        st.error(
            f"⚠️ Masih ada {jwb_kosong} pertanyaan dan {len(skor_kosong)} skor akhir yang belum diisi. "
            f"Komponen yang belum lengkap: {', '.join(komponen_belum)}."
        )
    else:
        st.session_state["hasil"] = {"jawaban": jawaban, "skor": skor_akhir}

if "hasil" in st.session_state:
    h = st.session_state["hasil"]
    df = hitung_hasil(h["jawaban"], h["skor"])
    ring = ringkasan_domain(df)

    st.success("Evaluasi Selesai!")

    st.subheader("1. Grafik Rata-rata Skor per Domain")
    st.pyplot(grafik_domain(ring))

    st.subheader("2. Ringkasan Rata-rata per Domain")
    st.dataframe(
        ring, width="stretch", hide_index=True,
        column_config={c: st.column_config.NumberColumn(format="%.2f")
                       for c in ["Rata-rata Skor", "Target", "Gap"]},
    )

    st.subheader("3. Ringkasan Skor per Komponen")
    st.pyplot(grafik_komponen(df))
    st.dataframe(df, width="stretch", hide_index=True)

    st.subheader("4. Prioritas Perbaikan")
    prioritas = tabel_prioritas(df)
    if prioritas.empty:
        st.info("Semua komponen telah mencapai target.")
    else:
        st.dataframe(prioritas, width="stretch", hide_index=True)

    st.download_button(
        label="📥 Unduh Hasil Excel",
        data=buat_excel(df, ring, h["jawaban"]),
        file_name="Hasil_Audit_COBIT5_DagangNusantara.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        on_click="ignore",
    )
