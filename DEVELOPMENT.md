# HoaxScope --- Development Guide

> **Tujuan dokumen:** menjadi spesifikasi teknis dan panduan
> implementasi bagi OpenCode untuk membangun HoaxScope secara bertahap,
> konsisten, dapat diuji, dan mudah dikembangkan.
>
> **Produk:** platform analisis pola misinformasi pada teks berita
> berbahasa Indonesia menggunakan NLP dan Machine Learning.
>
> **Prinsip penting:** HoaxScope adalah alat analisis berbasis dataset
> dan model, bukan otoritas penentu kebenaran berita. Prediksi model
> tidak boleh ditampilkan sebagai bukti bahwa suatu klaim benar atau
> salah.

------------------------------------------------------------------------

## 0. Instruksi utama untuk OpenCode

Baca seluruh `DEVELOPMENT.md` sebelum mengubah atau membuat file.
Jadikan dokumen ini sumber spesifikasi utama.

### Aturan kerja

1.  Kerjakan project secara bertahap sesuai fase pada bagian 15. Jangan
    membangun semua fitur sekaligus.
2.  Sebelum coding, periksa struktur repository dan file yang sudah ada.
    Pertahankan implementasi yang valid; jangan menimpa konfigurasi
    tanpa alasan.
3.  Jika repository belum memiliki struktur, buat monorepo sesuai bagian
    3.
4.  Gunakan Python untuk data processing, training, evaluasi, dan
    inference. Gunakan FastAPI untuk API dan Next.js untuk dashboard.
5.  Jangan membuat data, hasil eksperimen, skor evaluasi, atau klaim
    performa palsu. Data contoh harus diberi label `mock` atau
    `illustrative`.
6.  Jangan mengunduh dataset secara otomatis dari sumber yang belum
    diperiksa lisensi, format, dan ketentuan penggunaannya.
7.  Jangan melakukan scraping situs berita atau media sosial tanpa
    memeriksa ketentuan layanan, robots policy, hak cipta, dan privasi.
8.  Jangan memasukkan dataset besar, secret, token, credential, atau
    model weights ke Git biasa.
9.  Buat test untuk setiap modul penting. Jangan menyatakan fitur
    selesai sebelum test relevan berhasil.
10. Gunakan type hints, validasi input, logging, error handling, dan
    konfigurasi melalui environment variables.
11. Hindari overengineering. Implementasikan fitur minimum yang benar
    terlebih dahulu, lalu tingkatkan.
12. Bila keputusan penting belum ditentukan dokumen ini, pilih default
    yang sederhana, dokumentasikan asumsi di `docs/decisions/`, dan
    lanjutkan. Tanyakan kepada pemilik project hanya jika keputusan
    tersebut berisiko mengubah scope, biaya, keamanan, atau sumber data.
13. Setelah setiap fase, laporkan file yang dibuat/diubah, perintah yang
    dijalankan, hasil test, keterbatasan, dan langkah berikutnya.

### Definition of Done

Sebuah fitur dianggap selesai jika: - implementasi sesuai spesifikasi; -
input tervalidasi dan error ditangani; - terdapat test yang relevan; -
dokumentasi diperbarui; - tidak ada secret atau data privat yang
ter-commit; - lint/type-check/test terkait berhasil; - hasil yang belum
benar-benar dijalankan tidak diklaim berhasil.

------------------------------------------------------------------------

## 1. Ringkasan produk

### 1.1 Nama

**HoaxScope --- Indonesian Misinformation & News Intelligence**

### 1.2 Tujuan

Membangun sistem yang dapat: - mengklasifikasikan teks berita
berdasarkan label dataset; - menganalisis karakteristik linguistik
teks; - menemukan berita dengan narasi semantik yang mirip; - menemukan
kelompok topik dari kumpulan berita; - menganalisis distribusi label dan
topik berdasarkan waktu jika timestamp memadai; - membandingkan
algoritma dan konfigurasi preprocessing; - menjelaskan faktor yang
memengaruhi prediksi; - menyediakan REST API dan dashboard analitik.

### 1.3 Bukan tujuan

Versi awal tidak dimaksudkan untuk: - memastikan kebenaran berita secara
otomatis; - menggantikan jurnalis atau pemeriksa fakta; - menyimpulkan
bahwa sebuah sumber selalu hoaks; - melakukan scraping agresif atau
otomatisasi penyebaran konten; - memprofilkan individu atau
mengidentifikasi penulis; - memprediksi niat atau afiliasi politik
seseorang.

### 1.4 Prinsip komunikasi hasil

Gunakan istilah: - `predicted_label`; - `model_confidence`; -
`dataset_label`; - `similarity_score`; - `topic_assignment`; -
`pattern_analysis`.

Hindari label UI seperti "Berita ini terbukti hoaks" hanya berdasarkan
prediksi model.

Tampilkan disclaimer yang jelas:

> Hasil ini merupakan prediksi model berdasarkan pola pada dataset dan
> bukan verifikasi fakta. Periksa sumber primer dan referensi
> pemeriksaan fakta sebelum mengambil keputusan.

------------------------------------------------------------------------

## 2. Scope produk

### 2.1 MVP --- wajib

1.  Dataset ingestion dari file CSV/JSON lokal.
2.  Validasi skema, deduplikasi, dan data quality report.
3.  Exploratory Data Analysis.
4.  Preprocessing teks bahasa Indonesia yang dapat dikonfigurasi.
5.  Baseline TF-IDF + Multinomial Naive Bayes.
6.  TF-IDF + Logistic Regression.
7.  TF-IDF + Linear SVM.
8.  Fine-tuning IndoBERT sebagai eksperimen lanjutan.
9.  Evaluasi dengan metrik klasifikasi.
10. Model registry sederhana dan metadata versi.
11. Single prediction dan batch prediction.
12. FastAPI REST API.
13. Dashboard untuk overview, analyzer, dan model benchmark.
14. Docker Compose untuk menjalankan aplikasi.
15. Unit test, integration test, dokumentasi, dan CI.

### 2.2 Fitur lanjutan

Implementasikan setelah MVP stabil: - semantic similarity menggunakan
Sentence Transformers; - topic modeling menggunakan BERTopic; - LDA/NMF
sebagai pembanding topic modeling; - SHAP/LIME atau token attribution; -
temporal trend analysis; - forecasting jumlah artikel per topik/label; -
external fact-check reference retrieval; - monitoring data drift dan
model drift.

### 2.3 Di luar MVP

-   real-time crawling seluruh internet;
-   browser extension;
-   automated social media posting;
-   klaim verifikasi fakta otomatis;
-   distributed GPU training;
-   multi-tenant SaaS kompleks.

------------------------------------------------------------------------

## 3. Teknologi dan struktur repository

### 3.1 Stack yang dipilih

  -----------------------------------------------------------------------
  Area                                Teknologi
  ----------------------------------- -----------------------------------
  Bahasa ML                           Python 3.11+

  Data processing                     Pandas, NumPy

  Traditional ML                      Scikit-learn

  NLP transformer                     Hugging Face Transformers

  Deep learning                       PyTorch

  Indonesian model                    IndoBERT, model card diverifikasi
                                      sebelum digunakan

  Topic modeling                      BERTopic (lanjutan)

  Semantic similarity                 Sentence Transformers (lanjutan)

  Experiment tracking                 MLflow (fase lanjutan)

  Hyperparameter tuning               Optuna (fase lanjutan)

  Explainability                      SHAP/LIME (fase lanjutan)

  API                                 FastAPI + Pydantic

  Frontend                            Next.js + TypeScript

  Styling                             Tailwind CSS

  Charting                            Plotly atau library chart React
                                      yang terpelihara

  Database                            PostgreSQL

  Cache/queue                         Redis, hanya jika dibutuhkan

  Testing Python                      pytest

  Testing frontend                    Vitest + Testing Library

  E2E                                 Playwright, fase deployment

  Container                           Docker + Docker Compose

  CI                                  GitHub Actions
  -----------------------------------------------------------------------

Pilih versi package yang saling kompatibel dan pin versi dependency.
Jangan mengasumsikan versi terbaru selalu kompatibel.

### 3.2 Struktur monorepo

``` text
hoaxscope/
├── apps/
│   ├── api/
│   │   ├── app/
│   │   │   ├── api/v1/
│   │   │   ├── core/
│   │   │   ├── schemas/
│   │   │   ├── services/
│   │   │   ├── repositories/
│   │   │   ├── db/
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── Dockerfile
│   └── web/
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   ├── features/
│       │   ├── lib/
│       │   └── types/
│       ├── public/
│       ├── package.json
│       └── Dockerfile
├── ml/
│   ├── configs/
│   ├── data/
│   │   ├── raw/.gitkeep
│   │   ├── interim/.gitkeep
│   │   └── processed/.gitkeep
│   ├── notebooks/
│   ├── src/hoaxscope_ml/
│   │   ├── data/
│   │   ├── preprocessing/
│   │   ├── features/
│   │   ├── models/
│   │   ├── training/
│   │   ├── evaluation/
│   │   ├── inference/
│   │   └── analysis/
│   ├── scripts/
│   ├── tests/
│   └── pyproject.toml
├── artifacts/
│   └── .gitkeep
├── docs/
│   ├── architecture.md
│   ├── dataset.md
│   ├── methodology.md
│   ├── api.md
│   ├── model-card.md
│   ├── experiment-log.md
│   └── decisions/
├── infra/
│   ├── postgres/
│   └── scripts/
├── .github/workflows/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── README.md
└── DEVELOPMENT.md
```

Boleh sesuaikan struktur jika repository sudah memiliki pola yang baik,
tetapi pisahkan dengan jelas: - frontend; - API; - ML pipeline; -
data/artifacts; - dokumentasi dan infrastruktur.

### 3.3 Dependency management

Gunakan `pyproject.toml` untuk package Python dan lockfile package
manager frontend. Jangan mencampur beberapa dependency manager tanpa
alasan.

Sediakan command yang konsisten melalui `Makefile` atau script: -
`make install` - `make lint` - `make test` - `make data-check` -
`make train-baseline` - `make evaluate` - `make api` - `make docker-up`

Jika command belum tersedia, buat dan dokumentasikan.

------------------------------------------------------------------------

## 4. Dataset dan data governance

### 4.1 Sumber dataset awal

Periksa sumber dan lisensi sebelum mengunduh atau mendistribusikan
ulang.

1.  BRIN Fake News Mafindo:
    `https://huggingface.co/datasets/nlp-brin-id/fakenews-mafindo`
2.  BRIN Indonesian Hoax Report:
    `https://huggingface.co/datasets/nlp-brin-id/id-hoax-report`
3.  Open Data fact-checking Jawa Barat:
    `https://data.go.id/dataset/dataset/data-pengecekan-fakta-fact-checking`
4.  Dataset tambahan hanya jika memiliki provenance, label, dan izin
    penggunaan yang jelas.

Jangan menganggap dataset berbeda dapat langsung digabungkan. Skema
label, sumber, periode, dan unit analisis mungkin berbeda.

### 4.2 Dataset adapter

Buat adapter terpisah untuk setiap dataset, misalnya: -
`mafindo_adapter.py` - `id_hoax_report_adapter.py` -
`jabar_factcheck_adapter.py`

Setiap adapter mengubah data sumber ke canonical schema HoaxScope.

### 4.3 Canonical schema

Field internal yang disarankan:

  Field            Tipe         Wajib Keterangan
  ---------------- ---------- ------- ------------------------------
  article_id       string          Ya ID internal stabil
  title            string       Tidak Judul/klaim
  content          string          Ya Teks utama
  source_name      string       Tidak Sumber jika tersedia
  source_url       string       Tidak URL referensi jika diizinkan
  published_at     datetime     Tidak Tanggal publikasi
  factcheck_date   datetime     Tidak Tanggal pemeriksaan
  label            string          Ya Label asli dan/atau mapped
  label_detail     string       Tidak Kategori detail
  fact             string       Tidak Penjelasan pemeriksa fakta
  references       array        Tidak Referensi sumber
  dataset_name     string          Ya Asal dataset
  split_group      string       Tidak Group untuk mencegah leakage

Simpan label asli. Jangan menghapus informasi label sumber ketika
melakukan mapping.

### 4.4 Label mapping

Jangan mengasumsikan semua dataset memakai definisi label yang sama.

Untuk baseline biner, buat mapping yang eksplisit dan dapat
dikonfigurasi, contohnya: - `HOAX` → `misleading_or_false` - `NON-HOAX`
→ `not_flagged_as_hoax`

Nama label kedua sengaja tidak menggunakan `TRUE`, karena NON-HOAX tidak
selalu berarti setiap klaim telah diverifikasi benar.

Untuk label multi-kelas, simpan kategori asli seperti fabricated
content, false context, false connection, manipulated content,
misleading content, impostor content, satire, dan label lain sesuai
dataset. Mapping hanya dilakukan setelah definisi setiap label
dipelajari.

Dokumentasikan label yang: - tidak dapat dipetakan; - ambigu; - tidak
tersedia; - atau perlu dikeluarkan dari eksperimen tertentu.

### 4.5 Validasi data

Buat laporan otomatis yang memeriksa: - missing title/content/label; -
duplicate exact text; - duplicate URL; - near-duplicate text; - label
distribution; - source distribution; - date coverage; - text length
distribution; - invalid dates; - conflicting labels; - data overlap
antar-split.

Jangan menghapus duplikat secara membabi buta. Simpan laporan dan alasan
penghapusan.

### 4.6 Data privacy dan licensing

-   Jangan menyimpan data pribadi yang tidak diperlukan.
-   Jangan mempublikasikan ulang dataset jika lisensinya tidak
    mengizinkan.
-   Jangan memasukkan raw data besar ke Git.
-   Sediakan `ml/data/README.md` yang menjelaskan cara memperoleh
    dataset.
-   Buat synthetic sample kecil hanya untuk unit test dan beri label
    jelas sebagai data sintetis.

------------------------------------------------------------------------

## 5. NLP preprocessing

Implementasikan preprocessing sebagai pipeline yang dapat dikonfigurasi
dan diuji.

### 5.1 Tahapan umum

1.  Unicode normalization.
2.  HTML/entity cleanup jika data memang mengandung markup.
3.  Whitespace normalization.
4.  URL handling.
5.  Token/character statistics.
6.  Optional slang normalization.
7.  Optional stopword removal.
8.  Optional stemming untuk eksperimen traditional ML.

### 5.2 Dua pipeline terpisah

**Traditional ML** - cleaning; - normalization; - optional stopword
removal; - optional stemming; - TF-IDF word n-grams dan/atau character
n-grams.

**Transformer** - cleaning minimal; - pertahankan tanda baca dan konteks
yang relevan; - gunakan tokenizer bawaan checkpoint; - jangan melakukan
stemming atau stopword removal secara default.

### 5.3 Leakage prevention

-   Fit TF-IDF hanya pada training set.
-   Transform validation/test menggunakan vectorizer yang sudah fit pada
    training.
-   Jangan menghitung vocabulary dari keseluruhan dataset.
-   Jangan menggunakan `fact`, `references`, atau hasil fact-check
    sebagai fitur input jika informasi tersebut tidak tersedia saat
    prediksi berita baru.
-   Jangan menggunakan label turunan atau metadata yang secara langsung
    mengungkap target.
-   Seluruh preprocessing yang dipelajari dari data harus fit pada
    training fold saja.

### 5.4 Test preprocessing

Buat test untuk: - empty string; - null value; - emoji; - URL; - HTML; -
repeated whitespace; - mixed case; - informal spelling; - punctuation; -
teks sangat panjang; - teks berbahasa campuran.

------------------------------------------------------------------------

## 6. Experiment design

### 6.1 Eksperimen baseline

Model wajib: 1. Multinomial Naive Bayes + TF-IDF. 2. Logistic
Regression + TF-IDF. 3. Linear SVM + TF-IDF.

Model lanjutan: 4. BiLSTM jika data dan resource memadai. 5. IndoBERT
fine-tuning.

Jangan menjalankan seluruh model sekaligus jika resource terbatas.
Prioritaskan baseline yang reproducible terlebih dahulu.

### 6.2 Split strategy

Default: - train: 70%; - validation: 15%; - test: 15%.

Gunakan stratified split jika sesuai dengan distribusi label.

Namun, sebelum split: 1. lakukan exact deduplication; 2. identifikasi
near-duplicate dan artikel yang bersumber dari klaim yang sama; 3.
bentuk group agar satu klaim/berita tidak tersebar ke train dan test; 4.
pertimbangkan source-based atau temporal split sebagai evaluasi
tambahan.

Untuk temporal generalization, latih pada periode lebih awal dan uji
pada periode lebih baru jika timestamp memadai.

Jangan mengubah test set berulang kali untuk tuning. Gunakan validation
set untuk pemilihan model.

### 6.3 Metrik utama

Untuk klasifikasi: - Macro F1 --- metrik utama; - per-class Precision,
Recall, F1; - confusion matrix; - accuracy sebagai metrik pendamping; -
PR-AUC untuk class imbalance; - ROC-AUC jika interpretasinya sesuai; -
calibration metric jika confidence digunakan.

Untuk efisiensi: - training duration; - inference latency; -
throughput; - model artifact size; - peak memory jika dapat diukur.

Untuk topic modeling: - topic coherence; - topic diversity; - human
inspection; - silhouette score hanya jika representasi dan asumsi metrik
sesuai.

Untuk similarity: - Precision@K / Recall@K jika ada relevance labels; -
human relevance assessment jika belum ada label; - latency.

Untuk forecasting: - MAE; - RMSE; - sMAPE jika tidak ada masalah nilai
nol; - chronological backtesting.

### 6.4 Eksperimen preprocessing

Buat experiment matrix yang membandingkan: - minimal cleaning; -
normalization; - normalization + stopword removal; - normalization +
stemming; - word n-grams; - character n-grams; - kombinasi word +
character features.

Jangan mengasumsikan stemming atau stopword removal selalu meningkatkan
performa.

### 6.5 Hyperparameter tuning

Gunakan Optuna setelah baseline stabil.

Contoh parameter: - TF-IDF `ngram_range`, `min_df`, `max_df`,
`max_features`; - Logistic Regression `C`, `class_weight`; - Linear SVM
`C`, `class_weight`; - IndoBERT `learning_rate`, `batch_size`, `epochs`,
`weight_decay`, `max_length`.

Tuning hanya menggunakan training/validation. Test set tetap untouched
sampai evaluasi final.

### 6.6 Reproducibility

Set random seed dan catat: - dataset version/fingerprint; - split
strategy; - preprocessing config; - model checkpoint; - package
versions; - hyperparameters; - metrics; - hardware/runtime; -
timestamp; - git commit hash bila tersedia.

Setiap eksperimen menghasilkan file metadata JSON dan laporan
Markdown/CSV.

------------------------------------------------------------------------

## 7. Model artifacts dan inference

### 7.1 Model interface

Buat interface seragam sehingga API tidak perlu mengetahui detail
implementasi model.

Konsep interface: - `load()` - `predict(texts)` - `predict_proba(texts)`
jika didukung - `metadata()`

Jika model tidak mendukung probabilitas terkalibrasi, jangan menyebut
output decision score sebagai confidence probability.

### 7.2 Model metadata

Setiap model artifact harus memiliki metadata: - model name; - model
version; - model family; - checkpoint; - label mapping; - preprocessing
version; - training dataset; - training timestamp; - evaluation
metrics; - artifact checksum; - intended use; - limitations.

### 7.3 Model selection

Sediakan konfigurasi model aktif melalui environment/config, bukan
hardcode pada endpoint.

Contoh: `ACTIVE_MODEL=indobert-v1`

Jika artifact tidak tersedia: - berikan error yang jelas; - jangan
diam-diam mengganti dengan model lain; - dokumentasikan cara training
atau memperoleh artifact.

### 7.4 Confidence dan calibration

-   Tampilkan nilai confidence hanya jika model menghasilkan
    probabilitas yang bermakna.
-   Pertimbangkan calibration menggunakan validation set.
-   Tampilkan "uncertain" atau "needs review" ketika confidence rendah
    atau input out-of-distribution.
-   Confidence tinggi bukan bukti kebenaran.

------------------------------------------------------------------------

## 8. Fitur lanjutan: similarity, topic, explainability, trends

### 8.1 Semantic similarity

Gunakan Sentence Transformers atau embedding model bahasa
Indonesia/multilingual yang model card dan lisensinya sudah diperiksa.

Pipeline: 1. encode artikel; 2. simpan embedding; 3. hitung cosine
similarity; 4. ambil top-K; 5. tampilkan artikel sumber, tanggal, label
dataset, dan similarity score.

Jika dataset kecil, implementasi awal dapat menggunakan exact cosine
search. Vector database baru diperlukan ketika ukuran data menuntutnya.

### 8.2 Topic modeling

Bandingkan: - LDA; - NMF; - BERTopic.

Jangan menyatakan topic sebagai kategori fakta. Topic merupakan kelompok
pola isi dokumen yang perlu interpretasi manusia.

### 8.3 Explainability

Gunakan: - SHAP/LIME untuk model yang kompatibel; - token attribution
untuk transformer dengan metode yang sesuai.

Jelaskan bahwa fitur penting menunjukkan kontribusi terhadap keputusan
model, bukan bukti suatu klaim benar atau salah.

### 8.4 Temporal analysis dan forecasting

Hanya aktifkan jika: - timestamp valid; - coverage waktu cukup; - volume
per periode memadai; - periode observasi konsisten.

Agregasikan jumlah artikel per hari/minggu/bulan sesuai volume. Gunakan
chronological split dan backtesting. Jangan memprediksi tren dari data
yang terlalu sedikit atau tanggal yang tidak dapat dipercaya.

------------------------------------------------------------------------

## 9. Backend API

Gunakan FastAPI, Pydantic, dan OpenAPI.

### 9.1 Endpoint MVP

  Method   Endpoint                       Fungsi
  -------- ------------------------------ ---------------------
  GET      `/api/v1/health`               Health check
  GET      `/api/v1/models`               Model yang tersedia
  POST     `/api/v1/predict`              Single prediction
  POST     `/api/v1/predict/batch`        Batch prediction
  GET      `/api/v1/analytics/overview`   Statistik overview
  GET      `/api/v1/analytics/labels`     Distribusi label
  GET      `/api/v1/experiments`          Hasil benchmark

### 9.2 Endpoint lanjutan

  Method   Endpoint                     Fungsi
  -------- ---------------------------- ------------------------
  POST     `/api/v1/analyze`            Analisis teks lengkap
  POST     `/api/v1/similarity`         Cari berita serupa
  GET      `/api/v1/topics`             Daftar topic
  GET      `/api/v1/analytics/trends`   Temporal trends
  GET      `/api/v1/articles/{id}`      Detail artikel dataset

### 9.3 Contoh request

``` json
{
  "title": "Contoh judul berita",
  "content": "Isi berita yang akan dianalisis.",
  "model_name": "indobert-v1"
}
```

### 9.4 Contoh response

``` json
{
  "data": {
    "predicted_label": "misleading_or_false",
    "scores": {
      "misleading_or_false": 0.82,
      "not_flagged_as_hoax": 0.18
    },
    "model": {
      "name": "indobert",
      "version": "1.0.0"
    },
    "status": "prediction"
  },
  "disclaimer": "Prediksi model berdasarkan pola dataset, bukan verifikasi fakta."
}
```

Contoh di atas hanya kontrak ilustratif. Implementasi harus mengikuti
label mapping aktual dan model yang benar-benar tersedia.

### 9.5 API requirements

-   validasi panjang title/content;
-   batasi ukuran request dan batch;
-   handle empty text;
-   response schema konsisten;
-   HTTP status code yang tepat;
-   logging tanpa menyimpan teks sensitif secara default;
-   CORS hanya untuk origin frontend yang dikonfigurasi;
-   rate limiting jika API dipublikasikan;
-   jangan expose internal filesystem path atau stack trace ke client.

------------------------------------------------------------------------

## 10. Database

Gunakan PostgreSQL. Untuk MVP, SQLAlchemy 2.x dan Alembic dapat
digunakan.

Tabel minimum:

### `articles`

-   id
-   title
-   content
-   source_name
-   source_url
-   published_at
-   dataset_name
-   created_at

### `article_labels`

-   id
-   article_id
-   original_label
-   normalized_label
-   label_detail
-   label_source

### `model_versions`

-   id
-   model_name
-   version
-   model_family
-   artifact_uri
-   metadata_json
-   created_at

### `predictions`

-   id
-   article_id nullable
-   model_version_id
-   input_hash
-   predicted_label
-   scores_json
-   created_at

### `experiment_runs`

-   id
-   experiment_name
-   model_name
-   dataset_fingerprint
-   config_json
-   metrics_json
-   artifact_uri
-   created_at

### `topics`

-   id
-   topic_model_version
-   topic_index
-   topic_name
-   keywords_json

### `article_topics`

-   article_id
-   topic_id
-   score

### `similar_articles`

-   article_id
-   matched_article_id
-   similarity_score
-   model_version

Tambahkan index pada kolom yang sering difilter seperti label,
published_at, dataset_name, dan foreign keys.

Jangan menyimpan seluruh raw training dataset ke tabel produksi jika
tidak diperlukan. File data dapat tetap berada di storage lokal/object
storage dengan metadata dan provenance di PostgreSQL.

------------------------------------------------------------------------

## 11. Frontend dashboard

Gunakan Next.js + TypeScript + Tailwind.

### Halaman MVP

1.  **Overview**
    -   jumlah artikel dataset;
    -   distribusi label;
    -   distribusi sumber;
    -   distribusi tanggal;
    -   model aktif;
    -   ringkasan hasil eksperimen.
2.  **News Analyzer**
    -   input title dan content;
    -   pilihan model;
    -   hasil prediksi;
    -   skor tiap kelas;
    -   disclaimer;
    -   loading, error, dan empty states.
3.  **Model Benchmark**
    -   tabel perbandingan model;
    -   Macro F1;
    -   Precision/Recall;
    -   training time;
    -   inference latency;
    -   confusion matrix.

### Halaman lanjutan

4.  Narrative Explorer.
5.  Topic Intelligence.
6.  Trend Analysis.
7.  Experiment Details.

### UI requirements

-   desain responsif;
-   aksesibilitas keyboard;
-   label dan tooltip yang jelas;
-   tidak menggunakan data mock sebagai statistik nyata;
-   setiap chart memiliki sumber data dan periode;
-   bedakan dataset label dari model prediction;
-   tampilkan disclaimer pada halaman prediksi.

Jika API belum tersedia, gunakan mock data hanya untuk pengembangan UI
dan tandai secara eksplisit.

------------------------------------------------------------------------

## 12. Testing dan quality assurance

### 12.1 ML tests

-   canonical schema validation;
-   preprocessing unit tests;
-   no train/test overlap;
-   deterministic split;
-   TF-IDF fitted only on training;
-   label mapping tests;
-   model save/load;
-   prediction output schema;
-   inference on empty and long input;
-   evaluation metric correctness.

### 12.2 API tests

-   health endpoint;
-   valid prediction;
-   empty input;
-   oversized input;
-   unknown model;
-   model artifact missing;
-   batch limit;
-   validation errors;
-   database unavailable.

### 12.3 Frontend tests

-   analyzer form validation;
-   loading state;
-   prediction result rendering;
-   error state;
-   disclaimer visibility;
-   chart empty state.

### 12.4 Quality commands

Sediakan dan dokumentasikan: - Python formatting/lint; - Python type
checking; - pytest; - frontend lint; - frontend type-check; - frontend
tests; - production build.

Gunakan tools yang dipilih secara konsisten, misalnya Ruff, mypy atau
pyright, pytest, ESLint, dan TypeScript compiler.

------------------------------------------------------------------------

## 13. Security, ethics, dan reliability

1.  Jangan menyimpan API keys di source code.
2.  Sediakan `.env.example` tanpa nilai secret.
3.  Validasi file upload berdasarkan ukuran dan tipe.
4.  Jangan mengeksekusi file atau URL yang diberikan pengguna.
5.  Jangan melakukan auto-fetch URL berita tanpa kontrol SSRF.
6.  Batasi request dan batch size.
7.  Jangan log full article content secara default.
8.  Jangan menampilkan prediksi sebagai keputusan faktual.
9.  Tampilkan sumber dataset, model version, dan batasan.
10. Sediakan mekanisme koreksi/feedback untuk evaluasi manusia, bukan
    otomatis mengubah label training.
11. Lindungi endpoint internal dan dokumentasi admin bila deployment
    membutuhkan autentikasi.
12. Jangan melakukan retraining otomatis dari feedback tanpa review dan
    quality checks.

------------------------------------------------------------------------

## 14. Environment variables

Buat `.env.example` seperti berikut:

``` dotenv
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000

DATABASE_URL=postgresql+psycopg://hoaxscope:hoaxscope_dev@postgres:5432/hoaxscope

ACTIVE_MODEL=baseline-svm
MODEL_ARTIFACT_DIR=./artifacts
DATA_DIR=./ml/data

FRONTEND_ORIGIN=http://localhost:3000

REDIS_URL=redis://redis:6379/0
```

Sesuaikan variable dengan implementasi. Redis boleh dihilangkan dari
compose MVP jika belum digunakan. Credential di atas hanya contoh
development lokal dan tidak boleh digunakan pada production.

------------------------------------------------------------------------

## 15. Tahapan implementasi untuk OpenCode

Ikuti urutan ini. Jangan melompat ke tahap deployment sebelum fondasi
data dan model dapat diuji.

### Phase 0 --- Repository inspection & planning

-   periksa repository;
-   identifikasi file yang sudah ada;
-   buat implementation plan;
-   catat asumsi;
-   buat struktur folder minimum;
-   buat `.gitignore`, `.env.example`, dan README awal.

**Acceptance criteria:** struktur jelas, instruksi setup tersedia, tidak
ada file existing yang rusak.

### Phase 1 --- Dataset pipeline

-   buat canonical schema;
-   buat dataset adapters;
-   buat data validation;
-   buat deduplication report;
-   buat label mapping config;
-   buat EDA notebook/script;
-   dokumentasikan dataset provenance.

**Acceptance criteria:** dataset dapat dimuat, divalidasi, dan
menghasilkan data quality report. Tidak ada split leakage yang
diketahui.

### Phase 2 --- Baseline ML

-   implementasikan preprocessing;
-   implementasikan TF-IDF;
-   latih Naive Bayes;
-   latih Logistic Regression;
-   latih Linear SVM;
-   evaluasi dengan split yang sama;
-   simpan metrics dan config.

**Acceptance criteria:** seluruh baseline dapat dijalankan ulang dan
menghasilkan laporan metrik.

### Phase 3 --- IndoBERT & optimization

-   periksa model card dan lisensi checkpoint;
-   implementasikan tokenizer dan fine-tuning;
-   gunakan validation set;
-   simpan best checkpoint;
-   lakukan error analysis;
-   bandingkan dengan baseline;
-   tuning dengan Optuna jika resource memadai.

**Acceptance criteria:** model dapat di-load dan inference. Perbandingan
menggunakan test set yang sama dan tidak digunakan untuk tuning.

### Phase 4 --- Advanced analysis

-   implementasikan semantic similarity;
-   implementasikan topic modeling;
-   buat topic evaluation;
-   buat temporal analysis jika data memadai;
-   buat explainability;
-   dokumentasikan batasan.

**Acceptance criteria:** tiap modul mempunyai test dan output yang dapat
ditelusuri ke input/model version.

### Phase 5 --- API & database

-   setup PostgreSQL;
-   buat migrations;
-   implementasikan model registry;
-   implementasikan prediction service;
-   implementasikan endpoints;
-   buat API tests.

**Acceptance criteria:** API berjalan dan dapat melayani prediction
menggunakan artifact nyata.

### Phase 6 --- Dashboard

-   buat layout dan navigation;
-   implementasikan Overview;
-   implementasikan News Analyzer;
-   implementasikan Model Benchmark;
-   integrasikan API;
-   tambahkan loading/error/empty states;
-   buat frontend tests.

**Acceptance criteria:** dashboard menampilkan data dari API, bukan mock
data, kecuali halaman development yang diberi label.

### Phase 7 --- Docker, CI, dan documentation

-   buat Dockerfile API;
-   buat Dockerfile frontend;
-   buat docker-compose;
-   tambahkan health checks;
-   tambahkan GitHub Actions;
-   dokumentasikan setup dan deployment;
-   buat model card.

**Acceptance criteria:** clean setup dapat dijalankan dari dokumentasi
dan CI menjalankan lint/test/build.

------------------------------------------------------------------------

## 16. GitHub Actions

Buat workflow minimal untuk: - Python lint; - Python tests; - frontend
lint; - frontend type-check; - frontend tests; - frontend build.

Jangan jalankan full IndoBERT training pada setiap CI karena memerlukan
resource besar. Gunakan unit tests dengan synthetic fixtures dan smoke
tests yang ringan.

Training eksperimen dijalankan secara eksplisit atau melalui workflow
manual.

------------------------------------------------------------------------

## 17. README dan dokumentasi final

README harus memuat: 1. Project overview. 2. Problem statement. 3.
Features. 4. Screenshots. 5. Architecture diagram. 6. Tech stack. 7.
Dataset sources dan license. 8. Installation. 9. Environment setup. 10.
Running with Docker. 11. Training baseline. 12. Evaluation results yang
benar-benar dihasilkan. 13. API documentation. 14. Model limitations.
15. Responsible use disclaimer.

Dokumen tambahan: - `docs/dataset.md` - `docs/methodology.md` -
`docs/architecture.md` - `docs/api.md` - `docs/model-card.md` -
`docs/experiment-log.md`

------------------------------------------------------------------------

## 18. Prompt kerja yang disarankan untuk OpenCode

Gunakan prompt berikut untuk memulai. Berikan satu fase per sesi agar
perubahan dapat ditinjau.

### Prompt pertama --- inspeksi dan rencana

``` text
Baca DEVELOPMENT.md secara menyeluruh.

Periksa repository saat ini. Jangan langsung mengimplementasikan seluruh aplikasi.
Buat rencana implementasi berdasarkan Phase 0 dan Phase 1.
Identifikasi struktur existing, risiko kompatibilitas, dependency, dan file yang perlu dibuat.
Jangan mengunduh dataset sebelum memeriksa sumber dan lisensinya.
Setelah inspeksi, implementasikan hanya fondasi Phase 0.
Jalankan pemeriksaan yang relevan dan laporkan hasilnya.
```

### Prompt kedua --- dataset pipeline

``` text
Lanjutkan Phase 1 berdasarkan DEVELOPMENT.md.
Implementasikan canonical dataset schema, adapter untuk dataset yang benar-benar tersedia,
label mapping yang eksplisit, validasi data, deduplication report, dan EDA.
Jangan mengarang nama kolom atau label dataset. Periksa file dataset aktual terlebih dahulu.
Tambahkan unit tests dengan synthetic fixtures.
Dokumentasikan provenance, lisensi, dan keterbatasan data.
```

### Prompt ketiga --- baseline ML

``` text
Lanjutkan Phase 2 berdasarkan DEVELOPMENT.md.
Implementasikan pipeline TF-IDF + Multinomial Naive Bayes,
TF-IDF + Logistic Regression, dan TF-IDF + Linear SVM.
Pastikan preprocessing dan vectorizer fit hanya pada training data.
Gunakan split strategy yang mencegah duplicate/group leakage.
Simpan konfigurasi, metrik, confusion matrix, dan hasil eksperimen.
Jangan mengarang hasil evaluasi.
```

### Prompt keempat --- IndoBERT

``` text
Lanjutkan Phase 3 berdasarkan DEVELOPMENT.md.
Periksa model card, lisensi, dan kompatibilitas checkpoint IndoBERT.
Implementasikan fine-tuning dengan validation set, best checkpoint,
reproducibility, dan evaluasi yang sebanding dengan baseline.
Jangan menggunakan test set untuk tuning.
Jika resource tidak cukup, buat implementasi yang dapat dijalankan secara lokal
atau di environment GPU dan dokumentasikan kebutuhannya.
```

### Prompt kelima --- API dan dashboard

``` text
Lanjutkan Phase 5 dan Phase 6 secara berurutan.
Bangun FastAPI dan PostgreSQL terlebih dahulu, kemudian dashboard Next.js.
Gunakan model artifact nyata untuk prediction.
Jika model belum tersedia, tampilkan status model belum tersedia; jangan membuat prediksi palsu.
Buat integration tests dan dokumentasikan seluruh endpoint.
```

### Prompt keenam --- final quality review

``` text
Lakukan audit project berdasarkan seluruh acceptance criteria DEVELOPMENT.md.
Periksa keamanan, data leakage, model reproducibility, API validation,
frontend states, Docker, CI, dokumentasi, dan lisensi dataset/model.
Jalankan semua pemeriksaan yang relevan.
Perbaiki masalah yang ditemukan dan buat laporan:
- fitur selesai;
- fitur belum selesai;
- hasil test;
- risiko dan keterbatasan;
- instruksi menjalankan project dari clean setup.
Jangan menyatakan project production-ready jika masih ada acceptance criteria penting yang belum terpenuhi.
```

------------------------------------------------------------------------

## 19. Prioritas keputusan teknis

Jika harus memilih implementasi paling sederhana untuk MVP:

  Area                                  Keputusan awal
  ------------------------------------- ---------------------------------------------
  Klasifikasi utama                     Binary classification sesuai label dataset
  Baseline terbaik untuk dibandingkan   TF-IDF + Linear SVM
  Advanced model                        IndoBERT
  Metrik utama                          Macro F1
  Dataset utama                         BRIN Fake News Mafindo
  API                                   FastAPI
  Dashboard                             Next.js
  Database                              PostgreSQL
  Model tracking                        File metadata dahulu, MLflow kemudian
  Vector storage                        Belum wajib untuk MVP
  Forecasting                           Fase lanjutan, hanya jika timestamp memadai

**Keputusan ini adalah starting point, bukan asumsi bahwa SVM atau
IndoBERT pasti menjadi model terbaik. Hasil eksperimen yang
menentukan.**

------------------------------------------------------------------------

## 20. Hasil akhir yang diharapkan

HoaxScope versi portfolio harus memiliki:

-   [ ] Dataset pipeline yang reproducible.
-   [ ] Data quality dan leakage report.
-   [ ] Minimal tiga baseline ML.
-   [ ] IndoBERT fine-tuning atau dokumentasi alasan belum dijalankan.
-   [ ] Perbandingan metrik yang valid.
-   [ ] Model artifact dan metadata.
-   [ ] Single dan batch prediction API.
-   [ ] Dashboard analitik.
-   [ ] Model benchmark visualization.
-   [ ] Topic/similarity analysis sebagai fitur lanjutan.
-   [ ] Docker Compose.
-   [ ] Automated tests dan GitHub Actions.
-   [ ] README, architecture diagram, dataset documentation, dan model
    card.
-   [ ] Disclaimer dan batasan penggunaan.

**Prioritas terpenting:** bangun pipeline data dan eksperimen ML yang
valid terlebih dahulu. Dashboard hanyalah cara menyajikan hasil; nilai
utama HoaxScope terletak pada kualitas dataset, desain eksperimen,
generalisasi model, dan evaluasi yang dapat direproduksi.
