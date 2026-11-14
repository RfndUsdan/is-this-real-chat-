# HoaxScope

**Indonesian Misinformation & News Intelligence**

HoaxScope adalah proyek analisis pola misinformasi pada teks berita
berbahasa Indonesia menggunakan NLP dan machine learning. Hasil sistem
adalah **prediksi model berdasarkan pola pada dataset**, bukan verifikasi
fakta dan bukan bukti bahwa suatu klaim benar atau salah.

> **Status repository:** Phase 0 (repository inspection & planning)
> selesai. Phase 1 Stage 1 (dataset discovery/audit) selesai; dataset
> belum disetujui. Lihat
> [ADR 0002](docs/decisions/0002-phase-1-stage-1-dataset-discovery.md).
> Pipeline data, model, API, dan dashboard **belum diimplementasikan**.
> Tidak ada file dataset, model, artifact, atau metrik evaluasi yang
> tersedia atau diklaim.

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
- [DATASET.md](DATASET.md) — kebijakan dan template audit dataset.
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
| 1 — Dataset audit & pipeline | In progress (Stage 1) | Audit metadata/lisensi selesai; file dataset belum diakses; dataset belum disetujui |
| 2 — Baseline NLP | Not started | Menunggu dataset dan split yang tervalidasi |
| 3 — Advanced model & optimization | Not started | Menunggu baseline |
| 4 — Advanced content intelligence | Not started | Fitur opsional, tidak menghambat baseline |
| 5 — API & persistence | Not started | Menunggu artifact model |
| 6 — Dashboard | Not started | Harus memakai data API aktual |
| 7 — Integration & delivery | Not started | Docker/CI setelah komponen utama stabil |

Status terbaru dan acceptance criteria ada di [ROADMAP.md](ROADMAP.md).

## Langkah berikutnya

Phase 1: putuskan dataset kandidat utama dan ajukan akses file. Stage 1
sudah mengaudit metadata, lisensi, provenance, dan dokumentasi label;
file aktual, deduplikasi, distribusi kelas, dan split belum diverifikasi.
Jangan mengarang nama kolom, label, jumlah data, atau metrik.

## Keterbatasan

- Metadata dataset sudah diaudit pada Stage 1; file dataset belum
  diunduh atau diverifikasi.
- Belum ada dataset yang disetujui untuk pipeline.
- Belum ada model, artifact, atau hasil evaluasi.
- Belum ada API, database, atau dashboard.
- Label taxonomy dan split strategy belum final.
- Remote Git masih menunjuk ke repository lama; lihat decision record
  Phase 0 sebelum publikasi.
