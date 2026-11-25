# Bukti pengujian BAB V

Naskah utama berada di `docs/BAB_V_Implementasi_dan_Pengujian_Sistem.md` pada root proyek. Naskah final dibuat setelah eksperimen selesai dan seluruh pemeriksaan ketepatan lulus.

## Isi bukti

- `manifest.json`: tanggal, konfigurasi, pasangan titik, versi runtime dan hash dataset.
- `benchmark.json`: ringkasan dan seluruh eksekusi terukur.
- `raw-runs.csv`: 60 eksekusi, termasuk rute setiap eksekusi.
- `correctness.json`: pemeriksaan terhadap NetworkX dan validitas rute.
- `provenance.json`: perangkat, hash kode algoritma dan batasan pengukuran.
- `pytest.xml`: sembilan tes backend.
- `ui-tests.json`: enam pemeriksaan antarmuka.
- `ui-bandung-route.json`: satu hasil pencarian dari antarmuka; terpisah dari statistik benchmark.
- `pair-statistics.json`: statistik tiap pasangan untuk grafik.
- `evidence-sha256.json`: hash berkas bukti final.
- `implementasi-*.png`: tangkapan layar aplikasi; nama `demo` berarti data uji fungsional, bukan eksperimen Kota Bandung.
- `grafik-waktu.png` dan `.svg`: grafik statistik benchmark Kota Bandung.

## Reproduksi dalam proyek

1. Pertahankan dataset JSON dengan SHA-256 yang tercantum pada manifest.
2. Gunakan dependensi backend dan pengolahan data proyek. Pembuatan grafik juga memakai Matplotlib 3.11.2.
3. Dari root proyek jalankan `backend/.venv/Scripts/python.exe backend/scripts/run_thesis_experiment.py`.
4. Setelah selesai jalankan `backend/.venv/Scripts/python.exe artifacts/bab5/finalize-report.py`.

Skrip eksperimen menjalankan fungsi benchmark aplikasi dengan Firestore dinonaktifkan. Ia membungkus fungsi standar hanya untuk mencetak kemajuan setelah timer internal selesai. Hasil waktu berasal dari timer asli algoritma. Warm-up tidak masuk hasil mentah atau statistik. Pemeriksaan NetworkX berlangsung setelah benchmark selesai, di luar pengukuran.

Hasil waktu antar-pengulangan atau pengujian ulang tidak harus identik. Urutan masih tetap standar lalu optimasi. Sesi ini belum mengendalikan beban komputer sepenuhnya dan tidak menguji signifikansi statistik. Sepuluh pasangan acak tidak mewakili seluruh kombinasi rute.

## Catatan penyusunan skripsi

Penomoran mengikuti bagian skripsi S1 pada pedoman: 5.1 perangkat keras, 5.2 perangkat lunak, 5.3 database, 5.4 implementasi sistem, 5.5 pengujian. Ini memperbaiki susunan usulan awal dalam percakapan.

Tanggal pengujian nyata adalah 17 September 2026. Jika BAB I masih menggunakan jadwal tahun 2025, selaraskan jadwal berdasarkan pelaksanaan sebenarnya. Angka atau tanggal pengujian tidak boleh diganti menjadi data fiktif.

Firestore dirancang dan memiliki kode integrasi, tetapi pengujian sesi ini memakai memori. Jangan menyatakan persistensi Firestore telah lulus. Tampilan demo memakai bobot relatif dan tidak boleh dicampurkan ke tabel pengujian Kota Bandung yang memakai meter.
