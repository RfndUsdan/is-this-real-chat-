# Dataset Directory

Folder ini adalah lokasi data kanonik untuk pipeline ML, mengikuti
`DEVELOPMENT.md` bagian 3.2.

```text
ml/data/
├── raw/          # file sumber asli, tidak di-commit
├── interim/      # hasil transformasi sementara, tidak di-commit
└── processed/    # data siap training/evaluasi, tidak di-commit
```

## Status

Tidak ada CSV/XLSX yang disalin atau di-commit ke folder ini. Dataset
dibaca dari lokasi sementara di luar repository; teks mentah hanya ada
dalam memori proses dan penyimpanan lokal yang diabaikan Git.

Stage 3 selesai pada 2026-11-24. Pipeline menulis laporan JSON yang sudah
tanpa raw text/URL ke `ml/data/processed/` (diabaikan Git):

```text
stage3-validation.json
stage3-workbook-audit.json
stage3-dedup.json
stage3-quarantine.json
stage3-split.json
stage3-preprocessing.json
stage3-summary.json
```

Hasil dan keterbatasannya ada di
[`docs/experiments/stage-3-data-pipeline.md`](../../docs/experiments/stage-3-data-pipeline.md).
Kondisi dataset tetap mengikuti
[`docs/decisions/0003-dataset-selection.md`](../../docs/decisions/0003-dataset-selection.md).
Folder sumber tetap hanya berisi penanda `.gitkeep`.

## Aturan

1. Jangan menyalin dataset ke repository sebelum kondisi ADR 0003
   diterima dan mekanisme penyimpanan lokal disepakati.
2. Jangan meng-commit raw data, data berukuran besar, data pribadi, atau
   data yang lisensinya tidak mengizinkan redistribusi.
3. Jangan mengarang nama kolom, label, jumlah record, atau statistik.
4. Catat sumber, tanggal akses, versi, lisensi, hash, dan transformasi di
   `DATASET.md` setelah audit nyata.
5. Pertahankan pemisahan `raw`, `interim`, dan `processed`.
6. Buat fixture sintetis kecil dan berlabel jelas untuk unit test; jangan
   memakai data privat.
7. Jangan memakai file 250 atau menggabungkannya dengan dataset 600.

## Kandidat sumber

Dataset MVP adalah Mendeley `p3hfgr5j3m` versi 1, hanya CSV 600. Audit
lengkap ada di [ADR 0003](../../docs/decisions/0003-dataset-selection.md).
Kandidat Stage 1 dan rekomendasi lama ada di
[ADR 0002](../../docs/decisions/0002-phase-1-stage-1-dataset-discovery.md);
rekomendasi BRIN di ADR 0002 digantikan untuk pemilihan sumber MVP.
[`DATASET.md`](../../DATASET.md) adalah register kanonik.

## Menjalankan pipeline

```powershell
python ml/scripts/run_stage3_pipeline.py `
  --csv "<path ke 600 news with valid hoax label.csv>" `
  --workbook "<path ke 600 news labelling process.xlsx>" `
  --output-dir ml/data/processed
```

Unit test memakai fixture sintetis dan tidak memerlukan dataset asli:

```powershell
python -m unittest discover -s ml/tests -v
```

## Langkah berikutnya

Stage 3 sudah selesai. Training Phase 2 belum boleh dimulai tanpa
persetujuan pemilik. Jika disetujui, gunakan split dan daftar karantina
dari laporan Stage 3, bukan split acuan dari file 250.
