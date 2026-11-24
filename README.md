# HoaxScope

**Indonesian Misinformation & News Intelligence**

HoaxScope adalah proyek analisis pola misinformasi pada teks berita
berbahasa Indonesia menggunakan NLP dan machine learning. Hasil sistem
adalah **prediksi model berdasarkan pola pada dataset**, bukan verifikasi
fakta dan bukan bukti bahwa suatu klaim benar atau salah.

> **Status repository:** Phase 0 dan Phase 1 selesai. Stage 1 discovery,
> Stage 2 dataset selection/audit, dan Stage 3 canonical schema/data
> pipeline telah diselesaikan; dataset Mendeley 600-news tetap
> **CONDITIONALLY APPROVED**. Lihat
> [ADR 0003](docs/decisions/0003-dataset-selection.md) dan
> [laporan Stage 3](docs/experiments/stage-3-data-pipeline.md). Training
> Phase 2, model, API, dan dashboard belum diimplementasikan. Tidak ada
> file dataset, model, artifact, atau metrik evaluasi di repository; data
> mentah tetap dibaca dari lokasi sementara di luar repo.

## Responsible use

Gunakan istilah seperti `predicted_label`, `model_confidence`, dan
`dataset_label`. Jangan menampilkan klaim seperti "pasti hoaks" atau
"pasti benar" hanya berdasarkan prediksi model.

> Hasil ini merupakan prediksi model berdasarkan pola pada dataset dan
> bukan verifikasi fakta. Periksa sumber primer dan referensi
> pemeriksaan fakta sebelum mengambil keputusan.

## Dokumentasi

- [DEVELOPMENT.md](DEVELOPMENT.md) — spesifikasi teknis dan tahapan
  implementasi.
- [ARCHITECTURE.md](ARCHITECTURE.md) — rancangan arsitektur.
- [DATASET.md](DATASET.md) — register, audit, dan governance dataset.
- [ROADMAP.md](ROADMAP.md) — status dan acceptance criteria per fase.
- [AGENTS.md](AGENTS.md) — aturan kerja untuk coding agent.
- [docs/README.md](docs/README.md) — indeks dokumentasi dan decision
  record.

## Stack yang direncanakan

| Area | Teknologi |
| --- | --- |
| ML & data processing | Python 3.11+, Pandas, NumPy, scikit-learn |
| NLP lanjutan | Hugging Face Transformers, PyTorch, IndoBERT |
| API | FastAPI, Pydantic |
| Dashboard | Next.js, TypeScript, Tailwind CSS |
| Database | PostgreSQL |
| Testing | pytest, Vitest, Playwright |
| Delivery | Docker Compose, GitHub Actions |

Dependency belum dipasang dan belum dipin. Manifest dependency akan
dibuat pada fase yang membutuhkannya agar versi dapat dipilih dan diuji
secara nyata.

## Struktur repository

```text
hoaxscope/
├── apps/
│   ├── api/                 # FastAPI (Phase 5)
│   └── web/                 # Next.js dashboard (Phase 6)
├── ml/
│   ├── configs/
│   ├── data/                # raw/interim/processed, tidak di-commit
│   ├── notebooks/
│   ├── src/hoaxscope_ml/    # package pipeline ML
│   ├── scripts/
│   └── tests/
├── artifacts/               # model artifacts, tidak di-commit
├── docs/
│   ├── decisions/           # architecture decision records
│   ├── diagrams/
│   └── experiments/         # laporan eksperimen yang benar-benar dibuat
├── infra/
├── .github/workflows/
├── .env.example
├── .gitignore
├── README.md
└── dokumentasi proyek
```

Folder data kanonik adalah `ml/data/`, mengikuti `DEVELOPMENT.md` bagian
3.2. Keputusan dan perbedaan dengan `ARCHITECTURE.md` dicatat di
[docs/decisions/0001-phase-0-repository-foundation.md](docs/decisions/0001-phase-0-repository-foundation.md).

## Prasyarat

Diverifikasi pada environment inspeksi Phase 0:

- Python 3.11.9 (`py -3.11`)
- Node.js v25.2.1 dan npm 11.6.2
- Docker 29.9.2 (opsional untuk fase awal)
- Git 2.51.0
- `make` tidak tersedia pada environment tersebut; command build akan
  disediakan melalui mekanisme yang dapat dijalankan di Windows dan CI.

Versi final dependency dan Node.js akan dipin saat manifest dibuat.
Jangan mengasumsikan versi terbaru selalu kompatibel.

## Setup lokal saat ini

Belum ada dependency aplikasi yang perlu dipasang pada Phase 0.

```powershell
git clone <repository-url>
cd hoaxscope
Copy-Item .env.example .env
```

`.env` hanya berisi konfigurasi lokal dan tidak boleh di-commit. Nilai
`ACTIVE_MODEL` sengaja kosong karena belum ada artifact model.

## Status fase

| Phase | Status | Catatan |
| --- | --- | --- |
| 0 — Repository inspection & planning | Done | Struktur minimum, dokumentasi fondasi, dan rencana tersedia |
| 1 — Dataset audit & pipeline | Done | Stage 3 selesai: loader CP1252, canonical schema, validasi, dedup/konflik, preprocessing, group-aware split, 20 test lulus |
| 2 — Baseline NLP | Not started | Menunggu persetujuan pemilik untuk training dengan split Stage 3 |
| 3 — Advanced model & optimization | Not started | Menunggu baseline |
| 4 — Advanced content intelligence | Not started | Fitur opsional, tidak menghambat baseline |
| 5 — API & persistence | Not started | Menunggu artifact model |
| 6 — Dashboard | Not started | Harus memakai data API aktual |
| 7 — Integration & delivery | Not started | Docker/CI setelah komponen utama stabil |

Status terbaru dan acceptance criteria ada di [ROADMAP.md](ROADMAP.md).

## Langkah berikutnya

Stage 3 sudah selesai dan berhenti sebelum training. Pemilik perlu
menyetujui Phase 2 dengan dataset dan split yang telah dibekukan. Untuk
menjalankan ulang audit:

```powershell
python -m unittest discover -s ml/tests -v
python ml/scripts/run_stage3_pipeline.py --csv "<csv 600>" --workbook "<workbook 600>" --output-dir ml/data/processed
```

Jangan merge file 250 atau BRIN/Mafindo. Jangan mengarang nama kolom,
label, jumlah data, atau metrik.

## Keterbatasan

- Dataset 600-news sudah diaudit pada Stage 2, tetapi hanya berstatus
  conditionally approved; hak sumber berita pihak ketiga belum
  terverifikasi dan penggunaan komersial memerlukan review hukum.
- Label CSV tidak sepenuhnya identik dengan voting workbook; ada label
  konflik dan near-duplicate yang harus ditangani sebelum split.
- CSV tidak memiliki URL, sumber, topik, timestamp, atau ID record.
- File 250 praktis redundan dan tidak boleh digabungkan.
- Belum ada model, artifact, API, database, atau dashboard.
- Stage 3 sudah menyediakan preprocessing dan split group-aware, tetapi
  hasilnya belum diuji pada training/evaluasi model.
- Remote Git masih menunjuk ke repository lama; lihat decision record
  Phase 0 sebelum publikasi.
