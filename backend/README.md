# Dijkstra Backend

Dataset utama penelitian: **Kota Bandung**, `kota-bandung-osm-drive`
(27.172 simpul dan 61.630 sisi berarah). Dataset Soreang tetap untuk uji awal.
Untuk mereproduksi ekstraksi dengan batas terverifikasi, jalankan dari root proyek:
`backend/.venv/Scripts/python.exe backend/scripts/build_bandung_dataset.py`.
Skrip menggunakan `artifacts/kota-bandung-boundary.geojson`; metadata, CSV,
dan GraphML tersedia pada `artifacts/kota-bandung/`.

Backend FastAPI untuk simulator navigasi dan benchmark Dijkstra.

## Deploy Railway + Firebase Hosting

Railway menjalankan FastAPI dari `backend/Dockerfile`. Konfigurasi
`railway.json` memeriksa endpoint `/api/health`. Firebase Hosting melayani
frontend statis.

```powershell
npm i -g @railway/cli
railway login
railway up backend --path-as-root --new --name dijkstra-route-api
railway domain
```

Setelah Railway memberi URL publik, misalnya `https://dijkstra-route-api.up.railway.app`,
build dan deploy frontend dari root proyek:

```powershell
$env:NUXT_PUBLIC_API_BASE = 'https://dijkstra-route-api.up.railway.app'
pnpm generate
firebase deploy --only hosting
```

Tambahkan URL Firebase Hosting ke `ALLOWED_ORIGINS` pada Railway jika API diakses
langsung dari browser. Saat backend memakai Firestore, set variable Railway:
`FIREBASE_ENABLED=true`, `FIREBASE_PROJECT_ID=dijkstra-route-optimization`, dan
`FIREBASE_SERVICE_ACCOUNT_JSON` berisi seluruh JSON service account dalam satu baris.
Simpan nilai JSON hanya sebagai Railway Variable; jangan commit ke repository.

## Menjalankan secara lokal

Dari folder `backend` pada PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Konfigurasi Firebase Firestore

Firestore menyimpan metadata eksperimen pada collection `experiments` dan
raw run pada subcollection `experiments/{experimentId}/runs`. Graph dataset
tetap dimuat ke memori; Firestore tidak masuk ke jalur pengukuran waktu
algoritma.

1. Buat project Firebase dan aktifkan Cloud Firestore melalui Firebase
   Console.
2. Buka Project settings > Service accounts > Generate new private key.
3. Simpan file key di luar repository, lalu salin `.env.example` menjadi `.env`.
4. Isi konfigurasi berikut:

```dotenv
FIREBASE_ENABLED=true
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\username\Downloads\firebase-service-account.json
FIREBASE_PROJECT_ID=project-id-anda
```

Jangan commit file service-account JSON atau isi `.env`. Jika Firebase belum
diaktifkan, backend tetap berjalan dengan fallback memory dan endpoint
`/api/firebase/status` akan melaporkan mode tersebut.

Setelah konfigurasi selesai, restart backend dan cek:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/firebase/status
```

Respons yang diharapkan ketika aktif memiliki `connected: true` dan
`mode: "firestore"`.

Jika ingin mengelola rules dari repository menggunakan Firebase CLI:

```powershell
firebase login
firebase use --add
firebase deploy --only firestore
```

Dokumentasi API tersedia di:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Menjalankan test

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Membuat dataset jaringan jalan dari OpenStreetMap

Dataset yang dipakai algoritma adalah graph: node mewakili persimpangan atau
ujung jalan, sedangkan edge mewakili ruas jalan. Nilai `weight` pada dataset
OSM di bawah ini adalah panjang ruas dalam meter. Pengambilan data dilakukan
satu kali sebagai preprocessing; API dan benchmark tidak mengakses internet
atau memakai NetworkX untuk menghitung rute.

Install dependency preprocessing:

```powershell
python -m pip install -r requirements-data.txt
```

Buat dataset baru dari nama wilayah yang dikenali Nominatim:

```powershell
python scripts/build_osm_dataset.py `
  --place "Kota Bandung, Jawa Barat, Indonesia" `
  --dataset-id kota-bandung-osm-drive `
  --version 1.0.0 `
  --network-type drive
```

Output akan tersimpan di `app/data/datasets/{dataset-id}.json` dan langsung
terbaca oleh endpoint `/api/datasets` setelah server direstart. Dataset contoh
yang sudah dibuat di repository adalah `soreang-osm-small` (223 node, 481 edge).

Data OpenStreetMap wajib diberi atribusi kepada kontributor OpenStreetMap dan
digunakan sesuai lisensi ODbL. Untuk penelitian, simpan juga wilayah, tanggal
ekstraksi, versi dataset, dan parameter preprocessing agar eksperimen dapat
direproduksi.

## Endpoint utama

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| GET | `/api/health` | Health check |
| GET | `/api/firebase/status` | Status koneksi Firestore |
| GET | `/api/datasets` | Daftar dataset |
| GET | `/api/datasets/{id}` | Detail dataset dan graf |
| POST | `/api/routes/standard` | Satu rute dengan baseline |
| POST | `/api/routes/optimized` | Satu rute dengan optimasi |
| POST | `/api/routes/compare` | Perbandingan dua algoritma |
| POST | `/api/benchmarks` | Batch benchmark |
| GET | `/api/benchmarks/{id}` | Detail benchmark |
| GET | `/api/experiments` | Riwayat benchmark dalam proses berjalan |
| GET | `/api/experiments/{id}/export.csv` | Export raw run ke CSV |

Contoh request compare:

```json
{
  "datasetId": "small-demo",
  "sourceId": "soreang",
  "destinationId": "baleendah"
}
```

Dataset tetap dimuat dari `app/data/datasets` ke memori. Firestore hanya
menyimpan metadata, konfigurasi, summary, dan raw result benchmark.

