# 0001 — Phase 0 Repository Foundation

- **Date:** 2026-11-13
- **Status:** Accepted for Phase 0
- **Scope:** repository inspection, planning, and minimum foundation only

## Context

Repository diperiksa pada branch `main` dengan commit terakhir
`9870a1f` (`Add initial DEVELOPMENT.md for project guidelines and
specifications`) dan `4af389d` (`first commit`).

Kondisi aktual saat inspeksi:

- Hanya tersedia dokumentasi; tidak ada source code, test, manifest
  dependency, Dockerfile, docker-compose, workflow CI, dataset, atau
  model artifact.
- `DEVELOPMENT.md` sudah di-track.
- `README.md` di-track tetapi berisi placeholder UTF-16LE
  `# is-this-real-chat-`, bukan dokumentasi proyek.
- `AGENTS.md`, `ARCHITECTURE.md`, `DATASET.md`, dan `ROADMAP.md` belum
  di-track saat inspeksi.
- Remote `origin` masih menunjuk ke
  `https://github.com/RfndUsdan/is-this-real-chat-.git`, yaitu repository
  lama. Remote tidak diubah pada fase ini.
- Tidak ada file penting yang dihapus.

Environment inspeksi:

| Tool | Versi |
| --- | --- |
| Python | 3.11.9 (default), 3.14.0 melalui `py` |
| pip | 26.1.2 untuk Python 3.11 |
| Node.js | v25.2.1 |
| npm | 11.6.2 |
| Docker | 29.9.2 |
| Git | 2.51.0.windows.2 |
| make | Tidak tersedia |

## Decisions

### D1 — Monorepo mengikuti `DEVELOPMENT.md` bagian 3.2

Struktur minimum yang dibuat:

- `apps/api/` untuk FastAPI.
- `apps/web/` untuk Next.js.
- `ml/` untuk pipeline data dan eksperimen.
- `artifacts/` untuk model artifact (isi tidak di-commit).
- `docs/` untuk decision record dan dokumen pendukung.
- `infra/` dan `.github/workflows/` untuk fase delivery.

Tidak dibuat stub `main.py`, `package.json`, atau konfigurasi yang
seolah-olah aplikasi sudah berjalan. Folder kosong diberi `.gitkeep`
agar struktur dapat di-commit.

### D2 — Data root kanonik adalah `ml/data/`

`DEVELOPMENT.md` bagian 3.2 menempatkan data di `ml/data/`, sedangkan
`ARCHITECTURE.md` bagian 8 menampilkan `data/` di root. Dipilih
`ml/data/{raw,interim,processed}` karena `DEVELOPMENT.md` adalah sumber
spesifikasi utama dan data berada dekat pipeline ML.

Konsekuensi:

- `.gitignore` mengabaikan isi `ml/data/*` tetapi mempertahankan
  `.gitkeep` dan `ml/data/README.md`.
- Folder `data/` di root tidak dibuat.
- Jika kebutuhan deployment nanti menuntut lokasi lain, keputusan harus
  diperbarui bersama dokumentasi dan konfigurasi `DATA_DIR`.

### D3 — Dokumen root menjadi sumber kanonik

`DEVELOPMENT.md` bagian 3.2 dan 17 menyebut `docs/architecture.md`,
`docs/dataset.md`, dan dokumen lain. Repository sudah memiliki
`ARCHITECTURE.md` dan `DATASET.md` di root, dan `ARCHITECTURE.md` sendiri
menargetkan dokumen root.

Keputusan:

- Dokumen root tetap kanonik agar tidak ada dua versi yang berbeda.
- `docs/README.md` menjadi indeks yang menautkan dokumen root.
- `docs/decisions/` menyimpan ADR; `docs/diagrams/` dan
  `docs/experiments/` disiapkan untuk output nyata.
- Tidak dibuat salinan `docs/architecture.md` atau `docs/dataset.md`
  pada fase ini. Jika nanti diperlukan path tersebut, gunakan pointer
  singkat ke dokumen kanonik, bukan duplikasi isi.

Lokasi final model card (root `MODEL_CARD.md` vs
`docs/model-card.md`) belum diputuskan; akan diselesaikan pada Phase 7
saat model benar-benar ada.

### D4 — Tooling dibuat pada fase yang membutuhkan

Belum dibuat `pyproject.toml`, `package.json`, `Makefile`, Dockerfile,
docker-compose, atau workflow CI. Alasannya:

- Belum ada kode atau dependency nyata untuk dipin dan diuji.
- Menulis manifest sekarang berisiko mengunci versi tanpa validasi.
- `make` tidak tersedia di environment inspeksi, sehingga command
  cross-platform perlu dirancang, bukan diasumsikan.

Rencana:

- Phase 1/2: `ml/pyproject.toml`, konfigurasi lint/type-check/test, dan
  command pipeline.
- Phase 5: dependency API dan database.
- Phase 6: dependency frontend dan lockfile.
- Phase 7: Docker Compose, CI, dan command delivery.

`DEVELOPMENT.md` bagian 3.3 tetap menjadi target; command belum
diklaim tersedia.

### D5 — `.env.example` tidak menyatakan model tersedia

`ACTIVE_MODEL` dibiarkan kosong karena belum ada artifact. Ini berbeda
dari contoh `baseline-svm` di `DEVELOPMENT.md` bagian 14, tetapi
mencegah API atau developer menganggap model tersebut sudah ada. API
nanti harus melaporkan model tidak tersedia, bukan mengganti diam-diam
dengan model lain.

`DATABASE_URL` memakai kredensial placeholder lokal (`change-me`) dan
tidak boleh dipakai di production. Tidak ada secret nyata di template.

### D6 — Placeholder `README.md` diganti

`README.md` lama hanya berisi `# is-this-real-chat-` dan tidak memuat
informasi proyek. File diganti dengan README HoaxScope yang menyatakan
status Phase 0 secara jujur, dokumentasi, stack rencana, setup minimum,
dan keterbatasan.

### D7 — Tidak ada dataset yang diunduh atau dibuat

Tidak ada dataset, angka distribusi, label aktual, atau metrik yang
dibuat pada fase ini. Kandidat dataset di `DATASET.md` belum
diverifikasi lisensi, schema, atau provenance. Audit dilakukan pada
Phase 1 sebelum download.

### D8 — Remote Git lama tidak diubah

Remote `origin` masih mengarah ke repository lama. Perubahan remote
adalah keputusan pemilik repository dan berisiko terhadap publikasi,
sehingga tidak dilakukan otomatis. Langkah yang disarankan: verifikasi
tujuan repository, lalu perbarui remote sebelum push hasil Phase 0.

## Consistency findings

| # | Temuan | Sumber | Status |
| --- | --- | --- | --- |
| 1 | Lokasi data `ml/data` vs `data/` di root | DEVELOPMENT 3.2 vs ARCHITECTURE 8 | Diputuskan: `ml/data` (D2) |
| 2 | Dokumen teknis di root vs `docs/*.md` | DEVELOPMENT 3.2/17 vs ARCHITECTURE 8 dan file aktual | Diputuskan: root kanonik (D3); lokasi model card menyusul |
| 3 | Payload prediksi `title` + `content` + `model_name` vs `text` + `model_version` | DEVELOPMENT 9.3 vs ARCHITECTURE 6 | Belum final; putuskan sebelum kontrak API Phase 5 |
| 4 | Bentuk response prediksi `data/scores/status` vs `prediction/model/notice` | DEVELOPMENT 9.4 vs ARCHITECTURE 6 | Belum final; samakan dengan kontrak OpenAPI dan schema test |
| 5 | Arti `score`: probability, decision score, atau confidence terkalibrasi | ARCHITECTURE 6 | Belum final; jangan menyebut confidence tanpa kalibrasi |
| 6 | Endpoint `/api/v1/*` | DEVELOPMENT 9.1 vs ARCHITECTURE 6 | Konsisten secara prefix; tidak ada konflik |
| 7 | Urutan fase 0–7 | DEVELOPMENT 15 vs ROADMAP | Selaras; perbedaan hanya judul/penekanan |
| 8 | Label mapping biner `misleading_or_false` / `not_flagged_as_hoax` | DEVELOPMENT 4.4 vs DATASET 4 | Contoh, bukan label final; wajib audit Phase 1 |
| 9 | Model baseline menyebut Linear SVM vs LinearSVC | DEVELOPMENT 6.1 vs ARCHITECTURE 5 dan ROADMAP | Tidak konflik; `LinearSVC` adalah implementasi yang direncanakan |
| 10 | Python 3.11+ vs Python 3.14 tersedia | DEVELOPMENT 3.1 vs environment | Targetkan Python 3.11.x; pin saat manifest dibuat |
| 11 | Node.js v25.2.1 tersedia | Environment | Belum tentu kompatibel dengan Next.js; pin versi LTS pada Phase 6 |
| 12 | Command `make` diwajibkan/diilustrasikan | DEVELOPMENT 3.3 | `make` tidak tersedia; sediakan command cross-platform dan dokumentasikan |
| 13 | Remote dan README masih memakai nama proyek lama | Git remote dan README lama | README diperbaiki; remote menunggu keputusan pemilik (D8) |

## Assumptions

- Proyek masih greenfield; dokumentasi adalah sumber requirement utama.
- Python 3.11.x adalah runtime ML awal sampai ada alasan kompatibilitas
  untuk naik versi.
- PostgreSQL dan Redis belum dijalankan; Redis tetap opsional.
- API, database schema, dan UI belum dikontrakkan secara final.
- Data akan diperoleh dari sumber yang lisensinya diverifikasi pada
  Phase 1, bukan dari scraping otomatis.

## Out of scope

Phase 0 tidak mencakup:

- download atau pembuatan dataset;
- adapter, schema validation, EDA, atau split;
- preprocessing dan training;
- model artifact;
- endpoint API dan database;
- dashboard;
- Docker dan CI yang aktif.

## Validation

Validasi yang dijalankan pada Phase 0:

1. `git status --short` dan pemeriksaan struktur folder aktual.
2. `git check-ignore --no-index <path>` untuk memastikan `.env`, data,
   artifact, dependency, cache, dan build output diabaikan.
3. Pemeriksaan bahwa `.env.example`, `.gitkeep`, dan
   `ml/data/README.md` tidak diabaikan.
4. Pemeriksaan link relatif pada README dan dokumen pendukung.
5. Pemeriksaan tidak ada secret nyata atau file dataset/model yang
   tidak sengaja ditambahkan.

Belum ada test aplikasi yang dapat dijalankan karena belum ada kode.
Hasil perintah aktual dilaporkan pada laporan Phase 0; jangan mengklaim
Phase 1–7 berjalan.

Hasil aktual pada 2026-11-13:

- 12 path uji untuk secret/data/artifact/dependency/cache/build output
  semuanya cocok dengan pola `.gitignore`.
- 6 path yang harus tetap tracked (`.env.example`, empat `.gitkeep` data
  dan artifact, serta `ml/data/README.md`) semuanya tidak diabaikan.
- 17 link relatif diperiksa (README, ROADMAP, docs index, decision
  record, dan ml/data/README); 0 broken.
- 0 temuan untuk pola secret yang diuji.
- `ml/data/` dan `artifacts/` hanya berisi `.gitkeep` serta README; tidak
  ada dataset atau model artifact.
- Tidak ada file source, manifest dependency, atau test aplikasi pada
  Phase 0.

## Implementation plan (Phase 1–7)

Rencana ini bergantung pada hasil audit, bukan pada asumsi bahwa semua
dataset atau dependency tersedia.

| Phase | Pekerjaan utama | Dependency/exit criteria |
| --- | --- | --- |
| 1 — Dataset audit & pipeline | Verifikasi lisensi/provenance/schema/label; buat loader, canonical schema, adapter untuk dataset yang benar-benar ada, validation, dedup report, EDA, dan split strategy | Tidak ada data masuk sebelum audit; laporan kualitas dan test loader tersedia |
| 2 — Baseline NLP | `ml/pyproject.toml`; preprocessing reusable; TF-IDF fit hanya pada train; MultinomialNB, Logistic Regression, LinearSVC; metrik Macro F1 dan per kelas; simpan config/metadata | Phase 1 selesai; split dan label mapping tervalidasi; hasil reproducible |
| 3 — Advanced model | Periksa model card/lisensi IndoBERT; fine-tuning dengan validation set; kalibrasi dan biaya komputasi; bandingkan pada test set yang sama | Baseline stabil; resource dicatat; test set tidak dipakai untuk tuning |
| 4 — Content intelligence | Similarity, topic modeling, explainability, temporal analysis hanya jika data mendukung; evaluasi dan dokumentasi limitasi | Output dapat ditelusuri ke model/data version; fitur opsional tidak memblokir baseline |
| 5 — API & persistence | Selesaikan kontrak request/response; FastAPI + Pydantic; model registry; prediction service; PostgreSQL; validasi dan API tests | Ada artifact nyata; model tidak tersedia ditangani eksplisit; error schema konsisten |
| 6 — Dashboard | Next.js + TypeScript + Tailwind; Overview, Analyzer, Benchmark; integrasi API; loading/empty/error/unavailable states; disclaimer | API stabil; data aktual, bukan mock tanpa label; test komponen utama |
| 7 — Integration & delivery | Docker/Compose, health checks, CI lint/test/build, README akhir, model card, audit secret dan file besar | Clean setup diuji; CI berjalan; dokumentasi sesuai implementasi |

Prinsip eksekusi: satu fase per perubahan, jangan memasang seluruh stack
sekaligus, dan jangan memulai training sebelum dataset serta split
tervalidasi.

## Next action

Phase 1 — Dataset audit & pipeline:

1. Verifikasi dataset card, lisensi, provenance, schema, dan definisi
   label untuk kandidat di `DATASET.md`.
2. Buat canonical schema dan adapter hanya untuk dataset yang benar-benar
   tersedia.
3. Buat validasi data, laporan duplikasi, dan audit kualitas.
4. Tentukan split strategy yang mencegah duplicate/group leakage.
5. Tambahkan unit test dengan fixture sintetis berlabel jelas.
6. Dokumentasikan hasil audit nyata, bukan placeholder.
