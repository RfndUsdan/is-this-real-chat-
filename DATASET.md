# HoaxScope --- Dataset Documentation

> Isi dokumen ini berdasarkan audit nyata. Jangan mengarang jumlah data,
> distribusi label, lisensi, atau kualitas dataset.

## 1. Tujuan

Mencatat sumber, lisensi, schema, label, kualitas, preprocessing, split,
dan batasan dataset HoaxScope. Label dari sumber tidak otomatis bebas
kesalahan atau mewakili seluruh berita Indonesia.

## 2. Kandidat sumber untuk ditinjau

  ------------------------------------------------------------------------------------------------------------------------
  Dataset/sumber          URL                                                                      Yang harus diperiksa
  ----------------------- ------------------------------------------------------------------------ -----------------------
  BRIN Fake News Mafindo  https://huggingface.co/datasets/nlp-brin-id/fakenews-mafindo             Dataset card, schema,
                                                                                                   label, lisensi,
                                                                                                   provenance

  BRIN id-hoax-report     https://huggingface.co/datasets/nlp-brin-id/id-hoax-report               Apakah unit data berupa
                                                                                                   laporan, klaim, atau
                                                                                                   artikel; definisi label

  Open Data Fact Checking https://data.go.id/dataset/dataset/data-pengecekan-fakta-fact-checking   Metadata, format,
                                                                                                   lisensi, cakupan
  ------------------------------------------------------------------------------------------------------------------------

Daftar ini hanya kandidat, bukan konfirmasi bahwa dataset telah
disetujui atau digabungkan. Periksa halaman sumber dan file aktual
sebelum penggunaan.

## 3. Register dataset

Isi satu register untuk setiap dataset yang benar-benar digunakan.

### Dataset: \[nama resmi\]

  Atribut                  Nilai
  ------------------------ ----------------------------------
  Nama resmi               \[isi\]
  URL sumber               \[isi\]
  Organisasi/pembuat       \[isi\]
  Tanggal akses            \[YYYY-MM-DD\]
  Versi/release/commit     \[jika tersedia\]
  Lisensi                  \[salin ketentuan yang berlaku\]
  Format dan ukuran        \[isi\]
  Jumlah record awal       \[hasil audit\]
  Bahasa                   \[isi\]
  Rentang tanggal konten   \[jika tersedia\]
  Atribusi wajib           \[isi\]
  Catatan penggunaan       \[isi\]

## 4. Schema dan label

Catat nama kolom aktual; jangan mengasumsikan seluruh dataset memakai
schema sama.

  ------------------------------------------------------------------------------------
  Kolom asli     Tipe              Wajib?         Arti                Transformasi
  -------------- ----------------- -------------- ------------------- ----------------
  \[kolom teks\] string            Ya             Teks artikel/klaim  \[aturan\]

  \[kolom        string            Ya             Label sumber        Mapping
  label\]                                                             terdokumentasi

  \[kolom        datetime/string   Tidak          Tanggal             Parse/validasi
  tanggal\]                                       publikasi/laporan   

  \[kolom        string            Tidak          Sumber/publisher    Normalisasi
  sumber\]                                                            konservatif
  ------------------------------------------------------------------------------------

### Label taxonomy

  Label asli   Definisi dari sumber   Label internal   Catatan
  ------------ ---------------------- ---------------- -------------
  \[label\]    \[definisi\]           \[mapping\]      \[catatan\]

Jangan menyatukan label berbeda hanya karena namanya mirip. Jika
definisinya tidak sepadan, pisahkan eksperimen atau jelaskan mapping dan
risikonya.

## 5. Data quality audit

Laporkan hasil aktual: - total record sebelum/sesudah validasi; -
missing values per kolom; - teks kosong/terlalu pendek; - exact dan
near-duplicate; - distribusi label dan persentase kelas; - distribusi
panjang teks; - timestamp tidak valid; - label tidak dikenal; - potensi
kebocoran antar split.

  Pemeriksaan           Hasil aktual   Tindakan
  --------------------- -------------- ----------
  Total record          \[isi\]        \[isi\]
  Tanpa teks            \[isi\]        \[isi\]
  Tanpa label           \[isi\]        \[isi\]
  Exact duplicate       \[isi\]        \[isi\]
  Near duplicate        \[isi\]        \[isi\]
  Label tidak dikenal   \[isi\]        \[isi\]
  Timestamp invalid     \[isi\]        \[isi\]

## 6. Preprocessing policy

Langkah yang dapat dievaluasi: - normalisasi Unicode dan whitespace; -
penanganan null/teks kosong; - normalisasi URL/mention bila relevan; -
deduplikasi; - tokenisasi sesuai model; - stopword removal hanya setelah
diuji; - stemming hanya jika terbukti membantu dan konsisten.

Jangan menghapus negasi, angka, tanda baca, atau kata tertentu secara
membabi buta. Simpan teks asli dan hasil preprocessing terpisah jika
lisensi dan kebijakan retensi mengizinkan.

## 7. Split dan leakage

Catat proporsi split, seed, stratification, grouping berdasarkan
sumber/klaim/duplikasi, dan temporal split bila relevan. Fit vectorizer
dan transformasi yang mempelajari statistik hanya pada training data.
Jangan gunakan test set untuk tuning. Hindari salinan artikel yang sama
berada di split berbeda.

## 8. Bias dan keterbatasan

Evaluasi class imbalance, bias sumber/platform, bias topik/periode,
perubahan gaya bahasa, label noise, standar pelabelan yang berbeda,
representasi ragam bahasa, dan distribution shift. Jelaskan dampaknya
terhadap generalisasi. Jangan mengklaim model mendeteksi seluruh hoaks
di internet.

## 9. Data governance

-   Patuhi lisensi dan ketentuan sumber.
-   Catat URL, versi, tanggal akses, dan atribusi.
-   Jangan mempublikasikan ulang data jika lisensi tidak mengizinkan.
-   Jangan masukkan data pribadi/sensitif ke dashboard atau log tanpa
    kebutuhan dan dasar yang jelas.
-   Jangan commit dataset besar; gunakan penyimpanan yang sesuai.
-   Pisahkan data raw, interim, dan processed.
-   Tetapkan akses dan retensi data.

## 10. Template catatan versi dataset

``` text
Dataset version:
Source(s):
Access date:
License:
Raw records:
Records after validation:
Label mapping:
Duplicate handling:
Preprocessing version:
Split strategy:
Random seed:
Known limitations:
Prepared by:
```

## 11. Checklist sebelum digunakan

-   [ ] Sumber dan pembuat teridentifikasi.
-   [ ] Lisensi dan ketentuan penggunaan diperiksa.
-   [ ] Dataset card/metadata dibaca.
-   [ ] Schema aktual diverifikasi.
-   [ ] Definisi label dipahami.
-   [ ] Data quality audit dijalankan.
-   [ ] Duplikasi dan leakage diperiksa.
-   [ ] Split strategy ditetapkan.
-   [ ] Provenance dan versi dicatat.
-   [ ] Bias dan keterbatasan didokumentasikan.
