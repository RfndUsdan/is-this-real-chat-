# Documentation Index

Dokumentasi tingkat proyek berada di root repository dan menjadi sumber
kanonik:

| Dokumen | Isi |
| --- | --- |
| [../DEVELOPMENT.md](../DEVELOPMENT.md) | Spesifikasi teknis utama dan tahapan implementasi |
| [../ARCHITECTURE.md](../ARCHITECTURE.md) | Rancangan arsitektur dan alur data |
| [../DATASET.md](../DATASET.md) | Register dataset, audit kualitas, dan governance |
| [../ROADMAP.md](../ROADMAP.md) | Status fase dan acceptance criteria |
| [../AGENTS.md](../AGENTS.md) | Aturan kerja untuk coding agent |
| [../README.md](../README.md) | Gambaran proyek, setup, dan status |

Folder ini menyimpan dokumen pendukung:

- `decisions/` — architecture decision records (ADR).
- `diagrams/` — diagram yang dibuat kemudian.
- `experiments/` — laporan eksperimen yang benar-benar dijalankan.

Jangan menyalin isi dokumen root ke sini tanpa alasan. Jika sebuah
dokumen perlu dipecah, buat satu sumber kanonik dan tautkan dari tempat
lain. Keputusan tentang lokasi dokumentasi dicatat di
[decisions/0001-phase-0-repository-foundation.md](decisions/0001-phase-0-repository-foundation.md).

Decision records:

- Phase 1 Stage 1:
  [decisions/0002-phase-1-stage-1-dataset-discovery.md](decisions/0002-phase-1-stage-1-dataset-discovery.md).
- Phase 1 Stage 2 (dataset selection/audit, conditional approval):
  [decisions/0003-dataset-selection.md](decisions/0003-dataset-selection.md).

ADR 0002 tetap menjadi catatan sejarah Stage 1. Rekomendasi BRIN di
dalamnya digantikan untuk pemilihan sumber MVP oleh ADR 0003; isi ADR
0002 tidak dihapus.
