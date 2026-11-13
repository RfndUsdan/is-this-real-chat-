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

Belum ada dataset yang diunduh, disalin, atau diaudit. Folder hanya
berisi penanda `.gitkeep`.

## Aturan

1. Jangan mengunduh dataset sebelum memeriksa dataset card, lisensi,
   provenance, schema aktual, dan ketentuan penggunaan.
2. Jangan meng-commit raw data, data berukuran besar, data pribadi, atau
   data yang lisensinya tidak mengizinkan redistribusi.
3. Jangan mengarang nama kolom, label, jumlah record, atau statistik.
4. Catat sumber, tanggal akses, versi, lisensi, dan transformasi di
   `DATASET.md` setelah audit nyata.
5. Pertahankan pemisahan `raw`, `interim`, dan `processed`.
6. Buat fixture sintetis kecil dan berlabel jelas untuk unit test; jangan
   memakai data privat.

## Kandidat sumber

Kandidat sumber dan hal yang harus diperiksa tercantum di
[`DATASET.md`](../../DATASET.md). Daftar tersebut belum merupakan
konfirmasi lisensi atau persetujuan penggunaan.

## Langkah berikutnya

Phase 1 akan memverifikasi sumber, membuat loader dan schema validation,
menjalankan audit kualitas data, serta mencatat split strategy dan
provenance sebelum training dimulai.
