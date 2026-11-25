from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

out=Path(__file__).parent
class Wire:
 def __init__(self,title,active):
  self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1050" viewBox="0 0 1500 1050"><title>Wireframe {title}</title><rect width="1500" height="1050" fill="white"/>']
  self.rect(20,20,1460,990);self.rect(20,20,270,990,'#f5f5f5');self.text(48,72,'DIJKSTRA LAB',27)
  for i,n in enumerate(['Navigation Simulator','Comparison','Benchmark Lab','Experiment History']):
   y=135+i*80
   self.rect(35,y,240,60,'#dddddd' if i==active else 'white');self.text(48,y+37,n,21)
  self.text(45,960,'Panel navigasi',20)
  self.text(325,76,title,32);self.text(325,112,'Rancangan antarmuka — bukan hasil eksperimen',21)
  self.text(750,1035,'Placeholder menunjukkan posisi komponen dan data.',21)
 def text(self,x,y,t,size=23):self.s.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="black">{escape(t)}</text>')
 def rect(self,x,y,w,h,fill='white'):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="black" stroke-width="1.5"/>')
 def field(self,x,y,w,label,value):
  self.text(x,y,label,21);self.rect(x,y+14,w,48);self.text(x+12,y+46,value,21)
 def button(self,x,y,w,label):self.rect(x,y,w,48,'#e5e5e5');self.text(x+15,y+31,label,21)
 def table(self,x,y,width,cols,rows):
  rh=55;cw=width/len(cols)
  self.rect(x,y,width,rh*(len(rows)+1));self.rect(x,y,width,rh,'#eeeeee')
  for i,c in enumerate(cols):
   self.text(x+i*cw+12,y+34,c,20)
   if i:self.s.append(f'<path d="M{x+i*cw} {y} V{y+rh*(len(rows)+1)}" stroke="black"/>')
  for j,row in enumerate(rows):
   yy=y+(j+1)*rh;self.s.append(f'<path d="M{x} {yy} H{x+width}" stroke="black"/>')
   for i,c in enumerate(row):self.text(x+i*cw+12,yy+34,c,20)
 def save(self,name):
  p=out/name;p.write_text('\n'.join(self.s)+'</svg>',encoding='utf-8');ET.parse(p)

w=Wire('Navigation Simulator',0)
w.rect(325,150,710,700);w.text(530,200,'AREA PETA JARINGAN JALAN',23)
w.s.append('<g fill="none" stroke="#999" stroke-width="2"><path d="M355 320 H1005 M355 470 H1005 M355 620 H1005 M450 230 V800 M650 230 V800 M850 230 V800"/></g>')
w.s.append('<path d="M450 620 V470 H850 V320" fill="none" stroke="black" stroke-width="6"/><circle cx="450" cy="620" r="13" fill="white" stroke="black" stroke-width="3"/><circle cx="850" cy="320" r="13" fill="black"/>')
w.text(470,655,'Sumber',20);w.text(870,305,'Tujuan',20);w.text(375,828,'Ilustrasi posisi jalur, bukan peta Kota Bandung',21)
w.rect(1060,150,390,700);w.text(1080,195,'Konfigurasi pencarian',25)
for y,l,v in [(245,'Dataset','[Pilih dataset]  v'),(350,'Titik awal','[Pilih simpul]  v'),(455,'Titik tujuan','[Pilih simpul]  v'),(560,'Mode algoritma','[Standar / Optimasi / Bandingkan]')]:w.field(1080,y,350,l,v)
w.button(1080,665,350,'Jalankan pencarian');w.text(1080,760,'Status: [pesan proses]',21);w.text(1080,805,'[Pesan kesalahan jika ada]',20)
w.rect(325,875,1125,105);w.text(345,912,'Informasi dataset: [nama] | [versi] | [jumlah simpul] | [jumlah sisi]',22);w.text(345,950,'Sumber data: OpenStreetMap | Satuan jarak: meter',21)
w.save('wireframe-navigation-simulator.svg')

w=Wire('Comparison',1)
w.rect(325,155,1125,80);w.text(345,202,'Dataset: [nama]     Sumber: [ID]     Tujuan: [ID]',24)
for x,title in [(325,'Dijkstra standar'),(905,'Dijkstra optimasi')]:
 w.rect(x,265,545,220);w.text(x+20,310,title,27)
 for y,t in [(355,'Status: [hasil pencarian]'),(400,'Total bobot: [nilai] meter'),(445,'Waktu eksekusi: [nilai] ms')]:w.text(x+20,y,t,23)
w.table(325,520,1125,['Metrik','Standar','Optimasi','Perubahan'],[['Waktu eksekusi','[nilai] ms','[nilai] ms','[nilai] %'],['Simpul diproses','[jumlah]','[jumlah]','[nilai] %'],['Sisi diperiksa','[jumlah]','[jumlah]','[nilai] %'],['Total bobot','[nilai] m','[nilai] m','[selisih]']])
w.rect(325,835,1125,100);w.text(345,875,'Kesetaraan hasil: [sesuai / tidak sesuai]',25);w.text(345,913,'Toleransi: [nilai] | Status kedua algoritma: [keterangan]',21)
w.save('wireframe-comparison.svg')

w=Wire('Benchmark Lab',2)
w.rect(325,150,1125,310)
for x,y,sz,l,v in [(345,190,340,'Dataset','[Pilih dataset] v'),(720,190,330,'Jumlah kasus uji','[jumlah]'),(1080,190,350,'Mode pasangan','[Preset / Acak] v'),(345,295,340,'Jumlah pengulangan','[jumlah]'),(720,295,330,'Pemanasan awal','[jumlah]'),(1080,295,350,'Random seed','[nilai]')]:w.field(x,y,sz,l,v)
w.button(345,390,285,'Jalankan benchmark');w.text(660,422,'Status: [siap / berjalan / selesai / gagal]',21)
w.text(325,510,'Ringkasan hasil eksperimen',27)
w.table(325,540,1125,['Statistik waktu','Standar','Optimasi'],[['Rata-rata / median','[nilai] / [nilai]','[nilai] / [nilai]'],['Minimum / maksimum','[nilai] / [nilai]','[nilai] / [nilai]'],['Simpangan baku','[nilai]','[nilai]']])
w.text(325,800,'Ketidaksesuaian: [jumlah]     Eksekusi tercatat: [jumlah]',22);w.button(1180,775,270,'Ekspor CSV')
w.table(325,850,1125,['Algoritma','Sumber / tujuan','Waktu','Status'],[['[nama]','[ID] / [ID]','[nilai] ms','[status]']])
w.save('wireframe-benchmark-lab.svg')

w=Wire('Experiment History',3)
w.text(325,178,'Riwayat eksperimen tersimpan',27)
w.table(325,215,1125,['Eksperimen','Dataset','Waktu','Kasus / ulang','Mismatch','Tindakan'],[['[ID singkat]','[nama]','[tanggal]','[n] / [r]','[jumlah]','Buka detail'],['[ID singkat]','[nama]','[tanggal]','[n] / [r]','[jumlah]','Buka detail'],['[ID singkat]','[nama]','[tanggal]','[n] / [r]','[jumlah]','Buka detail']])
w.rect(325,480,1125,130);w.text(345,525,'Tindakan “Buka detail” menampilkan hasil di bagian Benchmark Lab.',23);w.text(345,568,'Konfigurasi, statistik, data eksekusi, dan ekspor dapat diakses kembali.',22)
w.rect(325,680,1125,180,'#f5f5f5');w.text(345,725,'Alternatif tampilan ketika riwayat kosong',25);w.text(345,780,'Belum ada eksperimen tersimpan.',24);w.text(345,822,'Jalankan pengujian melalui menu Benchmark Lab.',22)
w.save('wireframe-experiment-history.svg')
print('Four wireframes generated and XML validated.')
