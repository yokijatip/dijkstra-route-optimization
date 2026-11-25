## **PRODUCT REQUIREMENTS DOCUMENT** 

**Sistem Navigasi Cerdas Berbasis Web Optimasi Algoritma Dijkstra untuk Penentuan Jalur Terpendek** 

Penelitian: Zia Ulhaq (21110383) _Dokumen spesifikasi produk dan implementasi penelitian_ 

**Versi 1.0  |  Status: Draft Baseline** September 2026 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

# **1. Kontrol Dokumen** 

|**Item**|**Nilai**|
|---|---|
|Nama Produk|Sistem Navigasi Cerdas - Dijkstra Optimization Lab|
|Jenis Dokumen|Product Requirements Document (PRD)|
|Versi|1.0|
|Status|Draft baseline untuk perancangan, implementasi, dan Bab III/Bab IV|
|Basis Proposal|Seminar Proposal: Optimasi Algoritma Dijkstra untuk Penentuan Jalur Terpendek pada Sistem<br>Navigasi Cerdas|
|Platform Target|Web application|
|Frontend Usulan|Nuxt + TypeScript|
|Backend Usulan|Python + FastAPI|
|Penyimpanan Usulan|Firebase Firestore untuk hasil eksperimen/metadata; dataset graf dimuat ke memori backend|



**Status terhadap proposal:** Proposal sumber menyebut implementasi Python/Java pada lingkungan desktop. PRD ini sengaja mengusulkan implementasi berbasis web dengan Python sebagai engine algoritma. Jika arah ini dipakai, bagian Batasan Masalah dan Metode Pengembangan pada proposal perlu diselaraskan. 

# **2. Ringkasan Eksekutif** 

Produk yang akan dibangun adalah **aplikasi web simulasi navigasi dan laboratorium eksperimen algoritma Dijkstra** . Aplikasi tidak dimaksudkan menjadi pengganti Google Maps atau sistem navigasi real-time. Fungsi utamanya adalah memvisualisasikan pencarian jalur terpendek dan menghasilkan bukti kuantitatif perbandingan kinerja Dijkstra standar terhadap Dijkstra yang dioptimasi pada graf simulasi jaringan jalan. 

**Nilai penelitian utama:** jalur terpendek yang dihasilkan kedua implementasi harus tetap valid/ekuivalen dari sisi total bobot, sementara versi optimasi diharapkan mengurangi waktu eksekusi dan/atau ruang pencarian seperti jumlah node yang dikunjungi dan edge yang diproses. 

# **3. Latar Produk dan Problem Statement** 

### **3.1 Masalah penelitian** 

- Dijkstra akurat untuk graf berbobot non-negatif, tetapi dapat menjadi kurang efisien ketika ukuran dan kompleksitas graf meningkat. 

- Penelitian membutuhkan mekanisme objektif untuk membandingkan Dijkstra standar dan versi optimasi pada dataset serta skenario yang identik. 

- Hasil eksperimen perlu dapat ditinjau secara visual dan numerik agar dapat digunakan sebagai bukti pada Bab IV. 

- Aplikasi harus memisahkan waktu komputasi algoritma dari latensi jaringan/database agar benchmark tidak bias. 

### **3.2 Rumusan produk** 

**Bagaimana membangun aplikasi berbasis web yang dapat:** memodelkan jaringan jalan sebagai graf berbobot, menjalankan Dijkstra standar dan Dijkstra optimasi pada input yang sama, memvisualisasikan jalur, 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

mengukur performa algoritma, menyimpan hasil eksperimen, dan menyajikan perbandingan yang dapat digunakan untuk analisis penelitian? 

# **4. Visi Produk, Tujuan, dan Non-Tujuan** 

### **4.1 Product vision** 

_“Satu aplikasi web yang berfungsi sekaligus sebagai simulator navigasi, visualizer graf, dan benchmarking lab untuk membuktikan dampak optimasi Dijkstra secara terukur.”_ 

### **4.2 Tujuan utama** 

1. Mengimplementasikan Dijkstra standar sebagai baseline eksperimen. 

2. Mengimplementasikan Dijkstra optimasi tanpa mengubah tujuan utama algoritma, yaitu shortest path pada bobot non-negatif. 

3. Memungkinkan pengguna memilih titik awal dan titik tujuan pada graf simulasi. 

4. Memvisualisasikan shortest path dan node yang dieksplorasi. 

5. Menghasilkan metrik performa yang dapat direplikasi dan dibandingkan. 

6. Menyediakan mode batch benchmark untuk berbagai ukuran graf dan banyak pasangan source-destination. 

7. Menyimpan serta mengekspor hasil eksperimen untuk keperluan analisis skripsi. 

### **4.3 Non-goals** 

- Tidak menyediakan kondisi lalu lintas real-time. 

- Tidak menggunakan Google Maps Directions API sebagai sumber hasil shortest path. 

- Tidak melakukan navigasi turn-by-turn berbasis GPS. 

- Tidak memproses bobot negatif. 

- Tidak membandingkan Dijkstra terhadap algoritma berbeda sebagai fokus utama penelitian, kecuali kemudian disetujui sebagai pengembangan tambahan. 

- Tidak menjadikan performa query database atau network latency sebagai bagian dari metrik waktu eksekusi algoritma. 

# **5. Metrik Keberhasilan** 

|**Kategori**|**Metrik**|**Kriteria Keberhasilan**|
|---|---|---|
|Correctness|Kesetaraan shortest-path<br>cost|Total bobot hasil Dijkstra standar dan versi optimasi harus sama untuk setiap<br>kasus valid, kecuali terdapat beberapa shortest path ekuivalen.|
|Performance|Execution time|Sistem mengukur waktu komputasi algoritma secara terisolasi dan menyajikan<br>nilai per-run serta agregat.|
|Search efficiency|Visited nodes|Jumlah node yang dikeluarkan/diproses dari frontier tercatat untuk masing-<br>masing algoritma.|
|Search efficiency|Processed/relaxed edges|Jumlah edge yang dievaluasi/relaksasi tercatat.|
|Experiment|Repeatability|Konfigurasi dataset, source, destination, algorithm version, dan run metadata<br>dapat ditelusuri.|
|Usability|Demo workflow|Pengguna dapat memilih source-destination dan memperoleh visualisasi +<br>metrik dalam satu alur.|
|Research output|Export|Hasil benchmark dapat diekspor sekurang-kurangnya ke CSV.|



PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

**Catatan:** PRD tidak menetapkan target “X% lebih cepat” sebelum eksperimen dijalankan. Besarnya peningkatan merupakan hasil penelitian, bukan requirement yang boleh dipaksakan. 

# **6. Pengguna dan Persona** 

|**Persona**|**Kebutuhan Utama**|**Hak/Aktivitas**|
|---|---|---|
|Peneliti/Admin|Menyiapkan dataset, menjalankan eksperimen, melihat<br>metrik, mengekspor data.|Kelola dataset, run single test, batch<br>benchmark, lihat riwayat, export.|
|Dosen/Penguji|Memahami cara kerja sistem dan melihat bukti<br>perbandingan secara cepat.|Pilih rute, lihat visualisasi, lihat tabel/chart<br>comparison.|
|Viewer/Demo User|Mencoba simulasi shortest path tanpa mengubah dataset.|Pilih node awal/tujuan dan menjalankan<br>pencarian.|



# **7. Scope Produk** 

### **7.1 P0 - Wajib untuk skripsi** 

- Dataset graf berbobot non-negatif dan mekanisme loading dataset. 

- Dijkstra standar (baseline). 

- Dijkstra optimasi (minimum: priority queue/min-heap + early termination; strategi final harus dikunci sebelum Bab III final). 

- Input source dan destination. 

- Visualisasi graph/map beserta shortest path. 

- Single-run comparison: standard vs optimized. 

- Metrik execution time, visited nodes, processed edges, total distance/cost, path length. 

- Batch benchmark pada banyak source-destination. 

- Statistik agregat hasil benchmark. 

- Riwayat eksperimen dan export CSV. 

- Validasi correctness hasil dua implementasi. 

### **7.2 P1 - Disarankan** 

- Preset dataset Small/Medium/Large untuk demonstrasi skalabilitas. 

- Visualisasi visited nodes/frontier secara bertahap. 

- Chart perbandingan execution time dan visited nodes. 

- Filter riwayat eksperimen berdasarkan dataset, tanggal, source, destination, dan versi algoritma. 

- Seed/randomization yang dapat dikunci untuk batch experiment reproducible. 

### **7.3 P2 - Opsional** 

- Autentikasi admin. 

- Import dataset melalui UI. 

- Export grafik sebagai gambar. 

- Replay animasi langkah Dijkstra. 

- Deployment publik dan mode read-only demo. 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

# **8. User Flow Utama** 

### **8.1 Flow A - Demo navigasi** 

1. Pengguna membuka halaman Navigasi. 

2. Sistem memuat dataset aktif. 

3. Pengguna memilih source dan destination. 

4. Pengguna memilih mode Standard, Optimized, atau Compare. 

5. Backend menjalankan algoritma pada graph di memori. 

6. Frontend menampilkan jalur, total bobot, metrik, serta highlight pada visualisasi. 

7. Pada mode Compare, sistem menampilkan hasil berdampingan dan persentase perbedaan metrik. 

### **8.2 Flow B - Batch benchmark** 

1. Peneliti memilih dataset. 

2. Peneliti menetapkan jumlah pasangan source-destination, mode pasangan (preset/random), warm-up, dan jumlah repeat. 

3. Sistem membuat/menetapkan test cases. 

4. Backend menjalankan Standard dan Optimized pada test cases yang identik. 

5. Setiap run mencatat metrik mentah. 

6. Sistem menghitung statistik agregat. 

7. Sistem melakukan correctness check. 

8. Hasil benchmark disimpan dan dapat diekspor ke CSV. 

# **9. Functional Requirements** 

|**ID**|**Priority**|**Area**|**Requirement**|
|---|---|---|---|
|FR-001|P0|Dataset|Sistem dapat memuat satu dataset graf aktif dari file/penyimpanan yang telah divalidasi.|
|FR-002|P0|Dataset|Setiap node memiliki id unik; edge memiliki from, to, dan weight >= 0.|
|FR-003|P0|Dataset|Sistem menolak edge dengan bobot negatif.|
|FR-004|P0|Navigation|Pengguna dapat memilih source dan destination dari node yang tersedia.|
|FR-005|P0|Algorithm|Backend menyediakan implementasi Dijkstra standar sebagai baseline.|
|FR-006|P0|Algorithm|Backend menyediakan implementasi Dijkstra optimasi yang terdokumentasi versinya.|
|FR-007|P0|Algorithm|Kedua algoritma menerima dataset dan pasangan source-destination yang identik.|
|FR-008|P0|Result|Sistem mengembalikan path, total cost/distance, execution time, visited nodes, processed<br>edges, dan status.|
|FR-009|P0|Result|Sistem mendeteksi kondisi no-path/unreachable.|
|FR-010|P0|Compare|Mode compare menjalankan kedua algoritma dan menampilkan metrik berdampingan.|
|FR-011|P0|Validation|Sistem menandai mismatch apabila shortest-path cost standard dan optimized tidak ekuivalen.|
|FR-012|P0|Visualization|Shortest path ditandai berbeda dari node/edge lain pada visualisasi.|
|FR-013|P1|Visualization|Sistem dapat menampilkan node yang dikunjungi selama pencarian.|
|FR-014|P0|Benchmark|Pengguna dapat menjalankan batch benchmark dengan beberapa test case.|
|FR-015|P0|Benchmark|Batch benchmark menguji dua algoritma pada test case yang sama.|



PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

|**ID**|**Priority**|**Area**|**Requirement**|
|---|---|---|---|
|FR-016|P0|Benchmark|Sistem menyimpan hasil raw tiap run sebelum membuat agregasi.|
|FR-017|P0|Benchmark|Sistem menghitung mean, median, minimum, maksimum, dan standard deviation execution<br>time.|
|FR-018|P0|Benchmark|Sistem menghitung rata-rata visited nodes dan processed edges.|
|FR-019|P0|History|Sistem menyediakan daftar eksperimen terdahulu.|
|FR-020|P0|Export|Hasil eksperimen dapat diunduh sebagai CSV.|
|FR-021|P1|Reproducibility|Batch random dapat menyimpan random seed.|
|FR-022|P1|Versioning|Setiap hasil mencatat algorithmVersion dan datasetVersion.|



# **10. Spesifikasi Algoritma** 

### **10.1 Baseline: Dijkstra standar** 

Baseline harus menjadi implementasi yang benar secara algoritmik dan cukup “standar” untuk dijelaskan dalam Bab III. Hindari membuat baseline sengaja buruk hanya agar versi optimasi terlihat lebih cepat. 

- Input: graph G=(V,E), source s, destination t. 

- Constraint: weight setiap edge >= 0. 

- Output: shortest path s→t jika tersedia, total cost, dan metrik instrumentasi. 

- Metrik tidak boleh mengubah correctness algoritma. 

### **10.2 Kandidat optimasi** 

|**Teknik**|**Status PRD**|**Tujuan**|
|---|---|---|
|Adjacency list|Direkomendasikan P0|Menghindari representasi yang boros pada graph sparse.|
|Priority queue / min-heap|Direkomendasikan P0|Mengambil node dengan tentative distance terkecil secara efisien.|
|Early termination|Direkomendasikan P0|Menghentikan proses saat destination telah memperoleh jarak<br>final.|
|Bidirectional Dijkstra|Kandidat P1 / opsi utama optimasi<br>lanjutan|Menjalankan pencarian dari source dan destination dan bertemu<br>di tengah.|
|Pruning/filtering node|Eksperimental; wajib didefinisikan jika<br>dipakai|Mengurangi search space tanpa mengorbankan optimality.|
|Heuristik|Tidak otomatis P0|Berisiko menggeser metode ke arah A* bila heuristik<br>memengaruhi prioritas; harus disetujui secara akademik sebelum<br>dipakai.|



**Keputusan yang perlu dikunci:** Istilah “Dijkstra optimasi” harus memiliki definisi implementasi yang tegas sebelum coding final. Rekomendasi aman: Standard Dijkstra vs Optimized Dijkstra berbasis adjacency list + min-heap + early termination, kemudian bidirectional Dijkstra dapat menjadi optimasi tambahan bila scope dan landasan teori mendukung. 

# **11. Definisi Metrik Penelitian** 

**Metrik** 

**Definisi Operasional** 

**Satuan/Output** 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

|**Metrik**|**Definisi Operasional**|**Satuan/Output**|
|---|---|---|
|Execution Time|Durasi hanya untuk fungsi pencarian shortest path setelah graph telah tersedia di<br>memori; tidak termasuk HTTP, render UI, Firestore, atau loading dataset.|ms atau µs|
|Visited Nodes|Jumlah node yang benar-benar diambil/diproses dari frontier sesuai definisi<br>implementasi. Definisi harus sama untuk dua algoritma.|count|
|Processed Edges|Jumlah edge yang diperiksa/dirileksasi selama pencarian.|count|
|Shortest Path Cost|Jumlah bobot edge sepanjang path hasil.|unit weight / km bila<br>bobot merepresentasikan<br>jarak|
|Path Length|Jumlah edge atau node pada path; definisi harus eksplisit.|count|
|Improvement %|(baseline - optimized) / baseline × 100% untuk metrik yang lebih kecil lebih baik.|%|
|Correctness Match|Apakah cost baseline dan optimized sama dalam toleransi numerik yang<br>ditentukan.|boolean|



# **12. Desain Eksperimen** 

### **12.1 Unit eksperimen** 

Satu unit eksperimen adalah satu pasangan (dataset, source, destination) yang dieksekusi menggunakan Dijkstra standar dan Dijkstra optimasi pada kondisi input yang sama. 

### **12.2 Dataset** 

Proposal menyebut simulasi jaringan jalan wilayah Kota Bandung. PRD mempertahankan framing tersebut. Detail sumber data, jumlah node, jumlah edge, dan proses pembentukan graph belum dijelaskan dalam Bab I sehingga harus ditetapkan pada tahap desain data/Bab III. 

|**Preset**|**Target Contoh**|**Keterangan**|
|---|---|---|
|Small|~100 node|Validasi fungsional dan demo cepat.|
|Medium|~500 node|Eksperimen menengah.|
|Large|~1.000 node|Uji skalabilitas.|
|X-Large|~5.000 node|Uji performa lanjutan jika dataset tersedia.|
|Huge|~10.000 node|Opsional; hanya jika masuk akal terhadap data dan environment.|



**Bukan angka proposal:** Ukuran preset di atas adalah rancangan produk untuk benchmarking, bukan fakta yang disebutkan di Bab I. Jumlah final harus disesuaikan dengan dataset yang benar-benar dibentuk. 

### **12.3 Prosedur benchmark** 

1. Load dan validasi graph sebelum timer dimulai. 

2. Gunakan test case yang sama untuk Standard dan Optimized. 

3. Lakukan warm-up run bila runtime/lingkungan memerlukannya; warm-up tidak dimasukkan ke data utama. 

4. Lakukan repeat per test case untuk mengurangi noise timing. 

5. Simpan raw timing, bukan hanya rata-rata. 

6. Gunakan timer monotonic/high-resolution pada backend. 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

7. Jalankan correctness check untuk setiap pasangan. 

8. Catat environment minimal: versi aplikasi, versi algoritma, dataset version, runtime/backend version. 

### **12.4 Output analisis** 

- Tabel per-run dan per-dataset. 

- Mean/median/min/max/std execution time. 

- Rata-rata visited nodes dan processed edges. 

- Improvement percentage per metrik. 

- Grafik trend terhadap ukuran graph. 

- Daftar correctness mismatch (target: 0 untuk test case valid). 

# **13. Arsitektur Sistem dan Tech Stack** 

### **13.1 Arsitektur logis** 

[Browser / Nuxt] 

- |-- Navigation UI 

- |-- Graph/Map Visualization 

- |-- Comparison Dashboard 

|-- Benchmark Dashboard 

- |-- Experiment History 

| | HTTP/JSON v [Python FastAPI] 

- |-- Dataset Service 

|-- Standard Dijkstra Engine 

|-- Optimized Dijkstra Engine 

|-- Benchmark Runner 

- |-- Metrics / Correctness Validator 

| 

+--> [In-memory Graph] | +--> [Firestore: experiment metadata/results] +--> [CSV export] 

### **13.2 Tech stack yang direkomendasikan** 

|**Layer**|**Teknologi**|**Alasan**|
|---|---|---|
|Frontend|Nuxt + TypeScript|UI modern, routing, component architecture, cocok untuk dashboard<br>penelitian.|
|UI Styling|Tailwind CSS|Cepat untuk membangun layout dashboard konsisten.|
|Graph/Map|Leaflet atau library graph yang sesuai<br>dataset|Untuk visualisasi lokasi/edge; pilihan final bergantung apakah dataset<br>memiliki koordinat geografis.|
|Backend API|Python + FastAPI|Mempertahankan Python untuk engine algoritma dan memisahkan<br>benchmark dari browser/network.|
|Algorithm|Python standard library (heapq) +<br>implementasi sendiri|Metrik dan logika optimasi lebih mudah dikontrol dan dijelaskan.|
|Database|Firebase Firestore|Menyimpan metadata eksperimen, konfigurasi, dan hasil; bukan hot<br>path algoritma.|
|Dataset runtime|JSON/CSV/parquet → in-memory<br>adjacency list|Benchmark tidak tercampur latency database.|



PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

|**Layer**|**Teknologi**|**Alasan**|
|---|---|---|
|Export|CSV|Mudah dianalisis di spreadsheet/statistical tools dan dimasukkan ke Bab<br>IV.|



# **14. Model Data** 

### **14.1 Graph node** 

Node { id: string name: string latitude?: number longitude?: number } 

### **14.2 Graph edge** 

Edge { from: string to: string weight: number       // wajib >= 0 bidirectional?: bool } 

### **14.3 Experiment result** 

ExperimentRun { id: string experimentId: string datasetId: string datasetVersion: string sourceId: string destinationId: string algorithm: "standard" | "optimized" algorithmVersion: string executionTimeNs: integer visitedNodes: integer processedEdges: integer totalCost: number | null path: string[] status: "success" | "unreachable" | "error" createdAt: timestamp } 

### **14.4 Benchmark summary** 

BenchmarkSummary { experimentId: string testCaseCount: integer repeatCount: integer randomSeed?: integer correctnessMismatchCount: integer standard: AggregateMetrics optimized: AggregateMetrics improvement: { 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

executionTimePct: number visitedNodesPct: number processedEdgesPct: number } } 

# **15. API Contract Tingkat Tinggi** 

|**Method**|**Endpoint**|**Tujuan**|
|---|---|---|
|GET|/api/datasets|Daftar dataset tersedia.|
|GET|/api/datasets/{id}|Metadata dan node/edge atau endpoint visualisasi dataset.|
|POST|/api/routes/standard|Menjalankan Dijkstra standar untuk satu source-destination.|
|POST|/api/routes/optimized|Menjalankan Dijkstra optimasi.|
|POST|/api/routes/compare|Menjalankan keduanya dan mengembalikan comparison.|
|POST|/api/benchmarks|Membuat dan menjalankan batch benchmark.|
|GET|/api/benchmarks/{id}|Mengambil hasil benchmark dan agregasi.|
|GET|/api/experiments|Daftar eksperimen/riwayat.|
|GET|/api/experiments/{id}/export.csv|Export hasil mentah/agregat.|



# **16. Struktur Halaman dan UI Requirements** 

|**Halaman**|**Komponen Utama**|**Output**|
|---|---|---|
|Dashboard|Summary cards, recent experiments, quick benchmark stats.|Ringkasan status penelitian.|
|Navigation Simulator|Source selector, destination selector, mode algorithm, Run button,<br>graph/map.|Path dan metrik single run.|
|Comparison|Standard vs Optimized cards, metric table, improvement indicators.|Perbandingan satu kasus.|
|Benchmark Lab|Dataset selector, test count, repeat, seed, Run Benchmark.|Progress + agregat benchmark.|
|Benchmark Detail|Charts, tables, mismatch list, metadata.|Bahan analisis Bab IV.|
|Experiment History|Filter, sort, view detail, export.|Audit trail eksperimen.|
|Dataset Detail|Node/edge count, version, validation status, preview graph.|Transparansi input penelitian.|



# **17. Acceptance Criteria Kritis** 

|**ID**|**Acceptance Criteria**|
|---|---|
|AC-01|Ketika graph valid dan path tersedia, Standard mengembalikan path dan cost yang benar.|
|AC-02|Optimized menghasilkan shortest-path cost yang ekuivalen dengan Standard pada seluruh regression test valid.|
|AC-03|Timer algoritma tidak mencakup loading dataset, HTTP latency, Firestore, atau render UI.|
|AC-04|Mode Compare menggunakan dataset/version/source/destination yang identik.|



PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

|**ID**|**Acceptance Criteria**|
|---|---|
|AC-05|Visited nodes dan processed edges memiliki definisi yang sama dan tercatat untuk kedua implementasi.|
|AC-06|Kasus source == destination menghasilkan cost 0 dan path yang valid.|
|AC-07|Kasus unreachable menghasilkan status unreachable tanpa crash.|
|AC-08|Negative weight ditolak pada tahap validasi dataset.|
|AC-09|Batch benchmark menyimpan raw run results dan agregat.|
|AC-10|Jika cost Standard dan Optimized berbeda di luar tolerance, benchmark ditandai mismatch.|
|AC-11|Hasil eksperimen dapat diekspor ke CSV dengan field yang cukup untuk reproduksi.|
|AC-12|UI dapat mendemokan satu rute dan perbandingan tanpa akses ke API navigasi real-time pihak ketiga.|



# **18. Non-Functional Requirements** 

|**ID**|**Kategori**|**Requirement**|
|---|---|---|
|NFR-001|Correctness|Tidak ada optimasi yang boleh mengorbankan optimality shortest path pada graph yang<br>memenuhi constraint.|
|NFR-002|Reproducibility|Eksperimen menyimpan konfigurasi, dataset version, algorithm version, dan optional random seed.|
|NFR-003|Performance isolation|Graph harus tersedia di memori sebelum timer algoritma dimulai.|
|NFR-004|Reliability|Error satu test case tidak boleh menghilangkan hasil test case lain dalam batch; status error<br>tercatat.|
|NFR-005|Observability|Backend mencatat error dan metadata run tanpa mencampurkan logging berat ke interval<br>benchmark bila dapat memengaruhi hasil.|
|NFR-006|Maintainability|Standard dan Optimized dipisahkan dalam module yang jelas dan memiliki interface result yang<br>konsisten.|
|NFR-007|Security|Jika deployment publik memiliki admin write action, endpoint write perlu autentikasi/otorisasi.|
|NFR-008|Compatibility|UI desktop browser menjadi target utama untuk demo sidang; responsive dasar tetap disediakan.|



# **19. Strategi Pengujian** 

### **19.1 Unit test algoritma** 

- Graph satu node. 

- Source sama dengan destination. 

- Graph sederhana dengan satu shortest path. 

- Graph dengan beberapa shortest path berkost sama. 

- Graph disconnected/unreachable. 

- Graph dengan zero-weight edge (bila diizinkan). 

- Graph dengan negative edge harus gagal validasi. 

- Regression test: cost Standard == cost Optimized. 

### **19.2 Integration test** 

- Nuxt → FastAPI single run. 

- Compare endpoint menghasilkan dua result dengan input identik. 

- Benchmark menyimpan raw result dan summary. 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

- Export CSV sesuai kolom yang disepakati. 

- Firestore failure tidak mengubah timing algoritma yang sudah selesai dan harus ditangani secara terpisah. 

### **19.3 UAT untuk sidang/demo** 

- Pilih dua lokasi dan tampilkan shortest path. 

- Jalankan Compare dan jelaskan mengapa cost harus sama tetapi metrik performa dapat berbeda. 

- Buka satu benchmark besar dan tunjukkan grafik/tabel agregat. 

- Tunjukkan hasil ekspor sebagai dasar pengolahan Bab IV. 

# **20. Milestone Implementasi** 

|**Milestone**||**Deliverable**|**Exit Criteria**|
|---|---|---|---|
|M1 - Research Design<br>Freeze|Definisi ba<br>format.|seline, optimized algorithm, metric, dataset|Tidak ada ambiguitas istilah “optimasi”; acceptance<br>criteria algoritma disetujui.|
|M2 - Algorithm Engine|Standard +|Optimized + unit test + metrics.|Cost match pada regression test; metrik keluar<br>konsisten.|
|M3 - Dataset & API|Dataset lo|ader, validation, FastAPI endpoints.|Single route dapat dipanggil via API tanpa database di<br>hot path.|
|M4 - Web Simulator|Nuxt navig|ation UI + visualization + comparison.|Demo source→destination end-to-end berhasil.|
|M5 - Benchmark Lab|Batch runn|er, history, aggregate stats, CSV export.|Eksperimen dapat direplikasi dan diekspor.|
|M6 - Research Run|Run ekspe|rimen final dan freeze hasil.|Dataset/versi algoritma dikunci; seluruh raw data<br>tersedia.|
|M7 - Thesis Integration|Tabel/grafi|k dan penjelasan metodologi.|Output sistem dapat langsung dipakai untuk Bab III/Bab<br>IV.|
|**21. Risiko dan**<br>**Risiko**|**Mitiga **|**si**<br>**Dampak**|**Mitigasi**|
|Definisi “Dijkstra optimasi” t|idak jelas|Bab III dan hasil eksperimen sulit<br>dipertanggungjawabkan.|Freeze teknik optimasi sebelum implementasi final;<br>dokumentasikan pseudo-code dan kompleksitas.|
|Baseline sengaja terlalu lam|bat|Perbandingan tidak fair.|Gunakan baseline yang benar dan wajar; jelaskan<br>struktur datanya.|
|Benchmark tercampur<br>network/Firestore||Data waktu tidak merepresentasikan<br>algoritma.|Timer hanya mengelilingi fungsi algoritma pada graph<br>di memori.|
|Dataset terlalu kecil||Perbedaan performa sulit terlihat.|Gunakan beberapa skala data dan cukup banyak test<br>case.|
|Optimized menghasilkan co<br>berbeda|st|Correctness penelitian gagal.|Automated regression/correctness check wajib pada<br>setiap benchmark.|
|Bidirectional/pruning salah<br>implementasi||Optimality dapat rusak.|Unit test, cross-check baseline, dan gunakan definisi<br>termination condition yang benar.|
|Proposal dan implementasi<br>konsisten|tidak|Masalah saat bimbingan/sidang.|Revisi bagian desktop/Python-Java dan jadwal yang<br>masih mengandung sisa template.|
|Hasil timing noisy||Kesimpulan lemah.|Repeat runs, simpan raw data, gunakan<br>median/mean dan environment konsisten.|



PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

# **22. Konsistensi dengan Bab I** 

Poin berikut berasal dari proposal dan dipertahankan oleh PRD: 

- Objek utama adalah algoritma Dijkstra untuk shortest path pada graf berbobot non-negatif. 

- Tujuan penelitian mencakup analisis kinerja Dijkstra, implementasi optimasi, dan evaluasi peningkatan efisiensi. 

- Pengujian menggunakan simulasi jaringan jalan, bukan data real-time API peta. 

- Objek/studi kasus diarahkan pada simulasi jaringan jalan Kota Bandung. 

- Metode penelitian adalah kuantitatif eksperimental dengan pengumpulan data seperti execution time dan jumlah node yang dikunjungi. 

- Metode pengembangan sistem yang tertulis pada proposal adalah Waterfall. 

Poin berikut adalah perubahan/usulan PRD dan perlu diselaraskan ke proposal bila dipakai: 

- Platform diubah dari lingkungan desktop menjadi aplikasi web. 

- Python dipertahankan sebagai backend/algorithm engine, sedangkan Nuxt + TypeScript digunakan untuk frontend. 

- Firebase ditambahkan sebagai penyimpanan metadata/hasil eksperimen, bukan sebagai bagian dari hot path algoritma. 

- Metrik processed edges, repeatability metadata, correctness mismatch, dan export CSV ditambahkan sebagai kebutuhan produk/eksperimen. 

- Jadwal proposal mengandung frasa “pengumpulan data awal di apotek” dan “implementasi Linear Regression” yang tidak konsisten dengan topik Dijkstra dan perlu diperbaiki. 

# **23. Definition of Done** 

- Semua P0 functional requirements selesai. 

- Standard dan Optimized lulus automated correctness regression test. 

- Tidak ada negative-weight dataset yang dapat lolos validasi. 

- Single-run compare dapat didemokan melalui web. 

- Batch benchmark menghasilkan raw data, summary, dan CSV. 

- Dataset version dan algorithm version tercatat pada hasil eksperimen. 

- Timing algoritma telah dipastikan tidak mencakup database/network/UI. 

- Eksperimen final dijalankan pada environment yang terdokumentasi. 

- Hasil dapat digunakan untuk menyusun tabel/grafik Bab IV. 

- Bab I/Bab III telah diselaraskan dengan platform dan teknik optimasi yang benar-benar diimplementasikan. 

# **24. Open Decisions Sebelum Coding** 

|**No.**|**Keputusan**|**Rekomendasi Baseline PRD**|
|---|---|---|
|1|Apa definisi final Dijkstra optimasi?|Adjacency list + min-heap + early termination; pertimbangkan bidirectional<br>sebagai optimasi tambahan.|
|2|Dataset berasal dari mana dan bagaimana<br>dibentuk?|Tetapkan sumber, proses cleansing, node/edge definition, dan versioning<br>pada Bab III.|
|3|Bobot edge merepresentasikan apa?|Utamakan jarak untuk konsistensi “jalur terpendek”; bila memakai biaya lain<br>harus dijelaskan.|
|4|Graph directed atau undirected?|Ikuti karakter data jalan; bila simulasi sederhana dapat menggunakan<br>undirected dengan flag eksplisit.|
|5|Library visualisasi?|Leaflet jika node memiliki lat/lng; graph visualization library jika dataset<br>bersifat abstrak.|
|6|Perlukah autentikasi?|Tidak P0. Tambahkan hanya jika deployment publik membutuhkan write<br>protection.|



PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 

|**No.**|**Keputusan**|**Rekomendasi Baseline PRD**|
|---|---|---|
|7|Firestore wajib?|Tidak untuk core penelitian. Gunakan bila riwayat eksperimen ingin<br>persisten/multi-session.|



# **Lampiran A - Contoh Output Compare** 

{ "source": "soreang", "destination": "baleendah", "standard": { "totalCost": 14.21, "executionTimeMs": 8.42, "visitedNodes": 847, "processedEdges": 1421 }, "optimized": { "totalCost": 14.21, "executionTimeMs": 2.16, "visitedNodes": 213, "processedEdges": 378 }, "correctnessMatch": true, "improvement": { "executionTimePct": 74.35, "visitedNodesPct": 74.85 } } 

**Penting: angka di atas hanya contoh format output, bukan hasil eksperimen penelitian.** 

# **Lampiran B - Artefak yang Diharapkan untuk Skripsi** 

- Diagram arsitektur sistem. 

- Flowchart/pseudocode Dijkstra standar. 

- Flowchart/pseudocode Dijkstra optimasi. 

- ERD/struktur koleksi bila Firestore dipakai. 

- Spesifikasi dataset dan contoh graph. 

- Tabel test case algoritma. 

- Tabel raw benchmark. 

- Tabel statistik agregat. 

- Grafik execution time terhadap ukuran graph. 

- Grafik visited nodes terhadap ukuran graph. 

- Tabel persentase peningkatan performa. 

- Screenshot halaman Navigation, Comparison, dan Benchmark Lab. 

**Baseline keputusan produk:** PRD ini dirancang supaya aplikasi dan penelitian tidak berjalan sebagai dua pekerjaan terpisah: seluruh fitur produk yang P0 secara langsung menghasilkan bukti yang dibutuhkan untuk menjawab rumusan masalah dan menyusun Bab IV. 

PRD - Sistem Navigasi Cerdas | Optimasi Algoritma Dijkstra 


