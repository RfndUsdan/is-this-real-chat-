# HoaxScope --- Dataset Documentation

> Dokumen ini adalah register dataset kanonik HoaxScope. Isinya berasal
> dari audit file aktual pada 2026-11-16, bukan dari asumsi atau template.
> Detail keputusan dan metode audit ada di
> [ADR 0003](docs/decisions/0003-dataset-selection.md).

## 1. Status dan tujuan

Dataset utama MVP: **Mendeley Data `p3hfgr5j3m` versi 1**, hanya file
`600 news with valid hoax label.csv`.

Status keputusan: **CONDITIONALLY APPROVED** dengan kondisi ADR 0003
diterima pemilik. Stage 3 selesai pada 2026-11-24: loader CP1252, canonical
schema, validasi baseline, row-order workbook audit, deduplikasi/konflik,
preprocessing modular, dan group-aware split telah diimplementasikan serta
diuji. Dataset **belum boleh dipakai untuk training** sampai pemilik
menyetujui Phase 2. Hasil audit:
[laporan Stage 3](docs/experiments/stage-3-data-pipeline.md).

Batas penting:

- Label dataset adalah label sumber, bukan verdict fact-check.
- `Valid` tidak membuktikan bahwa seluruh klaim dalam teks benar.
- Dataset bukan gold benchmark dan tidak mewakili seluruh berita Indonesia.
- File 250 tidak dipakai dan tidak digabungkan.
- BRIN/Mafindo dan sumber lain tidak digabungkan pada MVP.
- Raw text tidak boleh di-commit atau ditampilkan ulang sebagai dataset
  publik tanpa review hak.

Pipeline data Stage 3 tersedia di `ml/src/hoaxscope_ml`; model, API,
dan dashboard belum diimplementasikan.

## 2. Register dataset

| Atribut | Nilai |
| --- | --- |
| Nama resmi | `INDONESIAN HOAX NEWS DETECTION DATASET` |
| URL sumber | <https://data.mendeley.com/datasets/p3hfgr5j3m/1> |
| DOI | `10.17632/p3hfgr5j3m.1` |
| Pembuat/kontributor | Faisal Rahutomo; Inggrid Yanuar; Rosa Andrie Asmara |
| Tanggal akses | 2026-11-16 |
| Versi | `1` |
| Tanggal publikasi | 15 October 2018 |
| Lisensi | CC BY 4.0; ada catatan izin pihak ketiga untuk konten yang bukan milik uploader |
| Format | ZIP berisi CSV dan XLSX |
| Jumlah record awal | 600 pada CSV utama |
| Bahasa | Indonesia |
| Rentang tanggal konten | Tidak tersedia di CSV; tidak boleh diasumsikan |
| Unit data | Teks berita + label biner |
| Artikel terkait | I. Y. R. Pratiwi, R. A. Asmara, F. Rahutomo, ICTS 2017, DOI `10.1109/ICTS.2017.8265649` |
| Atribusi wajib | DOI, kreator, versi, lisensi CC BY 4.0, dan indikasi perubahan |
| Catatan penggunaan | Hanya 600 CSV; jangan merge 250/BRIN; jangan pakai post-hoc field; group split wajib |

## 3. File manifest

Paket resmi berisi lima file data dan satu `Readme.txt`. File dataset
sebenarnya berada di dalam ZIP; endpoint download Mendeley menambahkan
ZIP pembungkus. Hash ZIP dataset:

```text
0f1e671ccaee23bdada94821737acb39e4b95127a2a3011edb0a6972b2b1a2fb
```

| File | Ukuran (byte) | SHA-256 |
| --- | ---: | --- |
| `600 news with valid hoax label.csv` | 1,335,120 | `8c16f1e6258f3a828381c0e4b12ecee6730111c7c5be95ef5e70725201631f67` |
| `600 news labelling process.xlsx` | 88,152 | `ab2b269cf5df8068a11a8e823b8db55ca5f15671da7ea41699848fda0816c28a` |
| `250 news with valid hoax label.csv` | 588,520 | `3510a9c6b018f33cfe6c684561f42ef86c6b7ff474f814805291932c6255393b` |
| `250 news labelling process.xlsx` | 38,248 | `f042592f9eb595d60a23fe8bebc7c057c4f4d372be027aa3a02ab7249ae1ae9d` |
| `250 news experiment documentation.xlsx` | 25,227 | `c51abda1779a86732327dd0cd970bf946c9ce942b662af2f345730bcb2359636` |
| `Readme.txt` | 1,894 | `6b0ef7ae2e6b43752b3ba460f90879ec9581b9fae4a438ede5ad189ddd300718` |

File audit hanya berada di direktori sementara di luar repository. Tidak
ada file dataset yang disalin ke `ml/data/raw/` atau di-commit.

## 4. Schema dan label

### 4.1 Schema aktual CSV

| Properti | Nilai |
| --- | --- |
| Encoding | `cp1252`, tanpa BOM |
| Delimiter | `;` |
| Line ending | CRLF |
| Header | `berita;tagging` |
| Kolom teks | `berita` |
| Kolom label | `tagging` |
| Kolom lain | Tidak ada |
| ID, URL, sumber, topik, timestamp | Tidak tersedia |

CSV tidak memiliki kunci record. Whitespace, encoding, tanda kutip, dan
karakter non-ASCII harus ditangani secara eksplisit pada loader. Jangan
mengasumsikan file ini UTF-8.

### 4.2 Label taxonomy

Label sumber adalah `Valid` dan `Hoax`.

| Label sumber | Label internal | Catatan |
| --- | --- | --- |
| `Hoax` | `hoax` | Label sumber untuk teks yang dilabeli hoax oleh proses dataset |
| `Valid` | `not_flagged_as_hoax` | Label sumber untuk teks yang tidak dilabeli hoax; bukan bukti kebenaran |

Aturan mapping:

- Simpan label sumber di `label_source`.
- Gunakan `hoax` dan `not_flagged_as_hoax` untuk baseline biner.
- Jangan memakai `TRUE`/`valid` sebagai klaim faktual.
- Jangan menyatukan label dengan dataset lain tanpa mapping dan audit baru.
- Jangan memakai label turunan atau metadata post-hoc sebagai fitur.

Tidak ada codebook definisi label yang lengkap di paket. Halaman dataset
dan `Readme.txt` hanya menjelaskan tiga referee dan voting. Karena itu
label harus diperlakukan sebagai label sumber yang memiliki noise, bukan
ground truth yang sempurna.

## 5. Data quality audit

### 5.1 CSV 600

| Pemeriksaan | Hasil aktual |
| --- | ---: |
| Total record | 600 |
| `Valid` | 372 (62.0%) |
| `Hoax` | 228 (38.0%) |
| Teks kosong/missing | 0 |
| Label missing/tidak dikenal | 0 |
| Exact duplicate text | 0 |
| Duplicate setelah whitespace normalization | 0 |
| Panjang minimum | 543 karakter |
| Panjang p25 / median / p75 | 1,351 / 1,944 / 2,780 karakter |
| Panjang maksimum | 9,618 karakter |
| Rata-rata panjang | 2,213.1 karakter |
| Teks dengan tag HTML sisa | 2 |
| Teks dengan URL | 6 |
| Teks dengan email | 2 alamat resmi `kemlu.go.id` |
| Teks dengan NIK 16 digit | 0 |
| Teks dengan nomor telepon jelas | 0; 2 deret tanggal adalah false positive regex |

### 5.2 Workbook labeling 600

| Pemeriksaan | Hasil aktual |
| --- | ---: |
| Sheet | 12: `KW1`–`KW12` |
| Record per sheet | 50 |
| Total record | 600 |
| Rater per record | 3 + voting |
| Voting `valid` / `hoax` | 369 / 231 |
| Raw rater `valid` / `hoax` | 1,094 / 702 |
| Rater tidak standar | `ho` 2 kali, `haox` 2 kali |
| Baris dengan rater tidak standar | 3 |
| CSV vs voting berbeda | 9 (6 `Valid`→`Hoax`, 3 `Hoax`→`Valid`) |
| Raw vote vs majority mismatch | 2; satu dijelaskan typo `haox` |
| URL unik | 567 |
| Grup URL duplikat | 31 grup / 64 baris |
| Grup URL dengan label CSV konflik | 10 grup / 20 baris |
| Grup URL dengan voting workbook konflik | 7 grup / 14 baris |

Perbedaan label CSV vs voting workbook pada baris 27, 28, 31, 144, 200,
378, 427, 439, dan 441. Rincian ada di ADR 0003. CSV dipakai sebagai label
final yang dibekukan, tetapi perbedaan ini harus disimpan sebagai label
noise dan tidak boleh diklaim sebagai hasil voting yang sepenuhnya
reproducible.

### 5.3 File 250

| Pemeriksaan | Hasil aktual |
| --- | ---: |
| CSV 250 | 250 record |
| Label `Valid` / `Hoax` | 159 / 91 |
| Workbook 250 | 10 topik × 25 record |
| CSV vs voting workbook | 10 posisi berbeda |
| Exact text match di 600 | 249 dari 250 |
| Label agreement pada exact match | 249 dari 249 |
| Satu teks tersisa | Near-duplicate 5-gram Jaccard 0.9825 terhadap 600 index 24; label sama |

Kesimpulan: 250 adalah versi awal/redundan. Tidak dipakai, tidak
digabungkan, dan tidak menjadi split acuan.

### 5.4 Experiment documentation 250

File ini berisi daftar ID untuk skema 60/40, 70/30, dan 80/20, tetapi
tidak memuat metrik atau hasil evaluasi. Audit menemukan ID duplikat dan
nilai di luar rentang 1–250 (sampai 1,179). File ini tidak dipakai sebagai
bukti performa atau split yang reproducible.

## 6. Hubungan record

- CSV 600: 600 teks unik, tanpa ID/URL/topik.
- Workbook 600: 12 topik × 50 record; memiliki link dan voting.
- Tidak ada kunci eksplisit CSV↔workbook.
- Dengan asumsi urutan baris CSV sama dengan urutan 12 sheet × 50,
  591/600 label cocok. Ini inferensi urutan, bukan relasi yang dijamin
  pembuat dataset.
- Workbook memiliki 567 URL unik; 31 grup URL muncul lebih dari sekali.
- Satu URL dapat memiliki dua versi teks dan dua label yang berbeda.
- File 250 praktis tercakup di 600; jangan merge.

Pemetaan CSV↔workbook telah dibekukan pada Stage 3 sebagai inferensi urutan
baris (`row_order_inference_12x50`) dan diverifikasi terhadap baseline:
600 link terpetakan, 567 URL unik, 31 grup duplikat/64 baris, dan 9
perbedaan label CSV vs voting. Ini tetap **bukan relasi resmi**; jangan
menganggap URL atau topik dapat diambil langsung dari CSV.

## 7. Duplikasi dan leakage

Exact/whitespace duplicate di CSV: **0**. Namun risiko leakage tetap
tinggi karena:

1. Ada 31 grup URL duplikat di workbook (64 baris).
2. Ada 10 grup/20 baris dengan label CSV yang saling bertentangan.
3. Near-duplicate teks cukup banyak.

Dengan 5-word shingles dan Jaccard ≥ 0.5:

| Metrik | Hasil |
| --- | ---: |
| Pasangan kandidat | 332 |
| Pasangan label sama | 278 |
| Pasangan label berbeda | 54 |
| Pasangan URL sama | 30 |
| Record dalam komponen multi-record | 255 |
| Komponen multi-record | 91 |
| Komponen terbesar | 16 record |
| Komponen dengan label konflik | 27 |

Dengan 8-word shingles/Jaccard ≥ 0.5: 280 pasangan dan 240 record dalam
89 komponen. Dengan 5-word/Jaccard ≥ 0.8: 166 pasangan dan 186 record
dalam 75 komponen.

Angka ini adalah kandidat near-duplicate. Random split tidak aman. Group
split wajib memakai URL dan komponen near-duplicate; detail ada di ADR
0003 dan bagian 9.

## 8. Preprocessing policy

Stage 3 mengimplementasikan preprocessing modular berikut. Urutan dan
defaultnya dapat direproduksi lewat `PreprocessingConfig`:

1. Baca CSV dengan encoding `cp1252` dan delimiter `;`.
2. Validasi header, jumlah kolom, label, dan teks kosong.
3. Normalisasi whitespace dan Unicode tanpa menghapus negasi/angka.
4. Tangani tag HTML sisa, URL, dan boilerplate secara eksplisit.
5. Jangan menghapus kata `hoax`/`valid` secara membabi buta hanya karena
   terlihat seperti label; uji dampaknya.
6. Simpan teks asli dan hasil preprocessing secara terpisah.
7. Jangan menaruh raw text di log, fixture publik, atau dashboard.

Preprocessing yang belajar dari data (TF-IDF, vocabulary, normalisasi
statistik) hanya boleh fit pada training split.

## 9. Split dan evaluation policy

Stage 3 mengimplementasikan split group-aware dengan seed `20261124`.
Keputusan dan hasil aktual:

- Dataset: CSV 600, label final dibekukan.
- Group key: URL exact dari workbook jika mapping urutan dipakai, plus
  komponen near-duplicate 5-word/Jaccard ≥ 0.5.
- Split awal: 70% train, 15% validation, 15% test; stratifikasi label
  setelah grouping bila memungkinkan.
- Tidak ada group yang muncul di dua split.
- Test set tidak dipakai untuk tuning, threshold, atau pemilihan model.
- Metrik utama: Macro F1; sertakan per-class precision/recall/F1,
  support, accuracy, dan confusion matrix.
- Laporkan sensitivity analysis untuk record konflik, bukan memilih
  angka yang paling bagus setelah melihat test.
- Jangan memakai file experiment 250 sebagai split acuan.

Hasil aktual Stage 3: 92 record dengan konflik label dalam komponen duplikat
dikarantina, sehingga 508 record layak dibagi. Terdapat 402 grup; seed
`20261124` menghasilkan 356 train / 76 validation / 76 test dengan
distribusi label `hoax` 133/28/29 dan `not_flagged_as_hoax` 223/48/47.
Seluruh enam leakage check lulus.

## 10. Bias dan keterbatasan

- Class imbalance: 62% `Valid`, 38% `Hoax`.
- Dataset terdiri dari 12 topik tetap, masing-masing 50 record; ini bukan
  sampel acak dari seluruh berita Indonesia.
- Tidak ada timestamp di CSV; tren temporal tidak didukung.
- Tidak ada sumber/publisher di CSV; source bias tidak dapat diukur
  secara langsung.
- Tidak ada codebook label rinci; label berasal dari tiga referee dan
  voting.
- Ada label noise, konflik CSV↔workbook, dan konflik URL.
- Near-duplicate dapat membuat model menghafal topik/gaya, bukan pola
  misinformasi yang umum.
- Label `Valid` bukan bukti kebenaran; `Hoax` bukan verdict hukum.
- Hasil model tidak boleh diklaim sebagai deteksi seluruh hoaks di
  internet.

## 11. Data governance

- Patuhi CC BY 4.0 dan ketentuan Mendeley/Elsevier.
- Cantumkan DOI, kreator, versi, lisensi, dan indikasi perubahan.
- Jangan mempublikasikan ulang raw text tanpa review hak.
- Jangan commit CSV/XLSX, model weights besar, atau data pribadi.
- Jangan menampilkan teks artikel lengkap di dashboard/API publik.
- Jangan mencatat teks mentah atau email ke log produksi.
- Simpan data hanya di penyimpanan lokal/terkelola yang tidak di-commit.
- Review hukum hak sumber berita sebelum deployment komersial.
- Jika dataset berubah, buat versi baru dan audit ulang.

## 12. Catatan versi dataset

```text
Dataset version: Mendeley p3hfgr5j3m version 1
Source(s): Mendeley Data, DOI 10.17632/p3hfgr5j3m.1
Access date: 2026-11-16
License: CC BY 4.0; third-party content caveat
Raw records: 600 (600 CSV), 250 (not used)
Records after validation: 600 (lolos baseline Stage 2)
Eligible after conflict quarantine: 508 (92 dikarantina)
Label mapping: Hoax -> hoax; Valid -> not_flagged_as_hoax
Label source preserved: ya, source_label
Duplicate handling: group URL + near-duplicate via connected components; record konflik dikarantina, bukan dihapus
Preprocessing version: Stage 3 (NFKC, HTML cleanup, URL placeholder, whitespace; lowercase/tokenization optional)
Split strategy: group-aware 70/15/15, greedy stratified, 402 grup
Random seed: 20261124
Known limitations: label noise, URL conflicts, near-duplicate, no timestamp/source
Prepared by: HoaxScope Stage 2 audit + Stage 3 pipeline (2026-11-24)
```

## 13. Checklist status

| Item | Status |
| --- | --- |
| Sumber dan pembuat teridentifikasi | Ya |
| Lisensi dan ketentuan diperiksa | Ya, dengan catatan pihak ketiga |
| Metadata/dataset card dibaca | Ya |
| Schema aktual diverifikasi | Ya |
| Definisi label dipahami | Sebagian; tidak ada codebook rinci |
| Data quality audit dijalankan | Ya |
| Duplikasi dan leakage diperiksa | Ya |
| Split strategy ditetapkan | Ya; group-aware 70/15/15, seed `20261124`, 6/6 leakage check lulus |
| Loader/validasi/preprocessing/split diimplementasikan | Ya; Stage 3, 20 unit test lulus |
| Provenance dan versi dicatat | Ya |
| Bias dan keterbatasan didokumentasikan | Ya |
| Review hukum komersial | Belum |
| Penerimaan kondisi ADR 0003 | Diterima pemilik; Stage 3 selesai, Phase 2 masih menunggu persetujuan |

## 14. Referensi

- [ADR 0003 — dataset selection & audit](docs/decisions/0003-dataset-selection.md)
- [ADR 0002 — Stage 1 dataset discovery](docs/decisions/0002-phase-1-stage-1-dataset-discovery.md)
- [Laporan audit Stage 3 — canonical schema & data pipeline](docs/experiments/stage-3-data-pipeline.md)
- Mendeley dataset: <https://data.mendeley.com/datasets/p3hfgr5j3m/1>
- CC BY 4.0: <https://creativecommons.org/licenses/by/4.0/>
- Mendeley Terms: <https://www.mendeley.com/terms/>
- Elsevier terms:
  <https://www.elsevier.com/legal/elsevier-website-terms-and-conditions>
