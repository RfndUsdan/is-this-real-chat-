# Stage 3 --- Canonical Schema & Data Pipeline Audit

- **Tanggal:** 2026-11-24
- **Status:** selesai; **training Phase 2 tidak dijalankan**
- **Scope:** Phase 1 Stage 3 hanya. Tidak ada scraping, merge dataset,
  perubahan label, API, dashboard, atau model training.
- **Sumber:** Mendeley `p3hfgr5j3m` versi 1, hanya
  `600 news with valid hoax label.csv` dan workbook
  `600 news labelling process.xlsx` untuk audit.
- **Manifest:**
  CSV 1.335.120 byte, SHA-256
  `8c16f1e6258f3a828381c0e4b12ecee6730111c7c5be95ef5e70725201631f67`;
  workbook 88.152 byte, SHA-256
  `ab2b269cf5df8068a11a8e823b8db55ca5f15671da7ea41699848fda0816c28a`.
- **Storage:** data mentah tetap di direktori sementara di luar repository.
  Laporan JSON dibuat di `ml/data/processed/` yang diabaikan Git.
  Tidak ada raw text atau URL yang ditulis ke laporan.

## 1. Struktur canonical schema

Implementasi: `ml/src/hoaxscope_ml/data/schema.py`.

| Field | Aturan |
| --- | --- |
| `record_id` | `mendeley_p3hfgr5j3m:v1:row:{source_row}`. Berasal dari posisi baris, bukan isi teks; aman untuk laporan. |
| `source_row` | Nomor baris CSV 1-based termasuk header; provenance dan dasar ID. |
| `text` | Teks mentah sumber. Hanya ada di memori/penyimpanan lokal yang diabaikan Git; tidak masuk laporan. |
| `source_label` | Label CSV asli (`Valid` atau `Hoax`) dan tidak diubah. |
| `target_label` | `Valid → not_flagged_as_hoax`; `Hoax → hoax`. Tidak pernah diganti menjadi `true` atau `verified`. |
| `source_dataset` | `mendeley_p3hfgr5j3m`. |
| `dataset_version` | `1`. |
| `url_group_id` | `url-{sha256(url)[:12]}` dari workbook, atau `None`. Opaque: URL tidak dipublikasikan. |
| `duplicate_group_id` | `dup-r{row:04d}`, hasil gabungan URL + near-duplicate components. |
| `label_conflict` | `True` bila komponen duplikat memuat lebih dari satu `target_label`. |
| `split` | Turunan Stage 3: `train`, `validation`, `test`, atau `None` bila dikarantina. |

`CanonicalRecord.report_dict()` secara eksplisit mengecualikan `text`.
Pemetaan workbook adalah `row_order_inference_12x50` dan tetap dicatat
sebagai hasil audit berdasarkan urutan baris, **bukan relasi resmi**.
Workbook voting hanya menghasilkan `vote_disagreement_count`, bukan label
pengganti.

## 2. Hasil validasi

Implementasi: `ml/src/hoaxscope_ml/data/loader.py` dan
`ml/src/hoaxscope_ml/data/validation.py`.

| Pemeriksaan | Hasil aktual |
| --- | --- |
| File | `600 news with valid hoax label.csv`, CP1252 strict, delimiter `;` |
| Header | `['berita', 'tagging']` |
| Line ending | CRLF; UTF-8 BOM tidak ada |
| SHA-256 | sesuai manifest Stage 2 |
| Record | 600 |
| Label sumber | 372 `Valid`, 228 `Hoax` |
| Label target | 372 `not_flagged_as_hoax`, 228 `hoax` |
| Teks kosong/whitespace-only | 0 |
| Karakter kontrol tidak valid | 0 |
| Exact duplicate | 0 |
| Duplicate setelah NFKC + whitespace normalization | 0 |
| Baseline comparisons | 5/5 cocok |

Jika ada discrepancy, pipeline menulis laporan validasi lalu berhenti;
data tidak pernah diubah agar sesuai baseline. Enam kondisi blocking
meliputi file/hash, header, encoding/BOM, tipe field, label tidak dikenal,
teks kosong/karakter kontrol, duplikasi, dan distribusi baseline.

## 3. Hasil deduplikasi

Implementasi: `ml/src/hoaxscope_ml/data/workbook.py` dan
`ml/src/hoaxscope_ml/data/dedup.py`.

### URL grouping (terpisah)

Workbook 12 sheet `KW1`–`KW12` dipetakan berurutan ke 600 baris CSV.
Hasilnya mereproduksi baseline: 600 link terpetakan, 567 URL unik, 31 grup
URL duplikat/64 baris, dan 9 perbedaan label CSV vs voting workbook.
URL tidak disimpan sebagai teks mentah di laporan; hanya `url_group_id`
opaque yang dipakai.

### Near-duplicate text detection (terpisah)

Parameter: 5-word shingles, casefold, token alfanumerik Indonesia,
Jaccard ≥ 0.5, prefilter rasio panjang ≥ 0.2.

| Metrik | Hasil aktual |
| --- | ---: |
| Pasangan kandidat | 332 |
| Komponen near-duplicate multi-record | 91 |
| Komponen terbesar | 16 |
| Komponen near-duplicate dengan konflik label | 27 |

### Connected components gabungan

Hubungan URL dan near-duplicate disatukan dengan union-find transitif.
Tidak ada record yang dihapus.

| Metrik | Hasil aktual |
| --- | ---: |
| Total komponen akhir | 431 |
| Komponen multi-record | 93 |
| Komponen singleton | 338 |
| Komponen akhir dengan konflik label | 29 |
| Record terdampak konflik | 92 |

Distribusi ukuran 93 komponen multi-record:

| Ukuran | Jumlah komponen |
| ---: | ---: |
| 2 | 61 |
| 3 | 15 |
| 4 | 8 |
| 5 | 4 |
| 6 | 2 |
| 7 | 1 |
| 8 | 1 |
| 16 | 1 |

Daftar lengkap `component_id(size)` ada di Lampiran A. Detail per
komponen, termasuk `record_ids` dan `target_label_counts`, ada di
`ml/data/processed/stage3-dedup.json`.

## 4. Kebijakan konflik label

- `source_label` dan `target_label` dari CSV tidak diubah.
- Voting workbook adalah bahan audit; 9 perbedaan tidak dipakai untuk
  mengganti label CSV.
- Jika sebuah komponen gabungan memiliki lebih dari satu `target_label`,
  seluruh anggota ditandai `label_conflict=True`.
- Record tersebut dikarantina dari benchmark utama dengan alasan
  `label_conflict_in_duplicate_component`, bukan dihapus.
- Laporan karantina terpisah: `ml/data/processed/stage3-quarantine.json`.
  Isinya hanya `record_id`, `component_id`, dan alasan; tidak ada raw text
  atau URL.
- Kebijakan akhir untuk record konflik tetap memerlukan keputusan pemilik;
  Stage 3 hanya menyiapkan daftar dan alasannya.

## 5. Hasil preprocessing

Implementasi: `ml/src/hoaxscope_ml/preprocessing/text.py`.

| Opsi | Default Stage 3 |
| --- | --- |
| Unicode normalization | NFKC |
| HTML cleanup | aktif |
| URL handling | `placeholder` (` URL `) |
| Whitespace normalization | aktif |
| Lowercase | nonaktif |
| Tokenization | nonaktif |
| Stemming / stopword removal | tidak ada |

Urutan transformasi tetap dan tanpa state yang dipelajari, sehingga
reproduktif. Negasi (`tidak`), angka, dan urutan kalimat dipertahankan.

Dari 508 record yang layak split:

| Metrik | Hasil |
| --- | ---: |
| Rata-rata panjang teks mentah | 2.206,56 karakter |
| Rata-rata panjang teks terproses | 2.200,85 karakter |
| Record yang memendek | 339 |

Teks mentah tidak ditimpa; `PreprocessedRecord` adalah representasi turunan.
TF-IDF/vocabulary dan transformasi lain yang belajar dari data tidak
dilakukan pada Stage 3.

## 6. Strategi group-aware split

Implementasi: `ml/src/hoaxscope_ml/data/split.py`.

1. Record dengan `label_conflict=True` dikeluarkan dari kandidat split.
2. Group key adalah `duplicate_group_id` (gabungan URL + near-duplicate
   components), sehingga satu komponen tidak pernah terbagi.
3. Group diurutkan deterministik berdasarkan ukuran menurun, lalu ID.
4. Target label per split dihitung dari rasio 70/15/15 dengan pembulatan
   deterministik; target adalah sasaran, bukan paksaan.
5. Setiap group diberikan ke split dengan overlap defisit label terbesar;
   tie-break memakai urutan yang diacak dengan seed `20261124`.
6. Jika greedy menyisakan split kosong, group terkecil dari donor yang
   masih memiliki lebih dari satu group dipindahkan, bukan memaksa razio.
7. Jika leakage check gagal, `SplitImpossibleError` dilempar dan split
   tidak dikeluarkan.

Jumlah group kandidat: 402 dari 508 record. Seed, parameter similarity,
jumlah group, distribusi label, dan jumlah record dicatat di
`ml/data/processed/stage3-split.json`.

## 7. Distribusi train, validation, dan test

| Split | Record | Group | `hoax` | `not_flagged_as_hoax` | Target label (hoax / not flagged) |
| --- | ---: | ---: | ---: | ---: | --- |
| train | 356 | 342 | 133 | 223 | 133 / 223 |
| validation | 76 | 40 | 28 | 48 | 28 / 48 |
| test | 76 | 20 | 29 | 47 | 29 / 47 |

Rasio aktual 356/508 (70,1%), 76/508 (15,0%), 76/508 (15,0%).
Stratifikasi label mencapai target persis pada eksperimen ini tanpa
memecah group. Angka ini berlaku hanya untuk hash file, config, dan seed
yang tercatat.

## 8. Hasil leakage checks

Enam pemeriksaan independen dijalankan setelah assignment dan sebelum
split dinyatakan valid:

| Check | Hasil | Detail |
| --- | --- | --- |
| `assignment_coverage` | PASS | missing=0, unexpected=0, invalid_split_names=0 |
| `non_empty_splits` | PASS | train=356, validation=76, test=76 |
| `duplicate_component_leakage` | PASS | leaked_keys=0 |
| `url_group_leakage` | PASS | leaked_keys=0 |
| `exact_duplicate_leakage` | PASS | leaked_keys=0 |
| `near_duplicate_leakage` | PASS | leaked_pairs=0 |

Status `passed=true` hanya diberikan setelah keenam check lulus.
Validation set dan test set belum dipakai untuk tuning atau pemilihan
model karena training tidak dijalankan.

## 9. Unit test yang dijalankan

Fixture sepenuhnya sintetis dan dibuat di direktori sementara saat test;
tidak ada raw dataset yang di-commit.

| File test | Fokus | Jumlah |
| --- | --- | ---: |
| `ml/tests/test_loader_validation.py` | CP1252, delimiter, label mapping, label invalid, byte invalid, teks kosong, duplicate, baseline | 5 |
| `ml/tests/test_dedup.py` | URL grouping, near-duplicate, transitive components, label conflict, report safety | 5 |
| `ml/tests/test_preprocessing.py` | Unicode/HTML/URL/whitespace, lowercase opsional, tokenisasi opsional, tanpa stemming/stopword | 4 |
| `ml/tests/test_split.py` | group-aware split, deteksi leakage, reprodusibilitas, eksklusi karantina | 4 |
| `ml/tests/test_workbook.py` | mapping urutan baris, audit voting, manifest check | 2 |

Perintah dan hasil aktual:

```text
python -m unittest discover -s ml/tests -v
Ran 20 tests ... OK

python -m compileall -q ml/src ml/scripts ml/tests
compileall: OK

python ml/scripts/run_stage3_pipeline.py --csv "<csv 600>" --workbook "<workbook 600>" --output-dir ml/data/processed
validation: passed=True records=600 labels={'Hoax': 228, 'Valid': 372}
dedup: url_groups=31 near_pairs=332 conflict_records=92
split: records={'test': 76, 'train': 356, 'validation': 76} leakage_checks=6/6 passed
```

Tidak ada dependency baru; seluruh Stage 3 memakai Python standard library.
Belum ada konfigurasi lint/type-check di repository, jadi hanya unittest
dan compileall yang dijalankan.

## 10. Keterbatasan yang tersisa

- Dataset tetap **conditionally approved**. Hak sumber berita pihak ketiga
  dan penggunaan komersial memerlukan review hukum.
- Pemetaan CSV↔workbook adalah inferensi urutan baris, bukan relasi resmi;
  URL group turut dipakai untuk grouping hanya sebagai audit grouping.
- Pilihan threshold near-duplicate (5-word/Jaccard ≥ 0.5) adalah heuristik
  yang direproduksi dari Stage 2, bukan bukti bahwa dua teks identik
  secara faktual.
- 29 komponen/92 record dikarantina karena konflik label. Kebijakan final
  untuk memasukkan kembali, memilih label, atau membuang record belum
  ditentukan pemilik.
- CSV tidak memiliki URL, sumber, topik, timestamp, atau ID resmi. Analisis
  tren temporal tidak didukung.
- Preprocessing default sengaja konservatif; dampak lowercase, tokenisasi,
  atau HTML handling terhadap performa model belum diuji.
- Split valid hanya untuk kombinasi hash dataset, config dedup, config
  split, dan seed yang tercatat. Perubahan salah satu harus mengulang
  seluruh pipeline dan leakage check.
- Belum ada training, evaluasi Macro F1, confusion matrix, atau analisis
  sensitivitas terhadap record karantina.
- Prediksi model kelak bukan verifikasi fakta dan tidak boleh ditampilkan
  sebagai bukti kebenaran suatu klaim.

## Lampiran A --- Ukuran semua komponen multi-record

Format: `component_id(size)`. Singleton tidak dicantumkan di sini; jumlahnya
338 dan tercatat di laporan JSON.

```text
dup-r0002(4), dup-r0003(2), dup-r0007(2), dup-r0010(2), dup-r0014(2),
dup-r0016(2), dup-r0020(2), dup-r0021(2), dup-r0022(3), dup-r0030(2),
dup-r0036(2), dup-r0054(2), dup-r0062(3), dup-r0066(2), dup-r0073(4),
dup-r0079(2), dup-r0081(2), dup-r0083(2), dup-r0102(3), dup-r0105(2),
dup-r0106(2), dup-r0111(2), dup-r0115(3), dup-r0124(2), dup-r0152(2),
dup-r0154(3), dup-r0155(3), dup-r0156(2), dup-r0158(2), dup-r0160(5),
dup-r0164(2), dup-r0167(2), dup-r0171(3), dup-r0174(2), dup-r0192(3),
dup-r0202(7), dup-r0204(2), dup-r0211(2), dup-r0215(3), dup-r0217(4),
dup-r0219(2), dup-r0220(2), dup-r0224(2), dup-r0225(4), dup-r0234(4),
dup-r0246(2), dup-r0253(4), dup-r0254(2), dup-r0257(2), dup-r0258(3),
dup-r0260(2), dup-r0265(2), dup-r0266(2), dup-r0267(2), dup-r0270(2),
dup-r0272(2), dup-r0274(3), dup-r0287(4), dup-r0307(2), dup-r0319(2),
dup-r0320(2), dup-r0352(4), dup-r0353(2), dup-r0354(2), dup-r0355(2),
dup-r0356(2), dup-r0368(3), dup-r0370(2), dup-r0372(2), dup-r0374(2),
dup-r0403(5), dup-r0406(3), dup-r0408(2), dup-r0417(2), dup-r0430(2),
dup-r0436(2), dup-r0437(2), dup-r0453(8), dup-r0455(2), dup-r0460(2),
dup-r0461(3), dup-r0462(6), dup-r0473(2), dup-r0485(2), dup-r0502(3),
dup-r0505(5), dup-r0508(6), dup-r0510(2), dup-r0538(2), dup-r0553(2),
dup-r0559(2), dup-r0564(16), dup-r0565(5)
```

## Lampiran B --- Komponen dengan konflik label

29 komponen berikut memuat lebih dari satu `target_label`; seluruh
anggotanya dikarantina (total 92 record):

```text
dup-r0002(4), dup-r0003(2), dup-r0007(2), dup-r0014(2), dup-r0020(2),
dup-r0021(2), dup-r0036(2), dup-r0073(4), dup-r0081(2), dup-r0083(2),
dup-r0102(3), dup-r0106(2), dup-r0115(3), dup-r0160(5), dup-r0164(2),
dup-r0171(3), dup-r0174(2), dup-r0253(4), dup-r0258(3), dup-r0274(3),
dup-r0352(4), dup-r0353(2), dup-r0368(3), dup-r0370(2), dup-r0453(8),
dup-r0462(6), dup-r0505(5), dup-r0508(6), dup-r0510(2)
```
