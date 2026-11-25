# Penetapan cakupan penelitian: Kota Bandung

Keputusan pengguna: objek geografis penelitian adalah seluruh Kota Bandung,
menggantikan rencana Kabupaten Bandung/Kecamatan Soreang. Dataset Soreang tetap
dipertahankan sebagai data uji awal dan bukan dataset utama penelitian.

## Pengganti uraian cakupan Bab I

Penelitian menggunakan jaringan jalan nyata di wilayah Kota Bandung yang
direpresentasikan sebagai graf berarah berbobot nonnegatif. Simpul mewakili
persimpangan, ujung jalan, atau titik yang dipertahankan oleh penyederhanaan
topologi. Sisi mewakili hubungan perjalanan antarsimpul dan bobot sisi menyatakan
panjang ruas dalam meter. Jaringan kendaraan diambil dari OpenStreetMap melalui
OSMnx berdasarkan batas administratif Kota Bandung.

Sesuaikan penyebutan objek pada 1.1, 1.3, 1.4, 1.5, 1.6.1, 1.7, dan 1.8,
serta uraian rencana penelitian pada Bab II. Jangan mengganti nama wilayah dalam
judul atau hasil penelitian terdahulu karena itu merupakan fakta sumber.

## 3.1.2 Cakupan Wilayah dan Sumber Data

Cakupan penelitian meliputi jaringan jalan kendaraan yang tercatat dalam
OpenStreetMap pada batas administratif Kota Bandung, Jawa Barat. Batas pengambilan
menggunakan objek relation OpenStreetMap 13290062 yang dikenali sebagai Bandung
City. Jaringan diambil menggunakan OSMnx dengan filter drive dan disederhanakan
secara topologis. Seluruh komponen jaringan dipertahankan, termasuk komponen yang
tidak saling terhubung, sehingga kasus tujuan tidak terjangkau tetap dapat diuji.

Data merupakan representasi jalan yang tercatat di OpenStreetMap pada saat
pengambilan, bukan jaminan kelengkapan seluruh jalan atau ketepatan pembatasan
kendaraan di lapangan. Bobot mengikuti panjang sisi OSMnx dalam meter, bukan
waktu perjalanan. Hasil pencarian berlaku pada graf yang diekstrak: rute yang
keluar wilayah lalu kembali masuk tidak dijamin tercakup. Penyederhanaan
topologi dapat mempertahankan geometri ruas yang melintasi batas; simpul graf
akhir mengikuti pemotongan wilayah OSMnx, bukan kliping setiap garis jalan.

## Artefak dan reproduksi

- Dataset aplikasi: backend/app/data/datasets/kota-bandung-osm-drive.json
- Batas wilayah: artifacts/kota-bandung-boundary.geojson
- Data lengkap dengan atribut dan geometri: artifacts/kota-bandung/network.graphml
- Tabel lampiran: artifacts/kota-bandung/nodes.csv dan edges.csv
- Jumlah data, tanggal ekstraksi, parameter, versi runtime, checksum, dan hasil
  validasi: artifacts/kota-bandung/metadata.json
- Skrip: backend/scripts/build_bandung_dataset.py

JSON aplikasi menyimpan struktur graf dan bobot, sedangkan GraphML menyimpan
atribut jalan serta geometri. Jumlah sisi berarah tidak sama dengan jumlah ruas
fisik: jalan dua arah umumnya direpresentasikan oleh dua sisi. ID simpul tidak
selalu berarti satu persimpangan fisik yang telah dikonsolidasikan.

Sumber: https://www.openstreetmap.org/relation/13290062
Dokumentasi: https://osmnx.readthedocs.io/en/stable/user-reference.html
Atribusi: © OpenStreetMap contributors.
Lisensi: https://www.openstreetmap.org/copyright

Salinan PRD pada folder docs telah diselaraskan untuk wilayah Kota Bandung.
PRD sumber di luar workspace dan naskah Word pengguna belum diubah. Referensi
Bab IV pada PRD sebagai lokasi hasil penelitian masih perlu diselaraskan dengan
pedoman enam bab (hasil implementasi/pengujian berada di Bab V).
