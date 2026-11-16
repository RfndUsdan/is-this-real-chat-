# 0003 — Phase 1 Stage 2 Dataset Selection & Audit

- **Date:** 2026-11-16
- **Status:** Stage 2 complete; dataset **CONDITIONALLY APPROVED**;
  Stage 3 belum dimulai
- **Scope:** verifikasi sumber, lisensi, metadata, file, schema, label,
  duplikasi, dan hubungan antar-record. Tidak ada preprocessing,
  training, model, API, atau dashboard yang dibuat.
- **Hubungan dengan ADR 0002:** rekomendasi BRIN Dataverse v2.1 di
  [ADR 0002](0002-phase-1-stage-1-dataset-discovery.md) digantikan untuk
  pemilihan sumber MVP. ADR 0002 tetap disimpan sebagai catatan sejarah
  dan audit Stage 1; isinya tidak dihapus atau diubah.

## 1. Context

Phase 1 membutuhkan satu dataset yang sumber, lisensi, provenance,
schema, label, dan batas penggunaannya dapat dipertanggungjawabkan.
Stage 1 menyelesaikan discovery metadata. Stage 2 harus memeriksa file
aktual, bukan hanya metadata, sebelum pipeline dimulai.

Keputusan pemilik proyek pada Stage 2:

- BRIN Dataverse v2.1 tidak dapat diakses dalam waktu yang wajar dan
  lisensi CC BY-NC 4.0 tidak dijadikan fondasi utama jika ada alternatif
  yang lebih fleksibel.
- Mendeley Data `p3hfgr5j3m/1` dipilih sebagai kandidat utama.
- Proyek adalah proyek portfolio dengan kemungkinan pengembangan
  komersial. Karena itu, risiko hak sumber berita harus dicatat, bukan
  diabaikan.

## 2. Decision

**CONDITIONALLY APPROVED** sebagai dataset utama MVP, dengan batas:

| Cakupan | Keputusan |
| --- | --- |
| Dataset utama MVP | `600 news with valid hoax label.csv` dari Mendeley `p3hfgr5j3m` versi 1 |
| File yang dipakai | Hanya CSV 600 record; file labeling workbook dipakai sebagai dokumentasi audit, bukan data training |
| 250-news files | Tidak dipakai dan tidak digabungkan; isinya praktis sudah terwakili di 600 record |
| BRIN/Mafindo | Tidak digabungkan pada MVP |
| Fakta/verdict | Label dataset bukan verdict fact-check dan bukan bukti kebenaran |
| Redistribusi raw text | Tidak disetujui untuk repository publik atau dashboard publik |
| Penggunaan komersial | Perlu review hukum hak sumber berita sebelum deployment komersial |
| Tahap berikutnya | Stage 3 belum boleh dimulai sampai pemilik menerima kondisi di bagian 9 |

Dataset ini **tidak** disetujui sebagai gold benchmark, sebagai otoritas
pemeriksa fakta, atau sebagai representasi seluruh berita Indonesia.

## 3. Source verification

Sumber resmi yang diperiksa pada 2026-11-16:

| Atribut | Nilai |
| --- | --- |
| Nama resmi | `INDONESIAN HOAX NEWS DETECTION DATASET` |
| Halaman resmi | <https://data.mendeley.com/datasets/p3hfgr5j3m/1> |
| DOI | `10.17632/p3hfgr5j3m.1` |
| Versi | `1` |
| Tanggal publikasi | 15 October 2018 |
| Kontributor | Faisal Rahutomo; Inggrid Yanuar; Rosa Andrie Asmara |
| Lisensi yang dicantumkan | CC BY 4.0 |
| Artikel terkait | DOI `10.1109/ICTS.2017.8265649` |
| Bahasa data | Indonesia |
| Kategori | Indonesian Language; Text Mining |

Halaman Mendeley menyebut lima file data. Arsip aktual berisi lima file
data tersebut ditambah `Readme.txt`. Halaman juga menyatakan bahwa
dataset adalah bagian dari makalah:

> I. Y. R. Pratiwi, R. A. Asmara and F. Rahutomo, "Study of hoax news
> detection using naïve bayes classifier in Indonesian language," 2017
> 11th International Conference on Information & Communication
> Technology and System (ICTS), Surabaya, 2017, pp. 73-78.
> doi: 10.1109/ICTS.2017.8265649

## 4. License and terms

### 4.1 Lisensi dataset

Halaman dataset mencantumkan **CC BY 4.0**. Teks lisensi yang
ditampilkan Mendeley menyatakan, secara ringkas:

> You can share, copy and modify this dataset so long as you give
> appropriate credit, provide a link to the CC BY license, and indicate
> if changes were made. ... Note that further permission may be required
> for any content within the dataset that is identified as belonging to
> a third party.

Implikasi:

- Atribusi, tautan lisensi, dan indikasi perubahan wajib disertakan.
- CC BY 4.0 mengizinkan penggunaan, adaptasi, dan redistribusi, termasuk
  penggunaan komersial, **jika** pemberi lisensi memang memiliki hak
  yang cukup atas konten.
- Teks berita adalah konten pihak ketiga. Paket dataset tidak memuat
  bukti izin tertulis dari portal berita atau pemilik hak atas setiap
  artikel.
- Karena itu, izin untuk memakai teks untuk eksperimen internal dan
  analisis tidak otomatis menjadi izin untuk mempublikasikan ulang teks
  mentah atau melakukan deployment komersial tanpa review.

**Kesimpulan operasional:** teks boleh dipakai dan dimodifikasi untuk
audit/eksperimen internal dengan atribusi, tetapi HoaxScope **tidak
menyetujui redistribusi teks mentah** ke repository publik atau
dashboard publik. Redistribusi teks dan penggunaan komersial tetap
memerlukan review hak pihak ketiga dan ketentuan Mendeley/Elsevier.

### 4.2 Ketentuan Mendeley/Elsevier

Mendeley Terms of Use (last updated 21 January 2022) menginkorporasikan
Elsevier Terms and Conditions.
Ketentuan tersebut memuat pembatasan umum terkait scraping, penggunaan
situs, Konten, dan AI training/data mining. Halaman dataset memberikan
lisensi khusus CC BY 4.0 untuk dataset. Ketentuan situs dan lisensi
dataset perlu dibaca bersama; penilaian ini bukan nasihat hukum.

Mendeley juga menempatkan tanggung jawab kepada uploader untuk memastikan
bahwa konten yang diunggah adalah milik uploader atau telah dibersihkan
haknya. Ini adalah warranty dari uploader, bukan bukti independen bahwa
semua hak berita sudah diperoleh.

### 4.3 Atribusi yang akan dipakai

Contoh atribusi untuk dokumentasi atau UI:

> Rahutomo, F.; Yanuar, I.; Asmara, R. A. (2018). *Indonesian Hoax News
> Detection Dataset* (Version 1) [Data set]. Mendeley Data.
> <https://doi.org/10.17632/p3hfgr5j3m.1>. Lisensi CC BY 4.0.
> Perubahan yang dilakukan: pemetaan label dan pembersihan teks untuk
> pipeline HoaxScope.

Jika teks mentah tidak dipublikasikan, atribusi tetap dicantumkan pada
dokumentasi dataset, model card, dan halaman metodologi.

## 5. File dan integritas

Paket resmi diunduh dari endpoint download Mendeley. Endpoint tersebut
membungkus file dataset di dalam ZIP luar; ZIP luar bukan isi dataset.
ZIP dataset yang sebenarnya berukuran **577,997 byte** dengan SHA-256:

```text
0f1e671ccaee23bdada94821737acb39e4b95127a2a3011edb0a6972b2b1a2fb
```

Isi ZIP dataset: lima file data yang didokumentasikan, ditambah
`Readme.txt` (total enam entry).

| File | Ukuran (byte) | SHA-256 |
| --- | ---: | --- |
| `600 news with valid hoax label.csv` | 1,335,120 | `8c16f1e6258f3a828381c0e4b12ecee6730111c7c5be95ef5e70725201631f67` |
| `600 news labelling process.xlsx` | 88,152 | `ab2b269cf5df8068a11a8e823b8db55ca5f15671da7ea41699848fda0816c28a` |
| `250 news with valid hoax label.csv` | 588,520 | `3510a9c6b018f33cfe6c684561f42ef86c6b7ff474f814805291932c6255393b` |
| `250 news labelling process.xlsx` | 38,248 | `f042592f9eb595d60a23fe8bebc7c057c4f4d372be027aa3a02ab7249ae1ae9d` |
| `250 news experiment documentation.xlsx` | 25,227 | `c51abda1779a86732327dd0cd970bf946c9ce942b662af2f345730bcb2359636` |
| `Readme.txt` | 1,894 | `6b0ef7ae2e6b43752b3ba460f90879ec9581b9fae4a438ede5ad189ddd300718` |

File dataset hanya disimpan di direktori sementara untuk audit. Tidak ada
file dataset yang disalin ke repository.

## 6. Schema dan label aktual

### 6.1 CSV 600 record

| Atribut | Nilai aktual |
| --- | --- |
| Encoding | `cp1252` (bukan UTF-8), tanpa BOM |
| Delimiter | Titik koma (`;`) |
| Line ending | CRLF |
| Header | `berita;tagging` |
| Jumlah record | 600 |
| Kolom teks | `berita` |
| Kolom label | `tagging` |
| Kolom lain | Tidak ada |
| ID/URL/source/topic/timestamp | Tidak ada di CSV |

CSV hanya berisi teks berita dan label. Tidak ada kolom `Fact`,
`References`, URL, sumber, tanggal, topik, atau ID record. Oleh karena
itu:

- tidak ada post-hoc fact-check field yang bisa dipakai sebagai fitur;
- analisis tren temporal tidak didukung oleh CSV ini;
- hubungan ke URL/topik hanya dapat diinferensikan dari workbook labeling,
  bukan dari kunci eksplisit.

### 6.2 Label taxonomy dan mapping

Label sumber di CSV adalah `Valid` dan `Hoax`. Workbook voting memakai
`valid`/`hoax` dengan beberapa variasi yang tidak standar.

| Label sumber | Label internal | Arti yang dipakai HoaxScope |
| --- | --- | --- |
| `Hoax` | `hoax` | Label dataset untuk teks yang diklasifikasikan sebagai hoax oleh proses sumber |
| `Valid` | `not_flagged_as_hoax` | Label dataset untuk teks yang tidak dilabeli hoax; **bukan** bukti bahwa semua klaimnya benar |

Aturan:

- Simpan label asli di `label_source`; jangan mengganti sejarah label.
- Jangan memakai `TRUE`/`valid` sebagai klaim kebenaran faktual.
- Jangan menganggap `Valid` sebagai hasil verifikasi independen.
- Jangan memakai label turunan atau metadata post-hoc sebagai fitur.
- Jangan menyatukan label ini dengan label dataset lain tanpa pemetaan
  dan audit terpisah.

Tidak ada codebook definisi label yang lengkap di paket. Halaman dataset
dan `Readme.txt` hanya mendeskripsikan proses tiga referee dan voting;
tidak memberikan definisi operasional rinci untuk `Valid`/`Hoax`.

## 7. Audit hasil aktual

### 7.1 CSV 600

| Pemeriksaan | Hasil aktual |
| --- | ---: |
| Total record | 600 |
| `Valid` | 372 (62.0%) |
| `Hoax` | 228 (38.0%) |
| Teks kosong/missing | 0 |
| Label missing/tidak dikenal | 0 |
| Exact duplicate text | 0 |
| Duplicate setelah whitespace normalization | 0 |
| Panjang teks minimum | 543 karakter |
| Panjang teks p25 / median / p75 | 1,351 / 1,944 / 2,780 karakter |
| Panjang teks maksimum | 9,618 karakter |
| Rata-rata panjang teks | 2,213.1 karakter |
| Teks dengan tag HTML sisa | 2 |
| Teks dengan URL | 6 |
| Teks dengan alamat email | 2 (alamat resmi `kemlu.go.id`) |
| Teks dengan NIK 16 digit | 0 |
| Teks dengan nomor telepon yang jelas | 0; 2 deret tanggal memberi false positive pada regex nomor telepon |

### 7.2 Workbook labeling 600

| Pemeriksaan | Hasil aktual |
| --- | ---: |
| Sheet | 12 (`KW1`–`KW12`) |
| Record per sheet | 50 |
| Total link/record | 600 |
| Rater per record | 3 + voting |
| Voting workbook `valid` / `hoax` | 369 / 231 |
| Raw rater label `valid` / `hoax` | 1,094 / 702 |
| Raw rater label tidak standar | `ho` 2 kali; `haox` 2 kali |
| Baris dengan label rater tidak standar | 3 |
| CSV vs voting workbook berbeda | 9 |
| Arah perbedaan | 6 CSV `Valid` → workbook `Hoax`; 3 CSV `Hoax` → workbook `Valid` |
| Raw vote vs majority mismatch | 2; satu dijelaskan oleh typo `haox` |
| URL unik (exact string) | 567 |
| Grup URL duplikat | 31 grup / 64 baris |
| Grup URL dengan label CSV konflik | 10 grup / 20 baris |
| Grup URL dengan voting workbook konflik | 7 grup / 14 baris |

Sembilan perbedaan label CSV vs voting workbook:

| CSV row | Label CSV | Voting workbook |
| ---: | --- | --- |
| 27 | `Valid` | `Hoax` |
| 28 | `Valid` | `Hoax` |
| 31 | `Hoax` | `Valid` |
| 144 | `Valid` | `Hoax` |
| 200 | `Valid` | `Hoax` |
| 378 | `Hoax` | `Valid` |
| 427 | `Valid` | `Hoax` |
| 439 | `Hoax` | `Valid` |
| 441 | `Valid` | `Hoax` |

Vote/majority mismatch:

- `KW1` row 57: rater `valid, hoax, valid`, voting `hoax`; mayoritas
  seharusnya `valid`.
- `KW8` row 24: rater `haox, haox, valid`, voting `hoax`; jika `haox`
  dinormalisasi menjadi `hoax`, hasilnya konsisten.

Temuan ini berarti CSV final **tidak sepenuhnya dapat direproduksi** dari
workbook voting. CSV tetap dapat dipakai sebagai label final yang
dibekukan, tetapi perbedaan dan konflik harus dicatat, bukan disembunyikan.

### 7.3 File 250 record

| Pemeriksaan | Hasil aktual |
| --- | ---: |
| CSV 250 record | 250 |
| Label CSV 250 `Valid` / `Hoax` | 159 / 91 |
| Workbook 250 sections | 10 topik × 25 record |
| Voting workbook 250 `valid` / `hoax` | 159 / 91 |
| CSV 250 vs voting workbook berbeda | 10 posisi |
| Exact text match di CSV 600 | 249 dari 250 |
| Label agreement pada exact match | 249 dari 249 |
| Satu teks yang tidak exact-match | Near-duplicate 5-gram Jaccard 0.9825 terhadap record 600 index 24; label sama-sama `Hoax` |

Kesimpulan: file 250 praktis merupakan versi awal/redundan dari 600.
File 250 tidak menambah nilai unik untuk MVP dan **tidak boleh
digabungkan** dengan 600.

### 7.4 Experiment documentation 250

File `250 news experiment documentation.xlsx` berisi daftar ID untuk
skema 60/40, 70/30, dan 80/20 (masing-masing tiga eksperimen). File ini
**tidak** berisi metrik, confusion matrix, atau hasil evaluasi.

Audit menemukan ID duplikat di dalam kolom split dan nilai di luar rentang
1–250 (sampai 1,179). Karena itu file ini tidak dapat dianggap sebagai
catatan split yang reproducible dan tidak dipakai sebagai bukti performa.

### 7.5 Duplikasi dan leakage

CSV 600 lulus exact/whitespace deduplication, tetapi tidak lulus
URL-level dan near-duplicate deduplication.

Dengan 5-word shingles, case-insensitive, token alfanumerik, dan Jaccard
≥ 0.5:

| Metrik | Hasil |
| --- | ---: |
| Pasangan near-duplicate kandidat | 332 |
| Pasangan dengan label sama | 278 |
| Pasangan dengan label berbeda | 54 |
| Pasangan dengan URL sama | 30 |
| Record dalam komponen multi-record | 255 |
| Komponen multi-record | 91 |
| Komponen terbesar | 16 record |
| Komponen dengan label konflik | 27 |

Dengan 8-word shingles, Jaccard ≥ 0.5: 280 pasangan dan 240 record dalam
89 komponen. Dengan 5-word shingles, Jaccard ≥ 0.8: 166 pasangan dan 186
record dalam 75 komponen. Angka ini adalah **kandidat** near-duplicate,
bukan vonis bahwa semua teks adalah artikel yang sama. Namun jumlahnya
cukup besar untuk membuat random split tidak aman.

Selain itu, 31 grup URL duplikat di workbook menunjukkan bahwa satu URL
dapat muncul lebih dari sekali dengan versi teks yang sedikit berbeda.
Sepuluh grup di antaranya memiliki label CSV yang saling bertentangan.
Ini adalah label noise dan leakage risk yang harus ditangani sebelum
split.

### 7.6 Privacy dan content hygiene

- Dua teks memuat alamat email resmi `kemlu.go.id`; alamat tidak
  ditampilkan di dokumen ini.
- Tidak ditemukan NIK 16 digit.
- Tidak ditemukan nomor telepon yang jelas; dua deret tanggal memicu
  false positive pada regex sederhana.
- Enam teks memuat URL; dua teks memuat tag HTML sisa.
- Tidak ada karakter kontrol yang tidak wajar.
- Teks memakai curly quotes, dash, dan ellipsis yang umum di `cp1252`.

Temuan ini bukan blocker utama, tetapi preprocessing harus menangani
encoding, HTML, URL, dan boilerplate secara eksplisit.

## 8. Hubungan record dan keterbatasan audit

1. CSV 600 tidak memiliki kunci eksplisit ke workbook labeling.
2. Workbook 600 memiliki 12 sheet × 50 record; CSV dibaca dalam urutan
   baris yang sama. Dengan asumsi urutan itu, 591 dari 600 label cocok
   dengan voting workbook.
3. Karena tidak ada ID/URL di CSV, pemetaan CSV↔workbook bersifat
   **inferensi urutan**, bukan relasi yang dijamin oleh pembuat dataset.
   Pemetaan ini harus dibekukan dan dicatat jika akan dipakai.
4. Workbook 600 memiliki 567 URL unik dan 31 grup duplikat. CSV memiliki
   600 teks unik; teks yang berbeda dapat berasal dari URL yang sama.
5. Tidak ada timestamp, sumber, publisher, atau topik di CSV. Analisis
   tren temporal dan source bias yang ketat tidak dapat dilakukan dari
   CSV saja.
6. File 250 tidak dipakai untuk melengkapi 600 karena praktis redundan
   dan memiliki masalah konsistensi label sendiri.
7. Audit ini tidak menghitung metrik model, tidak memilih model, dan
   tidak mengklaim kualitas prediksi.

## 9. Conditions of approval

Approval ini berlaku hanya jika semua kondisi berikut diterima dan
dijalankan pada Stage 3:

1. **Atribusi dan lisensi.** Cantumkan DOI, kreator, versi, dan tautan
   CC BY 4.0. Indikasikan perubahan yang dilakukan. Jangan hapus atau
   samarkan atribusi.
2. **Tidak ada redistribusi raw text.** Jangan commit file CSV/XLSX ke
   repository publik. Jangan menyajikan teks artikel lengkap di
   dashboard/API publik. Repository hanya berisi dokumentasi, kode, dan
   fixture sintetis.
3. **Satu dataset.** Gunakan hanya CSV 600. Jangan menggabungkan file
   250, BRIN, Mafindo, atau sumber lain pada MVP.
4. **Bekukan manifest.** Gunakan hash di bagian 5. Perubahan file atau
   mapping harus menghasilkan versi dataset baru dan audit ulang.
5. **Label adalah label sumber.** Simpan `label_source`; gunakan
   `Hoax → hoax` dan `Valid → not_flagged_as_hoax`. Jangan mengklaim
   `Valid` sebagai bukti kebenaran atau `Hoax` sebagai verdict hukum.
6. **Tangani konflik label.** Catat 9 perbedaan CSV↔workbook dan 10 grup
   URL/20 baris dengan label konflik. Untuk MVP, keluarkan record yang
   masih konflik dari data training/evaluasi utama, atau jalankan
   sensitivity analysis terpisah. Jangan memilih label hanya agar
   metrik terlihat lebih baik.
7. **Group split, bukan random split.** Bentuk group dari URL yang sama
   dan komponen near-duplicate (minimal 5-word Jaccard ≥ 0.5) sebelum
   split. Gunakan group-aware train/validation/test (rencana awal
   70/15/15) dan pastikan tidak ada group yang lintas split. Fit
   TF-IDF/vectorizer hanya pada training.
8. **Jangan memakai post-hoc fields.** Dataset ini tidak memiliki
   `Fact`/`References`, tetapi aturan tetap berlaku: jangan menambah
   field fact-check, verdict, URL, atau metadata post-hoc sebagai fitur.
9. **Review hak berita sebelum komersial.** Sebelum deployment komersial
   atau publikasi teks, lakukan review hukum hak sumber berita dan
   ketentuan Mendeley/Elsevier. Jangan menganggap CC BY 4.0 sebagai
   penyelesaian otomatis untuk konten pihak ketiga.
10. **Terima batas model.** Semua output harus menyebut prediksi model,
    confidence, dan kebutuhan verifikasi lanjutan. Jangan menampilkan
    "pasti hoaks" atau "pasti benar". Jangan menampilkan tren temporal
    karena tidak ada timestamp yang memadai.

## 10. Split dan evaluation policy untuk Stage 3

Kebijakan ini belum diimplementasikan; hanya keputusan arah:

- Dataset: 600 CSV, label final dibekukan.
- Group key: exact URL dari workbook bila pemetaan urutan dipakai, plus
  komponen near-duplicate teks.
- Split awal: 70% train, 15% validation, 15% test, stratified per label
  jika memungkinkan setelah grouping.
- Test set tidak dipakai untuk tuning, pemilihan threshold, atau
  pemilihan model.
- Macro F1 tetap metrik utama; sertakan per-class precision/recall/F1,
  support, accuracy, dan confusion matrix.
- Laporkan hasil dengan dan tanpa record konflik sebagai sensitivity
  analysis, bukan sebagai angka utama yang dipilih setelah melihat test.
- Jangan memakai file experiment 250 sebagai split acuan.

## 11. Mengapa tidak sepenuhnya disetujui

- Lisensi CC BY 4.0 mencakup dataset, tetapi teks berita adalah konten
  pihak ketiga dan tidak ada bukti izin hulu di paket.
- Label CSV tidak sepenuhnya cocok dengan workbook voting.
- Ada 10 grup URL dengan label konflik dan 20 baris terdampak.
- Ada near-duplicate yang cukup luas untuk menimbulkan leakage.
- CSV tidak memiliki ID, URL, sumber, topik, atau timestamp.
- Metadata tidak menjelaskan periode pengumpulan secara eksplisit.

## 12. Mengapa tidak ditolak

- Sumber dan versi resmi terverifikasi.
- Lisensi dataset eksplisit dan relatif permisif.
- File dapat diunduh melalui sumber resmi dan hash-nya tercatat.
- 600 record memiliki teks dan label yang lengkap; tidak ada teks kosong.
- Sebagian besar label CSV konsisten dengan workbook (591/600).
- Dataset cukup kecil dan jelas untuk MVP portfolio, asalkan batas dan
  konfliknya ditangani.

## 13. Validasi yang dilakukan

- Membaca halaman resmi Mendeley, DOI, metadata versi, kontributor,
  lisensi, dan artikel terkait.
- Mengunduh paket melalui endpoint download resmi Mendeley.
- Memeriksa ZIP luar, mengekstrak ZIP dataset, dan mencocokkan hash
  dataset dengan metadata.
- Membaca keenam entry arsip, termasuk `Readme.txt`.
- Mem-parse CSV 600 dan 250 dengan encoding `cp1252`.
- Mem-parse seluruh sheet XLSX tanpa library eksternal.
- Membandingkan label CSV dengan voting workbook untuk 600 dan 250.
- Menghitung distribusi label, panjang teks, missing value, exact
  duplicate, URL duplicate, near-duplicate, dan PII sederhana.
- Memeriksa Mendeley Terms of Use, Elsevier Terms and Conditions, dan
  CC BY 4.0.
- Memastikan tidak ada file dataset yang masuk repository.

Tidak ada test/lint/type-check aplikasi yang relevan karena Stage 2 tidak
mengubah kode pipeline.

## 14. Langkah berikutnya

Stage 2 berhenti di sini. Stage 3 belum dimulai.

Setelah pemilik secara eksplisit menerima kondisi di bagian 9:

1. Siapkan salinan dataset di penyimpanan lokal yang tidak di-commit.
2. Buat loader dan schema validation untuk CSV 600.
3. Bekukan mapping baris/URL dan dokumentasikan konflik label.
4. Buat group-aware split dan test untuk mencegah leakage.
5. Buat preprocessing minimal dan test-nya.
6. Baru mulai baseline model dan evaluasi.

Tanpa penerimaan kondisi tersebut, jangan mulai Stage 3.

## 15. Referensi

- Mendeley dataset:
  <https://data.mendeley.com/datasets/p3hfgr5j3m/1>
- DOI dataset: <https://doi.org/10.17632/p3hfgr5j3m.1>
- Artikel terkait: <https://doi.org/10.1109/ICTS.2017.8265649>
- CC BY 4.0: <https://creativecommons.org/licenses/by/4.0/>
- Mendeley Terms of Use: <https://www.mendeley.com/terms/>
- Elsevier Terms and Conditions:
  <https://www.elsevier.com/legal/elsevier-website-terms-and-conditions>
- ADR Stage 1:
  [0002-phase-1-stage-1-dataset-discovery.md](0002-phase-1-stage-1-dataset-discovery.md)
