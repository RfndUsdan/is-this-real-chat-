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

Belum ada file dataset yang disalin ke folder ini. Audit Stage 2 memakai
salinan sementara di luar repository; tidak ada CSV/XLSX yang di-commit.
Dataset Mendeley 600-news berstatus **conditionally approved**; hasil
audit dan kondisinya ada di
[`docs/decisions/0003-dataset-selection.md`](../../docs/decisions/0003-dataset-selection.md).
Stage 3 (loader, schema validation, preprocessing, split) belum dimulai.
Folder ini hanya berisi penanda `.gitkeep`.

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

## Langkah berikutnya

Stage 3 belum dimulai. Setelah pemilik menerima kondisi ADR 0003, baru
dibuat loader, schema validation, pemetaan record, group-aware split,
serta preprocessing dan test. Jangan mulai training sebelum split dan
leakage test tersedia.
