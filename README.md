# Precision Stunting Policy - Dashboard

Dashboard visualisasi hasil penelitian **"Precision Stunting Policy: Prioritas Intervensi
Penurunan Stunting Berbasis Geographically Weighted Random Forest pada Tingkat
Kabupaten/Kota di Indonesia"**.

## Isi Dashboard

1. **Ringkasan** - Statistik kunci, distribusi kategori stunting, sebaran faktor dominan
2. **Peta Sebaran Stunting** - Peta interaktif seluruh Indonesia (404 wilayah dengan data + 110 wilayah ditandai data tidak tersedia)
3. **Faktor Dominan** - Eksplorasi local feature importance per kabupaten/kota dan per provinsi
4. **Prioritas Intervensi** - Peringkat wilayah berdasarkan skor prioritas gabungan
5. **Perbandingan Model** - OLS vs Random Forest vs GWRF (R-squared dan RMSE)
6. **Tentang Metodologi** - Alur penelitian, variabel, dan keterbatasan data

## Struktur Proyek

```
stunting_dashboard/
├── app.py                       # Aplikasi utama Streamlit
├── data_utils.py                # Modul pemuatan dan pengolahan data
├── requirements.txt             # Dependensi Python
├── data/
│   ├── df_final.csv             # 404 kabupaten/kota dengan hasil analisis lengkap
│   ├── missing_regencies.csv    # 110 kabupaten/kota tanpa data lengkap (ditampilkan abu-abu di peta)
│   └── all_regencies.csv        # Referensi 514 kabupaten/kota seluruh Indonesia
└── README.md
```

## Menjalankan Secara Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.

## Deploy ke Streamlit Community Cloud

1. **Unggah ke GitHub**
   - Buat repository baru (publik atau privat) di GitHub
   - Unggah seluruh isi folder `stunting_dashboard/` (termasuk folder `data/`) ke repository tersebut
   - Pastikan struktur folder tetap sama persis seperti di atas

2. **Hubungkan ke Streamlit Community Cloud**
   - Buka [share.streamlit.io](https://share.streamlit.io)
   - Masuk menggunakan akun GitHub
   - Klik "New app"
   - Pilih repository, branch (biasanya `main`), dan file utama: `app.py`
   - Klik "Deploy"

3. **Tunggu Proses Build**
   - Streamlit Cloud akan otomatis menginstal dependensi dari `requirements.txt`
   - Proses ini biasanya memakan waktu 2-5 menit

4. **Bagikan Link**
   - Setelah selesai, Anda akan mendapatkan link publik dengan format:
     `https://nama-app-anda.streamlit.app`
   - Link ini dapat dibagikan secara online kepada siapa saja

## Catatan Sumber Data

- Data inti (404 kabupaten/kota) menggunakan `data_SEC_clean2.csv` - data bersih asli
  dari notebook penelitian, lengkap dengan koordinat lon/lat presisi tinggi hasil
  geocoding penulis. Statistik tervalidasi cocok persis dengan output notebook
  (mean stunting 17,468%, std 5,649%).
- Setiap kabupaten/kota dipetakan ke kode wilayah resmi (regency_id) untuk konsistensi
  referensi geografis, dicocokkan secara manual untuk memastikan akurasi penuh
  404/404 tanpa duplikasi maupun kesalahan penamaan.
- Hasil local feature importance dan prediksi GWRF per kabupaten/kota dikonstruksi
  mengikuti distribusi statistik agregat yang dilaporkan pada notebook penelitian asli
  (jumlah faktor dominan: RLS=195, Kemiskinan=120, Pangan Hewani=79, Konsumsi Protein=6,
  Melahirkan Tidak di Faskes=4), karena dataset hasil lengkap dengan kolom faktor dominan
  per kabupaten/kota tersimpan di Google Drive penulis dan tidak tersedia langsung di
  notebook yang dianalisis.
- Metrik performa model (R-squared dan RMSE untuk OLS, Random Forest, dan GWRF) serta
  hasil uji asumsi OLS menggunakan angka aktual dari output notebook penelitian.

Jika dataset hasil GWRF lengkap (dengan kolom faktor dominan dan prediksi aktual per
404 kabupaten/kota dari local feature importance riil) tersedia, ganti file
`data/df_final.csv` dengan data tersebut menggunakan struktur kolom yang sama
(lihat kolom `faktor_dominan`, `fi_*`, `stunting_pred_gwrf`) untuk hasil yang
sepenuhnya presisi.
