# AGENTS.md --- HoaxScope

Instruksi untuk AI coding agents yang bekerja di repository HoaxScope.
Baca `DEVELOPMENT.md` sebelum perubahan besar.

## Konteks proyek

HoaxScope adalah Indonesian Misinformation & News Intelligence: pipeline
NLP, eksperimen klasifikasi, analisis topik/tren, REST API, dan
dashboard. Sistem bukan otoritas pemeriksa fakta. Prediksi dan
confidence score bukan bukti bahwa berita benar atau palsu.

## Aturan kerja

1.  Baca `DEVELOPMENT.md` dan dokumen relevan sebelum bekerja.
2.  Inspeksi repository, branch, konfigurasi, dan kode yang ada sebelum
    mengubah apa pun.
3.  Buat rencana untuk pekerjaan multi-file; kerjakan satu fase/unit
    pada satu waktu.
4.  Jangan membangun seluruh aplikasi sekaligus atau memperluas scope
    tanpa alasan.
5.  Setelah perubahan, jalankan test, lint, type-check, atau validasi
    relevan.
6.  Laporkan file berubah, keputusan teknis, perintah dan hasil test
    aktual, keterbatasan, serta langkah berikutnya.

## Standar engineering

-   Utamakan kode modular, sederhana, typed, mudah diuji, dan mudah
    dipelihara.
-   Pisahkan eksperimen ML, API, frontend, dan infrastruktur.
-   Hindari duplikasi preprocessing antara training dan inference.
-   Tangani error secara eksplisit; jangan bocorkan stack trace atau
    secret ke client.
-   Jangan mengubah kontrak API/skema database tanpa memperbarui
    dokumentasi dan test.
-   Jangan menambah dependency tanpa kebutuhan yang jelas.

## Aturan data dan ML

-   Jangan mengarang dataset, label, metrik, hasil eksperimen, atau
    sumber.
-   Periksa sumber, lisensi, provenance, schema, dan ketentuan
    penggunaan sebelum memakai dataset.
-   Audit missing values, duplikasi, label noise, class imbalance, dan
    data leakage.
-   Fit TF-IDF/vectorizer dan transformasi yang belajar dari data hanya
    pada training split.
-   Jangan gunakan test set untuk tuning atau pemilihan model.
-   Bandingkan model dengan split dan preprocessing yang konsisten.
-   Gunakan Macro F1 sebagai metrik utama awal; sertakan metrik per
    kelas, support, confusion matrix, dan accuracy.
-   Catat seed, konfigurasi, versi dataset/kode, dan hasil eksperimen.
-   Jangan commit data privat, secret, dataset besar, atau model weights
    besar tanpa alasan dan mekanisme yang sesuai.

## UX dan responsible AI

-   Gunakan istilah "prediksi model", "indikasi", dan "perlu verifikasi
    lanjutan".
-   Jangan tampilkan "pasti hoaks" atau "pasti benar".
-   Jelaskan keterbatasan model dan sumber data.
-   Jangan tampilkan tren jika timestamp/cakupan data tidak memadai.
-   Sediakan loading, empty, error, dan unavailable states.

## Keamanan

-   Secret hanya melalui environment/secret manager; `.env.example`
    berisi placeholder.
-   Validasi input di backend, batasi ukuran request batch, atur CORS
    sesuai environment.
-   Gunakan ORM/parameterized query.
-   Hindari menyimpan data sensitif yang tidak diperlukan dan jangan
    merekamnya di log.

## Definition of Done

Pekerjaan selesai jika implementasi memenuhi acceptance criteria, test
relevan benar-benar dijalankan, dokumentasi diperbarui, tidak ada
secret/data terlarang ter-commit, dan keterbatasan dilaporkan.

## Format laporan

-   Ringkasan implementasi
-   File baru/diubah/dihapus
-   Keputusan teknis
-   Test/lint/type-check dan hasil aktual
-   Keterbatasan atau asumsi
-   Langkah berikutnya
