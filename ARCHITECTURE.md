# HoaxScope --- System Architecture

> Rancangan awal (living document). Sesuaikan dengan implementasi aktual
> dan perbarui bila ada perubahan.

## 1. Ringkasan

HoaxScope memanfaatkan NLP dan machine learning untuk mempelajari pola
pada dataset berlabel, membandingkan model, menganalisis
topik/kemiripan/tren bila data mendukung, dan menyajikan hasil melalui
API serta dashboard. HoaxScope tidak menggantikan fact-checker atau
sumber verifikasi tepercaya.

## 2. Prinsip

-   Separation of concerns: ML, API, web, dan infra terpisah.
-   Reproducibility: eksperimen mencatat konfigurasi, seed, versi data,
    dan metrik.
-   Training-serving consistency: preprocessing inference sama dengan
    pipeline training.
-   Provenance: sumber, label, lisensi, dan transformasi dataset dapat
    ditelusuri.
-   Responsible communication: prediksi bukan kebenaran faktual.
-   Bangun baseline sebelum model kompleks.

## 3. Arsitektur konseptual

``` mermaid
flowchart LR
  DS[Dataset CSV / JSON] --> ING[Ingestion & validation]
  ING --> PRE[Preprocessing & deduplication]
  PRE --> STORE[(PostgreSQL / processed data)]
  PRE --> EXP[ML experiments]
  EXP --> REG[Model artifacts & experiment metadata]
  REG --> API[FastAPI]
  STORE --> API
  API --> WEB[Next.js dashboard]
  WEB --> USER[Analyst / user]
```

  -----------------------------------------------------------------------
  Komponen                Teknologi awal          Tanggung jawab
  ----------------------- ----------------------- -----------------------
  ML pipeline             Python, Pandas,         Audit data,
                          scikit-learn            preprocessing,
                                                  training, evaluasi

  Advanced NLP            Transformers, PyTorch,  Fine-tuning lanjutan
                          IndoBERT                

  API                     FastAPI, Pydantic       Prediction, metadata
                                                  model, analytics

  Web                     Next.js, TypeScript,    Dashboard
                          Tailwind                

  Database                PostgreSQL              Metadata artikel,
                                                  label, prediksi,
                                                  eksperimen

  Visualization           Plotly                  Grafik dan analitik

  Quality                 pytest, Vitest,         Unit/integration/E2E
                          Playwright              tests

  Delivery                Docker, GitHub Actions  Environment dan CI
  -----------------------------------------------------------------------

Teknologi ini rekomendasi awal, bukan kewajiban untuk langsung dipasang
semua.

## 4. Alur data

1.  Ingest CSV/JSON dari sumber yang disetujui.
2.  Validasi schema, tipe, kolom wajib, tanggal, dan label.
3.  Normalisasi teks secara konservatif.
4.  Deteksi duplikasi exact dan near-duplicate bila diperlukan.
5.  Audit missing values, distribusi label, panjang teks, dan anomali.
6.  Catat provenance, lisensi, tanggal akses, dan versi dataset.
7.  Tentukan train/validation/test split.
8.  Training dan evaluasi; simpan konfigurasi serta artefak.
9.  API memuat artefak model dan preprocessing yang kompatibel.
10. Dashboard menampilkan data aktual dari API.

Jangan menggabungkan dataset berbeda sebelum menyelaraskan definisi
label, provenance, lisensi, dan kemungkinan overlap.

## 5. Strategi ML

### Baseline

-   TF-IDF + Multinomial Naive Bayes
-   TF-IDF + Logistic Regression
-   TF-IDF + LinearSVC

### Lanjutan

-   Fine-tuning IndoBERT.
-   Sentence Transformers untuk semantic similarity.
-   NMF/LDA/BERTopic untuk eksplorasi topik.
-   SHAP/LIME atau analisis token untuk interpretasi (bukan bukti
    kausal).

### Evaluasi

Gunakan Macro F1 sebagai metrik utama awal. Sertakan accuracy,
precision/recall/F1 per kelas, support, confusion matrix, dan
PR-AUC/ROC-AUC bila sesuai. Pilih split setelah audit sumber, duplikasi,
dan waktu. Pertimbangkan group split atau temporal split jika sesuai.
Jangan fit vectorizer pada validation/test dan jangan tuning menggunakan
test set.

## 6. API awal

Prefix `/api/v1`.

  Method   Endpoint                Tujuan
  -------- ----------------------- ------------------------------------
  GET      `/health`               Status layanan
  GET      `/models`               Metadata model
  POST     `/predict`              Prediksi satu teks
  POST     `/predict/batch`        Prediksi batch dengan batas ukuran
  GET      `/analytics/overview`   Ringkasan dataset/prediksi
  GET      `/analytics/labels`     Distribusi label
  GET      `/experiments`          Ringkasan eksperimen

Contoh request:

``` json
{
  "text": "Teks berita yang ingin dianalisis",
  "model_version": "baseline-logreg-v1"
}
```

Contoh bentuk respons (konseptual; label aktual harus mengikuti
dataset):

``` json
{
  "prediction": {"label": "label_dari_dataset", "score": 0.82},
  "model": {"name": "baseline-logreg", "version": "v1"},
  "notice": "Prediksi model bukan verifikasi fakta."
}
```

Definisikan apakah `score` merupakan decision score, probability, atau
confidence terkalibrasi. Jangan menyamakan ketiganya.

## 7. Database konseptual

  -----------------------------------------------------------------------
  Entitas                 Kolom konseptual        Keterangan
  ----------------------- ----------------------- -----------------------
  `articles`              id, text, source,       Konten/metadata sesuai
                          published_at,           kebijakan retensi
                          content_hash            

  `article_labels`        id, article_id, label,  Label dan asalnya
                          label_source            

  `model_versions`        id, name, version,      Versi model
                          artifact_uri, metadata  

  `predictions`           id, article_id,         Hasil prediksi
                          model_version_id,       
                          predicted_label, score  

  `experiment_runs`       id, dataset_version,    Catatan eksperimen
                          config, metrics         

  `topics`                id, name, method,       Topik
                          model_version           

  `article_topics`        article_id, topic_id,   Relasi artikel-topik
                          score                   

  `similar_articles`      article_id,             Kemiripan artikel
                          similar_article_id,     
                          similarity_score        
  -----------------------------------------------------------------------

Finalisasi skema setelah kebutuhan query, retensi, privasi, dan ukuran
data jelas.

## 8. Struktur repository target

``` text
HoaxScope/
├── apps/api/
├── apps/web/
├── ml/
│   ├── configs/
│   ├── notebooks/
│   ├── src/hoaxscope_ml/
│   └── tests/
├── data/{raw,interim,processed}/
├── artifacts/
├── docs/{diagrams,experiments}/
├── infra/
├── .github/workflows/
├── AGENTS.md
├── DEVELOPMENT.md
├── ARCHITECTURE.md
├── DATASET.md
├── MODEL_CARD.md
├── ROADMAP.md
└── README.md
```

Ini target konseptual. Inspeksi repository sebelum membuat folder atau
memindahkan file.

## 9. Keamanan dan operasional

-   Secret melalui environment/secret manager.
-   Validasi payload dan batasi ukuran batch.
-   Atur CORS sesuai environment.
-   Jangan simpan data sensitif yang tidak diperlukan.
-   Catat versi model pada setiap prediksi.
-   Health check dan logging tanpa secret/data sensitif.

## 10. Keputusan yang belum final

-   Dataset, lisensi, label taxonomy, dan cakupan waktu.
-   Penyimpanan teks lengkap atau metadata saja.
-   Split strategy setelah audit.
-   Definisi/kalibrasi score.
-   Apakah dashboard melayani input teks pengguna atau hanya data
    eksperimen.
-   Penyimpanan dan deployment artefak model.
