# HoaxScope --- Development Roadmap

> Status awal semua fase adalah **Not started**. Perbarui hanya
> berdasarkan implementasi dan validasi aktual. Per 2026-11-13, Phase 0
> berstatus **Done**; Phase 1–7 belum dimulai.

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

**Tujuan:** dataset tervalidasi dan dapat ditelusuri. - Verifikasi
sumber, lisensi, provenance, schema, dan label. - Buat loader CSV/JSON
dan schema validation. - Audit missing values, distribusi kelas,
duplikasi, panjang teks, timestamp. - Buat preprocessing reusable. -
Tentukan split dan catat versi dataset.

Acceptance criteria: - \[ \] Sumber/lisensi/provenance terdokumentasi. -
\[ \] Schema dan label jelas. - \[ \] Data quality report dapat
diulang. - \[ \] Duplikasi dan leakage diperiksa. - \[ \] Split strategy
memiliki alasan. - \[ \] Test loader/preprocessing tersedia.

## Phase 2 --- Baseline NLP

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
