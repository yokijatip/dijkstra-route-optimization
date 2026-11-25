# Pemeriksaan draf skripsi Zia Ulhaq

Sumber: `(Draft) Skripsi Zia Ulhaq.docx` pada folder OneDrive yang ditunjuk pengguna. Pemeriksaan dilakukan pada 18 September 2026 terhadap teks, tabel, dan struktur XML dokumen. Berkas asli tidak diubah.

## Hasil utama

BAB I–VI sudah terisi. Tabel hasil BAB V dan kesimpulan BAB VI sesuai dengan arsip eksperimen: 10 pasangan, tiga pengulangan per algoritma, 60 hasil terukur, waktu rata-rata 78.697,65 ms dan 25,88 ms. Cakupan graf 27.172 simpul dan 61.630 sisi juga konsisten pada BAB III–VI. Penggunaan memori dan belum terverifikasinya Firestore telah dijelaskan secara tepat pada BAB V.

Dokumen belum siap dianggap final karena masih terdapat perbedaan antara rencana penelitian dan pelaksanaan, bagian awal yang belum diisi, serta daftar otomatis yang belum diperbarui.

## Perbaikan substansi yang diprioritaskan

| Lokasi | Temuan | Perbaikan |
|---|---|---|
| 1.1 paragraf terakhir; 1.2 butir pertama; pengantar 1.5; 2.1.1; 2.11; relevansi beberapa baris Tabel 2.1 | Masih menyebut Kabupaten Bandung untuk penelitian ini | Ganti menjadi Kota Bandung. Jangan mengganti nama wilayah atau judul yang memang milik penelitian terdahulu. |
| 1.1, 1.3, dan 1.7.1 | Menjanjikan beberapa ukuran graf atau variasi ukuran graf | Pelaksanaan kinerja hanya memakai satu graf Kota Bandung. Jelaskan bahwa dataset demo digunakan untuk uji fungsi; variasi ukuran graf belum diuji. Jika tetap dipertahankan sebagai rencana, nyatakan penyimpangan pelaksanaannya secara eksplisit di BAB V. |
| 1.7.1 bagian Perancangan Eksperimen; 2.6.5; 3.6.2 | Menyebut urutan bergantian atau acak | Pelaksanaan menggunakan urutan tetap standar kemudian optimasi. Selaraskan deskripsi pelaksanaan dan tetap akui potensi bias urutan. Pengacakan pasangan titik tidak sama dengan pengacakan urutan algoritma. |
| 1.1, 1.4, 1.5.1, 1.6.1, 1.7.1, 2.5.1, dan 2.11 | Adjacency list terkesan sebagai perlakuan khusus optimasi | Kedua implementasi menggunakan adjacency list yang sama. Perlakuan yang dibandingkan adalah pemilihan minimum linear versus min-heap dan perbedaan penghentian pencarian. |
| 2.10.2 | Daftar kasus menyebut sisi berbobot nol dan beberapa jalur minimum yang sama | Belum terdapat bukti kasus tersebut pada sembilan tes backend yang diarsipkan. Nyatakan sebagai cakupan yang direncanakan atau tambahkan pengujian nyata sebelum mengklaim sudah diuji. |
| 2.2.4 | Contoh A–B–C merujuk Tabel 2.2 | Tabel 2.2 berisi komponen pemodelan jaringan jalan, bukan bobot A–B–C. Tulis contoh sebagai ilustrasi mandiri dengan bobot A–B=4, B–C=2, A–C=7 atau tambahkan tabel ilustrasi tersendiri. |

### Contoh redaksi untuk menyelaraskan metode

**Rumusan masalah (1.4):**

Berdasarkan latar belakang, identifikasi masalah, dan batasan masalah yang telah diuraikan, rumusan masalah dalam penelitian ini adalah bagaimana menerapkan optimasi algoritma Dijkstra menggunakan antrean prioritas berbasis min-heap dan penghentian dini pada sistem navigasi cerdas berbasis web untuk jaringan jalan Kota Bandung, serta bagaimana perbandingan kinerjanya terhadap implementasi standar dengan pencarian minimum linear berdasarkan waktu eksekusi, jumlah simpul yang diproses, dan jumlah sisi yang diperiksa, dengan kedua implementasi menggunakan adjacency list yang sama dan tetap menghasilkan jalur valid dengan total bobot terpendek yang ekuivalen?

**Cakupan eksperimen yang benar-benar dilaksanakan:**

Pengujian kinerja menggunakan satu graf jaringan jalan Kota Bandung dengan 10 pasangan titik asal–tujuan yang dipilih secara acak menggunakan seed 42. Setiap pasangan dijalankan dengan satu pemanasan dan tiga pengulangan terukur untuk setiap algoritma. Dataset demo digunakan untuk pengujian fungsional dan tidak digabungkan ke dalam statistik kinerja Kota Bandung. Pengujian variasi ukuran graf belum dilakukan.

**Urutan pelaksanaan:**

Pada setiap pengulangan, Dijkstra standar dijalankan terlebih dahulu, kemudian Dijkstra optimasi. Urutan tersebut tidak diacak atau diseimbangkan. Oleh karena itu, potensi pengaruh urutan eksekusi, cache, serta beban sistem diperlakukan sebagai keterbatasan pengujian.

## Kelengkapan dan konsistensi penulisan

1. Sampul masih bertahun 2025, sedangkan jadwal penelitian sudah Juni–Oktober 2026 dan pengujian pada 17 September 2026. Tetapkan tahun sampul sesuai tahun pengajuan sebenarnya. Jangan mengubah tahun artikel ilmiah atau nomor SK akreditasi hanya karena memuat angka 2025.
2. Judul sampul dan pernyataan keaslian menggunakan ejaan `DJIKSTRA`. Ejaan algoritma yang benar adalah `DIJKSTRA`. Caption Gambar 4.4 juga memakai `Djikstra`. Untuk judul artikel di daftar pustaka, ikuti ejaan resmi sumber.
3. Abstrak Indonesia, abstract Inggris, kata pengantar, lembar persetujuan, dan lembar pengesahan belum memuat isi substantif. Identitas pembimbing, tanda tangan, dan tanggal pengesahan harus berasal dari informasi sebenarnya.
4. Daftar isi yang tersimpan baru menampilkan judul BAB V dan VI, belum subbabnya. Daftar tabel berhenti pada BAB IV walaupun tujuh tabel BAB V sudah ada. Periksa penggunaan Heading lalu perbarui seluruh daftar otomatis, bukan hanya nomor halaman.
5. Tidak ditemukan bagian Daftar Gambar atau Lampiran pada teks dokumen. Tambahkan daftar gambar dan lampiran bukti pengujian. Daftar Simbol masih berupa judul; isi sesuai simbol yang digunakan atau sesuaikan dengan ketentuan kampus.
6. Caption menggunakan `Table`, sedangkan narasi menggunakan `Tabel`. Seragamkan label dan perbarui daftar tabel. Rapikan `Object Penelitian` menjadi `Objek Penelitian`, `Kebuthan` menjadi `Kebutuhan`, dan `Dijkstra Standa` menjadi `Dijkstra Standar`.
7. Beberapa sitasi menyatu dengan kata, misalnya `(Yovi & Sekarwati, 2024)menerapkan`. Perbaiki spasi serta tanda baca. Backtick Markdown masih muncul pada alamat layanan di BAB V; hilangkan tanda backtick dalam naskah Word.

## Pemeriksaan daftar pustaka

Daftar pustaka sudah tersedia tetapi metadata beberapa sumber belum lengkap. Entri FastAPI, TypeScript, heapq, Nuxt, dan Firestore tidak menampilkan URL pada teks daftar pustaka. Entri Lewis belum mencantumkan tautan atau identitas publikasi. Identitas penulis WAI tampil tidak wajar sebagai `(WAI), W. W. A. I.`. Metadata penulis IBM juga perlu dicocokkan dengan sumber asli.

Judul penelitian Pramestiana dan Anwar berbeda antara tabel penelitian terdahulu (`PT X`) dan daftar pustaka (`PT Pos Logistik Indonesia`). Judul Kurniawan dan Atmojo pada daftar pustaka lebih pendek daripada yang tercantum di tabel. Periksa sumber asli dan gunakan metadata yang konsisten. Jangan menyamakan tahun atau judul berdasarkan dugaan.

Rujukan teori graf sekarang menggunakan Maurer dan Ralston, bukan Liben-Nowell. Keduanya merupakan sumber berbeda, sehingga isi, tahun, halaman, dan DOI perlu diverifikasi terhadap sumber yang benar-benar digunakan. Tahun 2020 juga perlu diperiksa terhadap ketentuan kebaruan rujukan kampus untuk naskah tahun 2026.

Sejumlah subbab teori, khususnya pemodelan diagram dan pengujian perangkat lunak, belum memperlihatkan rujukan yang memadai. Ini belum memenuhi pola tiga rujukan dan simpulan peneliti yang disebut dalam pedoman. Lakukan pemeriksaan sumber per subbab; jangan menambahkan sitasi yang tidak mendukung isi.

Pemeriksaan ini menilai kelengkapan dan konsistensi internal daftar pustaka. Keabsahan metadata dan kesesuaian isi setiap sumber belum diverifikasi ulang melalui situs penerbit.

## Batas pemeriksaan format

Struktur dokumen mencatat ukuran A4 pada ketiga section, dengan margin atas/kiri sekitar 4 cm serta kanan/bawah sekitar 3 cm. Dokumen memuat 27 tabel dan 26 aset gambar. Jumlah aset bukan jumlah gambar bernomor karena dapat mencakup logo atau elemen lainnya.

Pemeriksaan visual halaman belum dapat diselesaikan karena renderer tidak menemukan LibreOffice yang dibundel. Karena itu, laporan ini tidak menyatakan bahwa tata letak, pemenggalan tabel, ukuran gambar, nomor halaman, atau posisi rumus sudah benar. Rumus Word menggunakan elemen matematika khusus; kekosongan simbol pada ekstraksi teks biasa tidak membuktikan rumus hilang dari dokumen.
