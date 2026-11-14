# 0002 — Phase 1 Stage 1 Dataset Discovery & Audit

- **Date:** 2026-11-14
- **Status:** Stage 1 complete; dataset decision pending approval
- **Scope:** discovery and source audit only. No dataset file was downloaded,
  merged, or used for training. No pipeline, API, or dashboard was built.

## 1. Context and constraints

Phase 1 membutuhkan dataset yang sumber, lisensi, provenance, schema, label,
dan batas penggunaannya dapat dipertanggungjawabkan. Stage 1 hanya menjawab
pertanyaan:

1. Sumber resmi setiap kandidat ada di mana dan versi mana yang berlaku?
2. Lisensi dan ketentuan penggunaan apa yang benar-benar tercatat?
3. Apakah schema, label, split, dan provenance dapat diverifikasi?
4. Dataset mana yang paling sesuai untuk MVP, dan apa syaratnya?

Batasan yang dipakai:

- Tidak mengunduh atau menggabungkan dataset sebelum ketentuan penggunaan
  dinilai.
- Tidak mengarang jumlah record, distribusi label, metrik, atau hasil EDA.
- Tidak menganggap label yang mirip memiliki arti yang sama.
- Tidak menggunakan test set untuk preprocessing, tuning, atau pemilihan model.
- Tidak melanjutkan ke pipeline sebelum ada keputusan dataset.

Repository berada di branch `main`, working tree bersih pada awal audit. Tidak
ada dataset, model artifact, atau metrik di repository. Root repository juga
belum memiliki file `LICENSE`; status komersial/non-komersial proyek belum
dinyatakan eksplisit.

> Catatan: `DEVELOPMENT.md` menyebut BRIN Fake News Mafindo sebagai dataset
> utama untuk starting point. Audit ini tidak otomatis mengikuti pilihan itu.
> Rekomendasi di bawah didasarkan pada bukti sumber dan lisensi yang ditemukan.

## 2. Metode audit

Audit dilakukan pada 2026-11-14 dengan:

- membaca `DATASET.md`, `DEVELOPMENT.md`, `ROADMAP.md`, `ARCHITECTURE.md`,
  `README.md`, `docs/README.md`, dan `ml/data/README.md`;
- membaca halaman dataset, dataset card, metadata API, dan file tree publik;
- membaca syarat layanan sumber hulu;
- memeriksa respons HTTP untuk URL sumber dan resource;
- tidak mengunduh file dataset, termasuk file sampel.

Sumber yang diperiksa:

- BRIN Dataverse:
  <https://data.brin.go.id/dataset.xhtml?persistentId=hdl:20.500.12690/RIN/7QBRKQ>
- Hugging Face `nlp-brin-id/fakenews-mafindo`:
  <https://huggingface.co/datasets/nlp-brin-id/fakenews-mafindo>
- Hugging Face `nlp-brin-id/id-hoax-report`:
  <https://huggingface.co/datasets/nlp-brin-id/id-hoax-report>
- `data.go.id`:
  <https://data.go.id/dataset/dataset/data-pengecekan-fakta-fact-checking>
- Open Data Jabar:
  <https://opendata.jabarprov.go.id/id/dataset/data-pengecekan-fakta-fact-checking>
- Ketentuan Open Data Jabar:
  <https://opendata.jabarprov.go.id/id/ketentuan-penggunaan>
- Jabar Saber Hoaks:
  <https://saberhoaks.jabarprov.go.id/v2/home>
- Klinik Hoaks Jatim:
  <https://klinikhoaks.jatimprov.go.id/>
- Mafindo/TurnBackHoax terms:
  <https://mafindo.or.id/terms-of-use/> dan
  <https://turnbackhoax.id/ketentuan-layanan>

## 3. Ringkasan keputusan

| Kandidat | Status Stage 1 | Alasan ringkas |
| --- | --- | --- |
| BRIN Dataverse v2.1, `hdl:20.500.12690/RIN/7QBRKQ` | **Kandidat utama, kondisional** | Rilis resmi terbaru yang dirujuk kedua card HF, lisensi CC BY-NC 4.0 eksplisit, 6.241 train + 506 test, tetapi file restricted dan schema/label aktual belum terverifikasi |
| HF `nlp-brin-id/fakenews-mafindo` | **Fallback saja** | Gated, tidak dipelihara, beta dan imbalanced, tag MIT tidak konsisten dengan rilis CC BY-NC 4.0 dan ketentuan Mafindo; schema lebih mudah dibaca setelah akses |
| HF `nlp-brin-id/id-hoax-report` | **Eksploratif saja** | Tiga sumber dengan label heterogen, tanpa split resmi, pemetaan label Klinik Hoaks tidak terdokumentasi, ketentuan sumber hulu tidak mendukung redistribusi |
| `data.go.id` Jabar fact-checking | **Tidak disetujui** | Metadata `isopen:false`, `private:true`, `review_status:rejected`, `license_title:null`, catatan `broken_link`/`not_complete`; CSV tidak dapat diverifikasi |
| Turunan HF `id-hoax-report-merge*` dan `unsup-content` | **Belum diaudit / bukan kandidat** | Gated, tidak dipelihara, dan mewarisi isu provenance/label dari sumber asal |

**Tidak ada dataset yang disetujui untuk implementasi pipeline pada Stage 1.**
Keputusan akhir membutuhkan persetujuan pengguna dan akses file aktual.

## 4. Temuan per sumber

### 4.1 BRIN Dataverse v2.1

#### Identitas dan akses

| Atribut | Nilai |
| --- | --- |
| Judul | Dataset Berita Palsu Bahasa Indonesia Dengan Penelusuran Fakta Berbasis LLM |
| Persistent identifier | `hdl:20.500.12690/RIN/7QBRKQ` |
| URL | <https://data.brin.go.id/dataset.xhtml?persistentId=hdl:20.500.12690/RIN/7QBRKQ> |
| Repository | RIN Dataverse (BRIN) |
| Penulis | Wijayanti, Rini; Ni'mah, Iftitahu; Santosa, Agung; Jarin, Asril; Uliniansyah, Mohammad Teduh; Yuyun; Khotimah, Purnomo Husnul; Xu, Ke |
| Publikasi | 2024-10-16 |
| Versi terbaru | 2.1, dirilis 2026-07-22 |
| Versi sebelumnya | 2.0 (2026-07-03), 1.1 (2025-09-24), 1.0 (2024-10-15) |
| Lisensi | CC BY-NC 4.0 (dinyatakan di terms of use) |
| Akses file | Restricted; file access request diaktifkan |

#### File yang terdaftar

Angka variabel dan observasi di bawah berasal dari metadata Dataverse, bukan
hasil pembacaan file. File tidak diunduh.

| File | Akses | Ukuran | Variabel | Observasi | Catatan |
| --- | --- | ---: | ---: | ---: | --- |
| `train_set_hki.tab` | Restricted | 39.391.483 byte | 13 | 6.241 | Dipublikasikan 2024-10-16 |
| `test_set_hki_rev.tab` | Restricted | 2.837.726 byte | 14 | 506 | Revisi label; dipublikasikan 2026-07-03 |
| `test_set_hki.tab` | Restricted | 2.837.726 byte | 14 | 506 | **Deprecated** karena bug mapping label; jangan digunakan |
| `sampel.xlsx` | Public | 26.037 byte | — | — | Data sampel; tidak diunduh pada Stage 1 |

`test_set_hki_rev.tab` memiliki deskripsi resmi: versi revisi data testing
dengan perbaikan label akibat kesalahan mapping saat konversi label numerik
(0/1) menjadi label `real` dan `fake`. File `test_set_hki.tab` secara eksplisit
disebut deprecated dan tidak boleh dipakai untuk evaluasi.

#### Provenance

Deskripsi resmi menyatakan:

- dataset berisi berita palsu (hoax) dan berita valid (real) berbahasa
  Indonesia;
- data dikumpulkan dari situs pelaporan hoaks dan portal berita online
  Indonesia;
- judul berita dari portal online diparafrase agar menyerupai klaim pada data
  pelaporan hoaks (Mafindo), lalu diberi label berita valid;
- semua klaim diperiksa ulang dengan bantuan API Bing dan LLM OpenAI;
- fakta disajikan sebagai poin-poin ringkasan;
- setiap klaim diberi atribusi `tone` (`neutral`/`not-neutral`) dan topik yang
  divalidasi manusia.

Implikasi audit:

- Provenance relatif jelas, tetapi data valid mengandung judul hasil parafrase,
  bukan judul asli. Ini perlu diuji sebagai potensi distribution shift dan
  artefak sintetis.
- Pemeriksaan fakta berbantuan Bing/OpenAI dan ringkasan fakta berbasis LLM
  perlu diaudit untuk label noise, hallucination, dan artefak gaya bahasa.
- Validasi manusia disebut untuk `tone` dan topik, **bukan** pernyataan bahwa
  seluruh label atau ringkasan fakta divalidasi manusia. Jangan memperluas
  klaim tersebut tanpa bukti.
- Sumber hulu mencakup data pelaporan hoaks Mafindo dan portal berita. Hak
  penggunaan hulu perlu dikonfirmasi; lisensi CC BY-NC 4.0 dari BRIN tidak
  otomatis menyelesaikan hak sumber hulu.

Publikasi terkait yang dicantumkan:

- R. Wijayanti and I. Ni'Mah, “Can BERT Learn Evidence-Aware Representation
  for Low Resource Fake News Detection?”, IC3INA 2024,
  DOI `10.1109/IC3INA64086.2024.10732358`.
- I. Ni'mah, R. Wijayanti, A. Santosa, et al., “A simple contrastive embedding
  framework for low-resource fake news detection”, Neural Computing and
  Applications (2025), DOI `10.1007/s00521-025-11467-0`.

#### Schema dan label

- Metadata publik menyebut 13 variabel pada train dan 14 variabel pada test,
  tetapi **nama, tipe, urutan, dan nilai label tidak diekspos** untuk file
  restricted.
- Export DDI dan metadata versi tidak memberikan daftar variabel yang dapat
  diverifikasi.
- `sampel.xlsx` bersifat publik, tetapi bukan pengganti audit file train/test.
- Deskripsi menyebut label `real`/`fake` pada catatan bug test lama, tetapi
  nilai label aktual, encoding, dan mapping-nya belum dapat dipastikan.
- Karena itu, jangan mengasumsikan bahwa label final adalah `HOAX`/`NON-HOAX`,
  `real`/`fake`, atau 0/1. Verifikasi setelah akses diberikan.

#### Penilaian

Kekuatan:

- rilis resmi dan terbaru yang dirujuk oleh kedua card HF;
- lisensi eksplisit CC BY-NC 4.0;
- metadata mencantumkan 6.241 observasi train dan 506 test; jumlah record HF
  belum diverifikasi;
- adanya train/test resmi dan versi test yang sudah diperbaiki;
- provenance dan publikasi pendukung tersedia.

Risiko/blocker:

- file restricted; pengguna harus mengajukan akses;
- schema dan label aktual belum terverifikasi;
- lisensi non-komersial; proyek belum punya `LICENSE` dan status komersialnya
  belum eksplisit;
- hak sumber hulu (Mafindo dan portal berita) belum jelas;
- test hanya 506 observasi; distribusi kelas dan support per kelas belum
  diketahui;
- judul valid diparafrase dan fakta dibantu LLM; perlu audit artefak dan label
  noise;
- split strategy, deduplikasi, overlap, dan timestamp belum diketahui.

### 4.2 HF `nlp-brin-id/fakenews-mafindo`

#### Identitas dan akses

| Atribut | Nilai |
| --- | --- |
| URL | <https://huggingface.co/datasets/nlp-brin-id/fakenews-mafindo> |
| Status | Gated `manual`; harus login dan menyetujui kondisi |
| Last modified | 2024-11-21 |
| Maintenance | Card menyatakan repository tidak dipelihara lagi |
| Lisensi metadata | `license: mit` |
| Pengganti yang dirujuk | BRIN Dataverse v2.1 |

File tree publik:

| File | Ukuran |
| --- | ---: |
| `train.csv` | 15.345.229 byte |
| `dev.csv` | 3.788.946 byte |
| `test.csv` | 385.198 byte |
| `README.md` | 1.885 byte |
| `.gitattributes` | 2.397 byte |

Jumlah record tidak diverifikasi karena file gated. Metadata ukuran juga tidak
konsisten: tag `size_categories` menyebut `1K<n<10K`, sedangkan `cardData`
menyebut `10K<n<100K`. Karena itu, metadata ukuran tidak boleh dipakai sebagai
jumlah record.

#### Schema yang didokumentasikan

Nama kolom diambil dari card. Tipe, urutan aktual, dan jumlah nilai unik belum
diverifikasi.

| Kolom | Deskripsi card | Peran yang disarankan |
| --- | --- | --- |
| `Label_id` | Binary class labels (`HOAX`=1, `NON-HOAX`=0) | Target, bukan fitur |
| `Label` | Binary class labels (`HOAX`/`NON-HOAX`) | Target, bukan fitur |
| `Title` | Claim atau headline berita | Kandidat fitur |
| `Title_cleaned` | Claim yang sudah dipreproses dengan menghapus tag di awal kalimat | Kandidat fitur hanya jika aturan cleaning direproduksi |
| `Content` | Isi artikel berita | Kandidat fitur; perlu verifikasi apakah ini klaim atau artikel fact-check |
| `Fact` | Ringkasan bukti faktual yang mendukung/membantah klaim | **Jangan dipakai sebagai fitur**; post-hoc dan berpotensi membocorkan label |
| `References` | URL artikel dan verdict/bukti faktual | **Jangan dipakai sebagai fitur**; berisi verdict |
| `Classification` | Label fine-grained | Target sekunder/analisis; bukan fitur |

#### Label

Binary:

- `HOAX` = 1
- `NON-HOAX` = 0

Fine-grained yang tercantum:

`CekFakta`, `Fabricated Content`, `False Connection`, `False Context`,
`Impostor Content`, `Manipulated Content`, `Misleading Content`, `Satire`,
`nan`.

Catatan:

- Card tidak memberikan definisi operasional untuk label fine-grained.
- `CekFakta` bukan nama jenis misinformation yang setara dengan tujuh tipe
  disinformasi/misinformasi yang dipakai sumber Jabar; bisa jadi penanda
  artikel fact-check. Jangan dianggap kelas hoax.
- `Satire` tidak otomatis sama dengan hoax; hubungannya ke label binary tidak
  dijelaskan.
- `nan` adalah nilai hilang/unknown, bukan kelas.
- `NON-HOAX` tidak didefinisikan. Label ini tidak boleh disamakan dengan
  `BENAR` atau “terverifikasi benar”.
- Card menyatakan dataset beta dan memiliki representasi `NON-HOAX` yang
  imbalanced, tetapi tidak memberikan angka.

#### Provenance dan hak penggunaan

- Data berasal dari `turnbackhoax.id` (Mafindo data 2018-2023).
- Mafindo terms menyatakan bahwa semua material adalah properti MAFINDO dan
  pengguna tidak boleh mereproduksi atau mendistribusikan ulang kekayaan
  intelektual MAFINDO. Kutipan dari arsip:
  > “You also agree that you will not reproduce or redistribute the MAFINDO's
  > intellectual property in any way, including electronic, digital, or new
  > trademark registrations.”
- Situs Mafindo/TurnBackHoax mengembalikan 502 saat dicek; arsip yang dipakai:
  <https://web.archive.org/web/20260209163951/https://mafindo.or.id/terms-of-use/>
  dan
  <https://web.archive.org/web/20251125185111/https://turnbackhoax.id/ketentuan-layanan>.
- Tidak ditemukan lisensi data/ML eksplisit dari Mafindo.
- Tag `license: mit` pada HF tidak cukup untuk menyimpulkan bahwa data hulu
  bebas digunakan kembali. Tag ini juga tidak konsisten dengan lisensi rilis
  BRIN Dataverse yang lebih baru, yaitu CC BY-NC 4.0.

#### Split

- Terdapat file `train.csv`, `dev.csv`, dan `test.csv`.
- Strategi split, seed, stratifikasi, deduplikasi, grouping, dan overlap antar
  split tidak didokumentasikan.
- Card example memakai nama dataset `nlp-brin-id/fakenews-id-brin`, bukan nama
  repository ini. Example tersebut tidak dapat dianggap sebagai dokumentasi
  yang dapat langsung dijalankan.

#### Penilaian

Kekuatan:

- schema lebih mudah dipahami daripada BRIN Dataverse;
- sudah ada pemisahan train/dev/test;
- binary label tersedia;
- ukuran file relatif kecil dan bisa diuji setelah akses.

Risiko/blocker:

- gated dan tidak dipelihara;
- beta dan imbalanced;
- label fine-grained ambigu;
- `Fact`, `References`, dan `Classification` adalah post-hoc;
- Mafindo terms membatasi reproduksi/redistribusi;
- tidak ada lisensi ML/data hulu yang jelas;
- split belum tentu bebas leakage;
- tidak ada timestamp eksplisit di schema yang didokumentasikan.

Status: **fallback saja**, bukan pilihan utama.

### 4.3 HF `nlp-brin-id/id-hoax-report`

#### Identitas dan akses

| Atribut | Nilai |
| --- | --- |
| URL | <https://huggingface.co/datasets/nlp-brin-id/id-hoax-report> |
| Status | Gated `manual`; harus login dan menyetujui kondisi |
| Last modified | 2024-11-21 |
| Maintenance | Card menyatakan repository tidak dipelihara lagi |
| Lisensi metadata | `license: mit` |
| Sumber | Saber Hoaks Jabar, Open Data Jabar, Klinik Hoaks Jatim |

File tree publik:

| File | Ukuran |
| --- | ---: |
| `saberhoax_data.csv` | 5.390.211 byte |
| `opendata_jabar.csv` | 95.052 byte |
| `klinikhoax_jatim.csv` | 183.750 byte |
| `README.md` | 1.965 byte |
| `.gitattributes` | 2.307 byte |

Tidak ada file `train`/`dev`/`test`. Card example menggunakan
`split="train"`, tetapi tidak ada split yang didokumentasikan; contoh card
bukan bukti adanya split resmi. Jumlah record, duplikasi, dan distribusi label
tidak diverifikasi.

#### Schema yang didokumentasikan

| Kolom | Deskripsi card | Peran yang disarankan |
| --- | --- | --- |
| `Label_id` | Binary class labels (`HOAX`=1, `NON-HOAX`=0) | Target |
| `Label` | Binary class labels (`HOAX`/`NON-HOAX`) | Target |
| `Title` | Claim atau headline berita | Kandidat fitur |
| `Content` | Isi artikel berita | Kandidat fitur; perlu verifikasi |
| `Fact` | Ringkasan bukti faktual | **Jangan dipakai sebagai fitur** |
| `References` | URL dan verdict/bukti | **Jangan dipakai sebagai fitur** |
| `Classification` | Label fine-grained per sumber | Target/analisis; bukan fitur |

Tidak ada `Title_cleaned` pada card ini.

#### Label

Card hanya mendokumentasikan label fine-grained untuk dua file:

`saberhoax_data.csv`:

`DISINFORMASI`, `MISINFORMASI`, `FABRICATED CONTENT`, `FALSE CONNECTION`,
`FALSE CONTEXT`, `IMPOSTER CONTENT`, `MANIPULATED CONTENT`,
`MISLEADING CONTENT`, `SATIRE OR PARODI`, `BENAR`.

`opendata_jabar.csv`:

`BENAR`, `DISINFORMASI (HOAKS)`, `FABRICATED CONTENT`, `FALSE CONNECTION`,
`FALSE CONTEXT`, `IMPOSTER CONTENT`, `MANIPULATED CONTENT`,
`MISINFORMASI (HOAKS)`, `MISLEADING CONTENT`.

`klinikhoax_jatim.csv` **tidak memiliki daftar label fine-grained di card**.
Ini blocker penting karena situs Klinik Hoaks Jatim memiliki setidaknya enam
kategori:

| Kategori Klinik Hoaks | Definisi dari situs |
| --- | --- |
| Hoaks | Informasi yang mengandung data palsu/salah/tidak terbukti kebenarannya |
| Disinformasi | Informasi yang diolah sehingga menimbulkan bias makna pada suatu isu |
| Fakta | Data yang benar terjadi dan dapat dibuktikan |
| Hate Speech | Pendapat/ide/pikiran terhadap suatu isu yang ditujukan untuk membangun kebencian |
| Lainnya | Kategori tambahan yang tampil di situs |
| Opini | Kategori tambahan yang tampil di situs |

Situs juga menampilkan contoh kategori `Hate Speech`, `Lainnya`, dan `Opini`.
Tidak ada penjelasan bagaimana kategori-kategori ini dipetakan ke label binary
`HOAX`/`NON-HOAX` di file HF. Jangan mengasumsikan `Fakta` = `NON-HOAX` atau
`Disinformasi` = `HOAX` tanpa verifikasi.

Perbedaan lain:

- Halaman `data.go.id` untuk dataset Jabar menyebut tujuh jenis
  disinformasi/misinformasi: satire/parody, misleading content, manipulated
  content, false connection, false context, imposter content, dan fabricated
  content. Halaman itu **tidak** menyebut `BENAR`.
- Card HF `opendata_jabar.csv` justru mencantumkan `BENAR`. Ini menunjukkan
  label pada file turunan tidak identik dengan taxonomy di halaman sumber.
- `DISINFORMASI` dan `MISINFORMASI` adalah pembedaan berbasis niat/konteks;
  card tidak memberikan definisi. Jangan digabung tanpa aturan eksplisit.
- `SATIRE OR PARODI` tidak otomatis hoax; hubungannya ke binary label tidak
  dijelaskan.
- `BENAR` berarti sumber menilai klaim benar/terverifikasi; `NON-HOAX` belum
  tentu berarti terverifikasi benar. Keduanya tidak ekuivalen.

#### Provenance dan hak penggunaan

- Saber Hoaks Jabar: situs resmi menyediakan klarifikasi dan data; tidak
  ditemukan lisensi data eksplisit.
- Open Data Jabar: ketentuan penggunaan memberikan hak terbatas, non-eksklusif,
  tidak dapat disublisensikan, dan hanya untuk **penggunaan non-komersial
  pribadi**. Ketentuan juga melarang penggunaan komersial dan mengakses data
  yang tidak berhak. Ini membatasi redistribusi dataset turunan.
- Klinik Hoaks Jatim: tidak ditemukan lisensi data eksplisit.
- Tag `license: mit` pada HF tidak menyelesaikan ketentuan sumber hulu.
- Data Jabar berasal dari laporan/klarifikasi yang merujuk media lain; hak
  kutipan/rujukan perlu diperhatikan.

#### Split dan kualitas

- Tidak ada split resmi.
- Tiga file berasal dari tiga sumber berbeda; menggabungkannya akan menciptakan
  source bias dan label heterogeneity.
- Duplikasi lintas file mungkin terjadi karena sumber berbagi klaim/rujukan;
  belum diukur.
- Tidak ada timestamp field yang terdokumentasi; analisis tren tidak dapat
  diasumsikan.

#### Penilaian

Kekuatan:

- sumbernya jelas per file;
- schema teks/label dasar tersedia;
- berguna untuk studi perbedaan label dan source bias.

Risiko/blocker:

- label heterogen dan sebagian tidak terdokumentasi;
- tidak ada split;
- `Fact`/`References` berpotensi leakage;
- ketentuan sumber membatasi penggunaan/redistribusi;
- tidak dipelihara.

Status: **eksploratif saja**, bukan dataset training utama MVP.

### 4.4 `data.go.id` Jabar fact-checking

#### Identitas dan status

| Atribut | Nilai |
| --- | --- |
| URL | <https://data.go.id/dataset/dataset/data-pengecekan-fakta-fact-checking> |
| Dataset ID | `8e744770-b9e8-4dde-8400-25c3d8487f40` |
| Dibuat | 2024-06-28 |
| Dimodifikasi | 2024-12-08 |
| Sumber | Open Data Jabar |
| `isopen` | `false` |
| `private` | `true` |
| `license_title` | `null` |
| `review_status` | `rejected` |
| Catatan kurasi | `broken_link`, `not_complete` |
| Resource | CSV `.../od_18946_data_pengecekan_fakta_fact_checking?download=csv` |

Halaman menampilkan badge “Terbuka”, tetapi metadata internal menyatakan
`isopen:false`, `private:true`, dan `review_status:rejected`. Halaman juga
menampilkan “URL Bermasalah”. Catatan kurasi menyatakan:

- source tidak dapat terhubung dan menampilkan 404;
- dataset dapat diunduh lewat URL resource;
- definisi menyebut data 2020–2022, tetapi CSV hanya menampilkan 2022.

Resource metadata memiliki `url_status.error = "pending"`, `size: null`,
`hash: ""`, dan `datastore_active: false`. Percobaan `HEAD` ke URL CSV
mengembalikan **403** dari environment ini. Pada pengecekan ulang di hari yang
sama, domain `data.go.id` mengembalikan **404** dari environment ini; ini bisa
berarti situs tidak stabil atau memblokir environment, bukan bukti definitif
tentang isi CSV. Snapshot halaman yang terbaca lebih awal tetap dipakai untuk
metadata di atas.

#### Schema yang didokumentasikan

Halaman sumber mendokumentasikan 12 field:

| Field | Arti menurut halaman |
| --- | --- |
| `Tanggal` | Tanggal aduan/pemantauan; halaman menyebut tipe numerik |
| `Judul klaim` | Tajuk klaim/isu |
| `Aduan atau pantauan` | Jenis tindakan pengecekan fakta |
| `Jenis materi aduan/pantauan` | Bentuk materi (video, teks, foto, gabungan) |
| `Topik` | Kategori isu |
| `Sub topik` | Turunan topik |
| `Lokasi` | Lokasi klaim |
| `Sub lokasi` | Lokasi lebih spesifik |
| `Jenis disinformasi/misinformasi` | Tujuh jenis disinformasi/misinformasi |
| `Sumber hoaks` | Platform sumber hoaks |
| `Kanal aduan` | Kanal aduan/pemantauan |
| `Media rujukan` | Media rujukan utama |

Tujuh jenis yang disebut halaman sumber: satire/parody, misleading content,
manipulated content, false connection, false context, imposter content, dan
fabricated content. Halaman tidak menyebut `BENAR`.

#### Penilaian

Status: **tidak disetujui**. Dataset tidak boleh dipakai untuk MVP karena:

- metadata menyatakan tidak terbuka, privat, dan rejected;
- tidak ada lisensi eksplisit;
- resource ditandai bermasalah dan tidak lengkap;
- cakupan tanggal tidak konsisten;
- CSV tidak dapat diverifikasi dari environment ini.

Dataset ini hanya boleh dipakai sebagai referensi/rujukan sejarah, bukan
sumber training, sampai metadata, lisensi, dan file diperbaiki.

### 4.5 Turunan HF yang ditemukan

Ditemukan dataset turunan berikut:

- `nlp-brin-id/id-hoax-report-merge`
- `nlp-brin-id/id-hoax-report-merge-v2`
- `nlp-brin-id/id-hoax-report-merge-v3`
- `nlp-brin-id/unsup-content`

Semuanya gated `manual`, bertag MIT, dan tidak dipelihara. Belum diaudit pada
Stage 1 dan bukan kandidat MVP.

Satu temuan penting: card `id-hoax-report-merge-v2` menyatakan bahwa versi itu
membersihkan `Fact` agar tidak memuat ringkasan eksplisit klasifikasi
`Hoax`/`Non-Hoax`, dengan menghapus kalimat yang mengandung n-gram seperti
`adalah hoaks`, `tidak benar`, `konten palsu`, dan sejenisnya. Ini adalah bukti
langsung bahwa field `Fact` pada data sejenis dapat mengandung label. Untuk
dataset asal, `Fact` tetap harus dianggap post-hoc dan tidak boleh menjadi
fitur.

## 5. Perbandingan schema dan label

| Aspek | BRIN Dataverse v2.1 | HF `fakenews-mafindo` | HF `id-hoax-report` | `data.go.id` Jabar |
| --- | --- | --- | --- | --- |
| Unit data | Klaim/berita + fakta | Klaim/berita + fakta | Klaim/berita + fakta per sumber | Klaim/berita + metadata fact-check |
| Kolom teks utama | Tidak terverifikasi | `Title`, `Content` | `Title`, `Content` | `Judul klaim`; teks lain tidak terdokumentasi sebagai isi artikel |
| Target biner | Tidak terverifikasi | `HOAX`/`NON-HOAX` | `HOAX`/`NON-HOAX` | Tidak ada label biner eksplisit di metadata |
| Label detail | Tidak terverifikasi | 9 nilai termasuk `CekFakta`, `Satire`, `nan` | Per sumber; `klinikhoax_jatim.csv` tidak terdokumentasi | 7 tipe disinformasi/misinformasi |
| Split | Train/test resmi; strategi belum diketahui | `train`/`dev`/`test`; strategi belum diketahui | Tidak ada | Tidak ada |
| Lisensi | CC BY-NC 4.0 | Tag MIT; tidak konsisten dengan hulu dan rilis BRIN | Tag MIT; tidak konsisten dengan ketentuan Jabar/Klinik | Tidak ada (`null`) |
| Akses | Restricted | Gated | Gated | CSV 403; metadata rejected |
| Status | Rilis resmi terbaru | Tidak dipelihara | Tidak dipelihara | Tidak disetujui |

### 5.1 Isu ekuivalensi label

- `HOAX` dan `NON-HOAX` adalah label biner yang didefinisikan oleh pembuat
  dataset, bukan hasil verifikasi independen HoaxScope.
- `BENAR` bukan sinonim `NON-HOAX`. `BENAR` menyiratkan klaim terverifikasi
  benar; `NON-HOAX` bisa berarti tidak terklasifikasi sebagai hoax, termasuk
  satire, opini, atau kasus yang tidak terbukti.
- `DISINFORMASI` dan `MISINFORMASI` berbeda secara intent/konteks; definisi
  tidak tersedia di card. Jangan digabung tanpa aturan.
- `SATIRE OR PARODI`/`Satire` tidak otomatis hoax.
- `CekFakta` bukan kategori misinformation yang setara dengan tujuh tipe
  disinformasi/misinformasi sumber Jabar.
- `Hate Speech`, `Opini`, dan `Lainnya` bukan label hoax biner; harus
  dikeluarkan atau dianalisis terpisah.
- `nan` adalah missing/unknown, bukan kelas.
- Label multi-kelas tidak mutually exclusive secara otomatis; jangan
  menganggapnya sebagai klasifikasi tunggal tanpa audit.

### 5.2 Target yang disarankan untuk MVP

Pada Stage 2, gunakan **binary classification** sesuai label sumber, dengan
aturan:

- target internal: `hoax` dan `not_flagged_as_hoax`;
- `NON-HOAX`/`BENAR`/`Fakta` hanya dipetakan ke `not_flagged_as_hoax` jika
  definisi sumber dan mapping per row sudah diverifikasi;
- label asli tetap disimpan di `label_source`/`label_detail`;
- label yang ambigu (`CekFakta`, `Satire`, `Hate Speech`, `Opini`, `Lainnya`,
  `nan`) tidak dipaksa masuk binary target tanpa keputusan eksplisit;
- jangan menggabungkan dataset berbeda dalam satu training set MVP;
- jangan menganggap `not_flagged_as_hoax` sebagai bukti kebenaran.

## 6. Leakage, preprocessing, dan split

### 6.1 Field post-hoc

`Fact`, `References`, dan `Classification` adalah hasil proses fact-check atau
label turunan. Ketiganya tidak boleh menjadi fitur input:

- `Fact` meringkas bukti yang mendukung/membantah klaim;
- `References` memuat URL dan verdict/bukti;
- `Classification` adalah label fine-grained.

Card turunan `id-hoax-report-merge-v2` secara eksplisit menyatakan bahwa `Fact`
dibersihkan karena memuat klasifikasi hoax. Ini memperkuat aturan bahwa field
tersebut tidak boleh dipakai untuk inference.

### 6.2 `Title_cleaned`

`Title_cleaned` pada `fakenews-mafindo` dibuat dengan menghapus tag label di
awal kalimat. Ini adalah preprocessing sumber, bukan preprocessing HoaxScope.
Untuk inference yang konsisten:

- gunakan `Title` mentah; atau
- reproduksi aturan cleaning secara eksplisit dan uji dampaknya.

Jangan mencampur `Title` dan `Title_cleaned` tanpa dokumentasi.

### 6.3 `Content`

Card menyebut `Content` sebagai isi artikel berita. Perlu diverifikasi apakah
isi tersebut adalah klaim/artikel yang diperiksa atau artikel fact-check yang
memuat verdict. Jika yang kedua, `Content` juga berpotensi leakage. Baseline
awal sebaiknya memakai `Title` saja atau `Title` + `Content` hanya setelah
audit.

### 6.4 Duplikasi dan split

Belum ada pengukuran duplikasi. Untuk Stage 2:

- lakukan exact duplicate dan near-duplicate audit;
- kelompokkan berdasarkan klaim, judul, URL, dan sumber;
- jangan melakukan random split sebelum grouping;
- pertahankan test set resmi jika tersedia;
- jangan memakai test untuk tuning atau pemilihan fitur;
- periksa overlap train/test dan distribusi label per split;
- pertimbangkan temporal split jika timestamp tersedia dan valid.

Untuk BRIN v2.1, gunakan `test_set_hki_rev.tab`, bukan `test_set_hki.tab`.
Test resmi hanya 506 observasi; laporkan support per kelas dan jangan
menginterpretasikan perbedaan kecil sebagai peningkatan bermakna tanpa
ketidakpastian.

## 7. Matriks kesesuaian MVP

| Kriteria | BRIN v2.1 | HF Mafindo | HF id-hoax-report | Jabar |
| --- | --- | --- | --- | --- |
| Sumber resmi dan terbaru | ✅ | ⚠️ tidak dipelihara | ⚠️ tidak dipelihara | ⚠️ metadata rejected |
| Lisensi jelas | ✅ CC BY-NC 4.0 | ⚠️ tag MIT, tidak konsisten | ⚠️ tag MIT, tidak konsisten | ❌ tidak ada |
| Akses file | ❌ restricted, perlu request | ⚠️ gated | ⚠️ gated | ❌ CSV 403 |
| Provenance | ✅ dengan catatan hulu | ⚠️ Mafindo 2018–2023 | ⚠️ tiga sumber berbeda | ⚠️ tidak lengkap |
| Schema aktual terverifikasi | ❌ | ⚠️ nama kolom saja | ⚠️ nama kolom saja | ⚠️ deskripsi saja |
| Definisi label | ❌ belum terverifikasi | ⚠️ binary jelas, fine ambigu | ❌ heterogen/tidak lengkap | ⚠️ 7 tipe, tanpa BENAR |
| Split | ✅ tersedia, strategi belum | ✅ file tersedia, strategi belum | ❌ tidak ada | ❌ tidak ada |
| Distribusi kelas | ❓ | ⚠️ imbalanced, tanpa angka | ❓ | ❓ |
| Hak sumber hulu | ⚠️ perlu review | ❌ Mafindo membatasi | ❌ Jabar/Klinik membatasi | ❌ tidak jelas |
| Kesesuaian MVP | **⚠️ utama kondisional** | **⚠️ fallback** | **❌ eksploratif** | **❌ tidak disetujui** |

Keterangan: ✅ = memadai untuk tahap ini; ⚠️ = ada risiko/blocker yang harus
diselesaikan; ❌ = tidak memenuhi syarat; ❓ = belum diverifikasi.

## 8. Rekomendasi

### 8.1 Kandidat utama: BRIN Dataverse v2.1

Rekomendasi: jadikan **BRIN Dataverse v2.1**
(`hdl:20.500.12690/RIN/7QBRKQ`) sebagai kandidat utama MVP, **bukan** sebagai
persetujuan final.

Alasan:

- ini rilis resmi terbaru yang dirujuk oleh kedua card HF;
- lisensinya eksplisit CC BY-NC 4.0;
- metadata mencantumkan 6.241 train + 506 test serta test revisi resmi;
- provenance dan publikasi pendukung tersedia;
- menghindari ketergantungan pada dataset HF yang sudah tidak dipelihara.

Syarat sebelum pipeline:

1. Pengguna mengajukan dan mendapatkan akses ke file restricted.
2. Pengguna mengonfirmasi bahwa penggunaan proyek bersifat non-komersial dan
   mematuhi CC BY-NC 4.0, termasuk atribusi.
3. Ada review hak sumber hulu (Mafindo dan portal berita); jika proyek akan
   dipublikasikan, pertimbangkan legal review atau izin tertulis.
4. Setelah akses: verifikasi schema aktual, tipe, nilai label, mapping,
   encoding, timestamp, dan dokumentasi split.
5. Audit duplikasi, overlap train/test, class imbalance, label noise, artefak
   parafrase/LLM, dan potensi leakage.
6. Gunakan `test_set_hki_rev.tab`; jangan gunakan `test_set_hki.tab`.
7. Jangan memakai `Fact`, `References`, atau field turunan fact-check sebagai
   fitur.

Jika salah satu syarat tidak terpenuhi, dataset belum boleh masuk pipeline.

### 8.2 Fallback: HF `fakenews-mafindo`

Hanya jika:

- akses BRIN ditolak atau tidak tersedia dalam waktu yang wajar; dan
- pengguna secara eksplisit menerima risiko ketentuan Mafindo dan
  ketidaksesuaian lisensi.

Aturan fallback:

- gunakan label binary saja;
- jangan memakai `Fact`, `References`, atau `Classification` sebagai fitur;
- gunakan `Title` mentah atau reproduksi `Title_cleaned`;
- lakukan grouping/deduplikasi sebelum split;
- jangan mendistribusikan ulang raw data;
- dokumentasikan bahwa dataset beta, tidak dipelihara, dan imbalanced;
- jangan mengklaim hasilnya sebagai representasi seluruh berita Indonesia.

### 8.3 Eksploratif: HF `id-hoax-report`

Gunakan hanya untuk:

- analisis perbedaan label antar sumber;
- studi source bias;
- perbandingan taksonomi;
- eksperimen terpisah yang tidak menjadi baseline MVP.

Jangan jadikan dataset training utama tanpa mapping label, split, deduplikasi,
dan penyelesaian hak sumber.

### 8.4 Tidak disetujui: `data.go.id` Jabar

Jangan gunakan sampai:

- metadata `isopen`, `private`, `review_status`, dan lisensi diperbaiki;
- catatan `broken_link`/`not_complete` diselesaikan;
- CSV dapat diunduh dan diverifikasi;
- cakupan 2020–2022 sesuai dengan isi file;
- ada dasar penggunaan yang jelas.

### 8.5 Jangan menggabungkan dataset pada MVP

Perbedaan unit data, definisi label, sumber, periode, dan lisensi membuat
penggabungan berisiko. MVP harus memakai satu dataset utama dan satu label
mapping yang eksplisit.

## 9. Keputusan yang diminta

Stage 1 berhenti di sini. Sebelum Stage 2, pengguna perlu memutuskan:

1. Setujui BRIN Dataverse v2.1 sebagai kandidat utama dan ajukan akses file?
2. Konfirmasi bahwa proyek memenuhi syarat non-komersial CC BY-NC 4.0?
3. Jika akses BRIN tidak memungkinkan, setujui HF `fakenews-mafindo` sebagai
   fallback dengan risiko ketentuan Mafindo?
4. Jika keduanya tidak memungkinkan, apakah akan mencari dataset lain dengan
   lisensi yang jelas, atau menghentikan Phase 1?

Sampai keputusan itu ada:

- tidak ada dataset yang disetujui;
- tidak ada loader, preprocessing, split, atau training;
- tidak ada API atau dashboard;
- `DATASET.md` belum diisi dengan hasil audit final karena dataset belum
  disetujui.

## 10. Validasi dan keterbatasan

### 10.1 Validasi yang dilakukan

- Mengambil metadata versi BRIN v2.1 melalui API Dataverse dan halaman dataset.
- Mengambil file tree dan card publik HF melalui API/page.
- Memeriksa respons HTTP untuk resource `data.go.id` dan halaman sumber.
- Membaca ketentuan Open Data Jabar.
- Membaca arsip ketentuan Mafindo/TurnBackHoax karena situs live 502.
- Membaca definisi kategori Klinik Hoaks dari situs resmi.
- Memastikan working tree bersih dan tidak ada file dataset/model yang masuk
  repository.

### 10.2 Keterbatasan

- File BRIN restricted; schema, tipe, label, dan isi aktual belum diverifikasi.
- File HF gated `manual`; raw README mengembalikan 401, sehingga schema dan
  record count tidak dapat diperiksa.
- `data.go.id` tidak stabil dari environment ini; CSV mengembalikan 403 dan
  halaman kemudian 404. Metadata snapshot dipakai, bukan isi CSV.
- Tidak ada record count, distribusi kelas, missing value, duplikasi, panjang
  teks, timestamp, atau hasil EDA yang dihitung.
- Audit PII, konten sensitif, dan kepatuhan hak cipta teks berita belum
  dilakukan.
- Angka file size, variabel, dan observasi BRIN berasal dari metadata, bukan
  audit file.
- Penilaian lisensi bukan nasihat hukum. Hak sumber hulu perlu ditinjau
  terpisah.
- Belum ada test/lint/type-check aplikasi yang relevan karena tidak ada kode
  pipeline pada Stage 1.

## 11. Langkah berikutnya

Setelah keputusan pengguna:

1. Ajukan akses BRIN dan simpan bukti persetujuan.
2. Unduh hanya file yang disetujui ke `ml/data/raw/` (tidak di-commit).
3. Audit schema/label aktual, duplikasi, distribusi, timestamp, dan overlap.
4. Susun canonical schema dan label mapping di `DATASET.md`.
5. Tetapkan split strategy dan test protocol.
6. Baru masuk implementasi loader/validation/preprocessing.

Tanpa keputusan tersebut, Phase 2 tidak dimulai.

## 12. Referensi

- BRIN Dataverse v2.1:
  <https://data.brin.go.id/dataset.xhtml?persistentId=hdl:20.500.12690/RIN/7QBRKQ>
- BRIN DDI export:
  <https://data.brin.go.id/api/datasets/export?exporter=ddi&persistentId=hdl:20.500.12690/RIN/7QBRKQ>
- HF `fakenews-mafindo`:
  <https://huggingface.co/datasets/nlp-brin-id/fakenews-mafindo>
- HF `id-hoax-report`:
  <https://huggingface.co/datasets/nlp-brin-id/id-hoax-report>
- HF `id-hoax-report-merge-v2`:
  <https://huggingface.co/datasets/nlp-brin-id/id-hoax-report-merge-v2>
- `data.go.id` Jabar:
  <https://data.go.id/dataset/dataset/data-pengecekan-fakta-fact-checking>
- Open Data Jabar:
  <https://opendata.jabarprov.go.id/id/dataset/data-pengecekan-fakta-fact-checking>
- Open Data Jabar terms:
  <https://opendata.jabarprov.go.id/id/ketentuan-penggunaan>
- Jabar Saber Hoaks:
  <https://saberhoaks.jabarprov.go.id/v2/home>
- Klinik Hoaks Jatim:
  <https://klinikhoaks.jatimprov.go.id/>
- Mafindo terms (arsip):
  <https://web.archive.org/web/20260209163951/https://mafindo.or.id/terms-of-use/>
- TurnBackHoax terms (arsip):
  <https://web.archive.org/web/20251125185111/https://turnbackhoax.id/ketentuan-layanan>
