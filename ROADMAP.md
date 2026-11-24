# HoaxScope --- Development Roadmap

> Status awal semua fase adalah **Not started**. Perbarui hanya
> berdasarkan implementasi dan validasi aktual. Per 2026-11-24, Phase 0
> berstatus **Done**; Phase 1 berstatus **Done** (Stage 1 discovery, Stage 2
> dataset selection/audit, dan Stage 3 canonical schema/data pipeline
> selesai); Phase 2–7 belum dimulai. Dataset Mendeley 600-news tetap
> **conditionally approved** dan belum boleh dipakai untuk training tanpa
> persetujuan Phase 2. File dataset mentah tetap di luar repository.

## Prinsip

-   Audit dataset sebelum training.
-   Bangun baseline yang reproducible sebelum model kompleks.
-   Selesaikan dan validasi satu fase sebelum lanjut.
-   Jangan mengarang hasil atau menyatakan fitur selesai tanpa bukti.
-   Prediksi model bukan verifikasi fakta.

## Phase 0 --- Repository inspection & planning

**Status:** Done (2026-11-13). Evidence and decisions:
[docs/decisions/0001-phase-0-repository-foundation.md](docs/decisions/0001-phase-0-repository-foundation.md).

**Tujuan:** memahami repository dan menyepakati rencana. - Inspeksi
struktur, branch, stack, konfigurasi, dan kode. - Baca instruksi
proyek. - Identifikasi komponen yang dapat digunakan kembali. - Susun
implementation plan dan catat risiko/asumsi.

Acceptance criteria: - \[x\] Struktur repository dirangkum. - \[x\]
Stack dan dependency aktual diidentifikasi. - \[x\] Tidak ada file
penting diubah/dihapus tanpa alasan. - \[x\] Rencana fase berikutnya
tersedia. - \[x\] Tidak membangun seluruh aplikasi pada fase ini.

## Phase 1 --- Dataset audit & pipeline

**Status:** Done (2026-11-24). Stage 1 discovery/audit, Stage 2 dataset
selection/audit, dan Stage 3 canonical schema/data pipeline selesai.
Dataset Mendeley `p3hfgr5j3m` versi 1 (600 CSV) **conditionally approved**;
training Phase 2 masih menunggu persetujuan pemilik. Evidence:
[ADR 0002](docs/decisions/0002-phase-1-stage-1-dataset-discovery.md),
[ADR 0003](docs/decisions/0003-dataset-selection.md), dan
[laporan Stage 3](docs/experiments/stage-3-data-pipeline.md).

**Stage 1 evidence (2026-11-14):**

- Metadata, lisensi, provenance, akses, dan dokumentasi schema/label kandidat
  telah diperiksa: BRIN Dataverse v2.1, HF `fakenews-mafindo`, HF
  `id-hoax-report`, dan `data.go.id` Jabar.
- BRIN Dataverse v2.1 direkomendasikan sebagai kandidat utama kondisional;
  HF `fakenews-mafindo` hanya fallback; HF `id-hoax-report` eksploratif;
  `data.go.id` Jabar tidak disetujui.
- Pada Stage 1, file dataset belum diunduh; row count, distribusi kelas,
  duplikasi, dan schema aktual belum diverifikasi. Rekomendasi BRIN di
  Stage 1 digantikan untuk pemilihan sumber oleh ADR 0003; ADR 0002 tetap
  disimpan sebagai catatan sejarah.
- Loader, data validation, preprocessing, split, dan EDA belum dibuat.

**Stage 2 evidence (2026-11-16):**

- Sumber resmi Mendeley, DOI `10.17632/p3hfgr5j3m.1`, versi 1, lisensi
  CC BY 4.0, kontributor, dan artikel terkait diverifikasi.
- Paket resmi diunduh ke direktori sementara; hash ZIP dan enam file
  dicatat. Tidak ada file dataset yang masuk repository.
- Audit CSV 600: 600 record; 372 `Valid` / 228 `Hoax`; 0 teks kosong;
  0 exact duplicate; median 1.944 karakter.
- Audit workbook 600: 12 topik × 50 record; 9 perbedaan label CSV vs
  voting; 31 grup URL duplikat; 10 grup label konflik.
- File 250 praktis redundan (249 exact match + 1 near-duplicate) dan
  tidak dipakai.
- Near-duplicate 5-word/Jaccard ≥ 0.5: 332 pasangan; 255 record dalam
  91 komponen; group split wajib.
- Keputusan: conditionally approved; lihat ADR 0003 untuk kondisi dan
  batas penggunaan.

**Stage 3 evidence (2026-11-24):**

- Loader CP1252 strict, canonical schema berbasis row-position ID, dan
  validasi baseline 600/372/228 lolos tanpa perubahan data.
- Workbook row-order audit mereproduksi 567 URL unik, 31 grup duplikat/64
  baris, dan 9 perbedaan voting; tetap diperlakukan sebagai inferensi,
  bukan relasi resmi.
- Near-duplicate 5-word/Jaccard ≥ 0.5 mereproduksi 332 pasangan, 91
  komponen, komponen terbesar 16, dan 27 komponen dengan konflik label.
- Gabungan URL + near-duplicate menghasilkan 431 komponen; 29 komponen
  berkonflik sehingga 92 record dikarantina, bukan dihapus.
- Preprocessing modular NFKC/HTML/URL-placeholder/whitespace tanpa
  stemming atau stopword removal otomatis.
- Split group-aware seed `20261124`: 508 record layak, 402 grup,
  356/76/76 train/validation/test; 6/6 leakage check lulus.
- 20 unit test dengan fixture sintetis lulus; raw dataset tidak di-commit.

**Tujuan:** dataset tervalidasi dan dapat ditelusuri. - Verifikasi
sumber, lisensi, provenance, schema, dan label. - Buat loader CSV/JSON
dan schema validation. - Audit missing values, distribusi kelas,
duplikasi, panjang teks, timestamp. - Buat preprocessing reusable. -
Tentukan split dan catat versi dataset.

Acceptance criteria: - \[x\] Sumber/lisensi/provenance terdokumentasi
(dengan catatan hak pihak ketiga). - \[x\] Schema dan label aktual
terdokumentasi (tanpa codebook rinci). - \[x\] Data quality report
dijalankan dan metode/hash dicatat. - \[x\] Duplikasi dan leakage
diperiksa. - \[x\] Split strategy group-aware diimplementasikan dan lolos
seluruh leakage check. - \[x\] Loader, validasi, preprocessing, dan 20 unit
test tersedia dengan fixture sintetis. - \[x\] Raw text dan dataset tidak
di-commit.

Stage 3 selesai dan tidak melanjutkan ke training. Phase 2 baru boleh
dimulai setelah pemilik menyetujui penggunaan dataset dan benchmark.

## Phase 2 --- Baseline NLP

**Status:** Not started. Menunggu persetujuan pemilik untuk memakai dataset
dan benchmark hasil Stage 3.

**Tujuan:** baseline pembanding yang reproducible. - TF-IDF +
MultinomialNB. - TF-IDF + Logistic Regression. - TF-IDF + LinearSVC. -
Evaluasi Macro F1, accuracy, metrik per kelas, support, confusion
matrix. - Simpan konfigurasi, seed, versi data, dan hasil.

Acceptance criteria: - \[ \] Training dapat dijalankan melalui instruksi
terdokumentasi. - \[ \] Evaluasi menggunakan data holdout. - \[ \]
Metrik per kelas tersedia. - \[ \] Perbandingan dapat direproduksi. - \[
\] Angka hanya dilaporkan setelah eksperimen benar-benar dijalankan.

## Phase 3 --- Advanced model & optimization

**Tujuan:** menguji peningkatan dari model lanjutan. - Fine-tuning
IndoBERT jika data/komputasi mendukung. - Tuning dengan validation set
atau cross-validation. - Evaluasi kalibrasi score dan biaya komputasi. -
Bandingkan dengan baseline.

Acceptance criteria: - \[ \] Konfigurasi dan versi model tercatat. - \[
\] Protokol evaluasi adil dan konsisten. - \[ \] Test set tidak
digunakan untuk tuning. - \[ \] Limitasi komputasi didokumentasikan. -
\[ \] Keputusan berdasarkan hasil aktual.

## Phase 4 --- Advanced content intelligence

**Tujuan:** analisis tambahan yang didukung data. - Semantic
similarity. - Topic modeling (NMF/LDA/BERTopic). - Interpretability
(SHAP/LIME/token analysis). - Temporal trends jika timestamp memadai. -
Forecasting hanya bila jumlah dan rentang observasi memadai.

Acceptance criteria: - \[ \] Tujuan dan limitasi setiap analisis
jelas. - \[ \] Output dievaluasi. - \[ \] Tidak menampilkan tren dari
data waktu yang tidak memadai. - \[ \] Interpretasi tidak diklaim
sebagai sebab-akibat. - \[ \] Fitur opsional tidak menghambat baseline.

## Phase 5 --- API & persistence

**Tujuan:** expose model dan analitik melalui API. - FastAPI/Pydantic. -
Model artifact/version integration. - Health, model metadata,
prediction, batch prediction, analytics. - PostgreSQL bila persistence
dibutuhkan. - Validasi, error handling, logging, request limits.

Acceptance criteria: - \[ \] Endpoint terdokumentasi dan tervalidasi. -
\[ \] Prediksi menyertakan versi model. - \[ \] Notice prediksi bukan
fact-check tersedia. - \[ \] Error response konsisten. - \[ \] API tests
mencakup sukses/gagal. - \[ \] Tidak ada secret di repository.

## Phase 6 --- Dashboard

**Tujuan:** menyajikan hasil secara jelas. - Overview, distribusi label,
kualitas data. - Perbandingan performa model. - Input prediksi bila
disepakati. - Tampilkan keterbatasan model. - Loading, empty, error,
unavailable states.

Acceptance criteria: - \[ \] Grafik berasal dari data/API aktual. - \[
\] Metrik dan label konsisten. - \[ \] UI responsif dan aksesibel. - \[
\] Tidak ada klaim "pasti hoaks/benar". - \[ \] Test komponen utama
tersedia.

## Phase 7 --- Integration & delivery

**Tujuan:** proyek dapat dijalankan dan dipahami developer lain. -
Integrasi web, API, database, model. - Docker/Compose bila sesuai. - CI
untuk lint dan test. - README dan `.env.example`. - Audit secret,
dependency, dan file besar.

Acceptance criteria: - \[ \] Setup lokal diuji sesuai dokumentasi. - \[
\] Test utama berjalan di CI. - \[ \] `.env.example` tanpa secret. - \[
\] Data/model besar tidak ter-commit tanpa alasan. - \[ \] Dokumentasi
sesuai implementasi. - \[ \] Limitasi sistem dijelaskan.

## Definition of Done

Fase selesai bila acceptance criteria terpenuhi atau pengecualian
dijelaskan, test benar-benar dijalankan, dokumentasi diperbarui,
keamanan diperiksa, dan pekerjaan tersisa dilaporkan.

## Template status

``` text
Phase:
Status: Not started | In progress | Blocked | Done
Completed:
Validation:
Evidence / output:
Known limitations:
Next action:
```
