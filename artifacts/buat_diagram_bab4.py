"""Generate print-ready, editable SVG figures for chapter IV."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

OUT = Path(__file__).parent
class SVG:
    def __init__(self,w,h,title):
        self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{escape(title)}</title>', '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="black"/></marker><marker id="general" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="15" markerHeight="15" orient="auto"><path d="M1 1 L11 6 L1 11 Z" fill="white" stroke="black"/></marker></defs>',f'<rect width="{w}" height="{h}" fill="white"/>']
    def text(self,x,y,lines,size=26,bold=False):
        if isinstance(lines,str):lines=[lines]
        self.s.append(f'<text x="{x}" y="{y-(len(lines)-1)*16+8}" text-anchor="middle" font-family="Times New Roman,Times,serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="black">')
        for i,t in enumerate(lines):self.s.append(f'<tspan x="{x}" dy="{32 if i else 0}">{escape(t)}</tspan>')
        self.s.append('</text>')
    def box(self,x,y,w,h,lines,round=False):
        self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{15 if round else 0}" fill="white" stroke="black" stroke-width="2"/>');self.text(x+w/2,y+h/2,lines)
    def path(self,d,arrow=True,dash=False,marker='a'):
        self.s.append(f'<path d="{d}" fill="none" stroke="black" stroke-width="2"'+(f' marker-end="url(#{marker})"' if arrow else '')+(' stroke-dasharray="8 6"' if dash else '')+'/>')
    def diamond(self,x,y,w=200,h=100,lines=None):
        self.s.append(f'<path d="M{x} {y-h/2} L{x+w/2} {y} L{x} {y+h/2} L{x-w/2} {y} Z" fill="white" stroke="black" stroke-width="2"/>')
        if lines:self.text(x,y,lines,24)
    def actor(self,x,y,name):
        self.s.append(f'<circle cx="{x}" cy="{y}" r="20" fill="white" stroke="black" stroke-width="2"/>')
        self.path(f'M{x} {y+20} V{y+75} M{x-35} {y+45} H{x+35} M{x} {y+75} L{x-30} {y+115} M{x} {y+75} L{x+30} {y+115}',False)
        self.text(x,y+150,name)
    def ellipse(self,x,y,w,h,lines):
        self.s.append(f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="white" stroke="black" stroke-width="2"/>');self.text(x,y,lines)
    def save(self,name):
        p=OUT/name;p.write_text('\n'.join(self.s)+ '\n</svg>',encoding='utf-8');ET.parse(p);print(p)

# Architecture: offline data preparation is explicitly outside runtime timing.
a=SVG(1400,1300,'Perancangan Arsitektur Sistem')
a.text(700,40,'Penyiapan dataset secara offline',29,True)
a.box(45,95,280,100,['OpenStreetMap','Batas Kota Bandung'])
a.box(490,95,350,100,['OSMnx','Ekstraksi dan validasi'])
a.box(1000,95,350,100,['File dataset JSON','Arsip GraphML dan CSV'])
a.path('M325 145 H490');a.path('M840 145 H1000')
a.path('M30 240 H1370',False,True)
a.text(700,275,'Aplikasi saat digunakan',29,True)
a.box(60,350,370,120,['Antarmuka Nuxt + TypeScript','Peta Leaflet'])
a.box(570,350,370,120,['Layanan API FastAPI','Validasi permintaan'])
a.box(1020,350,330,120,['Layanan dataset','Graf di memori'])
a.path('M430 385 H570');a.text(500,355,'HTTP',21)
a.path('M570 440 H430');a.text(500,470,'JSON',21)
a.path('M940 390 H1020');a.path('M1020 435 H940')
a.path('M1175 195 V350')
a.box(470,575,420,115,['Pengelola pencarian / eksperimen','Kasus uji, pengulangan, validasi'])
a.path('M755 470 V575')
a.box(155,825,400,110,['Dijkstra standar','Pemilihan minimum linear'])
a.box(735,825,470,110,['Dijkstra optimasi','Min-heap + penghentian dini'])
a.path('M610 690 V750 H355 V825');a.path('M750 690 V750 H970 V825')
a.path('M1185 470 V730 H1245 V970 H60 V880 H155')
a.path('M1245 880 H1205');a.text(1140,1008,'Graf yang sama',23)
a.text(665,785,'Diukur terpisah: inisialisasi dan iterasi algoritma',22)
a.box(370,1060,540,90,['Hasil dan statistik eksperimen'])
a.path('M355 935 V1105 H370');a.path('M970 935 V1105 H910')
a.box(55,1200,530,75,['Penyimpanan Firestore (jika aktif)'])
a.box(880,1200,380,75,['Ekspor CSV'])
a.path('M500 1150 V1175 H320 V1200');a.path('M800 1150 V1175 H1070 V1200')
a.save('bab4-arsitektur-sistem.svg')

# Use case associations have no arrowheads. Researcher specializes demo user.
u=SVG(1300,1260,'Use Case Diagram Sistem Navigasi dan Eksperimen')
u.s.append('<rect x="440" y="40" width="820" height="1120" fill="white" stroke="black" stroke-width="2"/>')
u.text(850,85,'Sistem Navigasi dan Eksperimen Dijkstra',30,True)
u.actor(185,235,'Pengguna demo');u.actor(185,795,'Peneliti')
u.path('M185 770 V440',True,False,'general')
cases=[['Melihat informasi dataset'],['Menentukan titik awal','dan tujuan'],['Menjalankan pencarian rute'],['Membandingkan','hasil algoritma'],['Menjalankan eksperimen','berkelompok'],['Melihat riwayat dan','detail eksperimen'],['Mengekspor hasil eksperimen']]
for i,lines in enumerate(cases):
    y=190+i*140;u.ellipse(865,y,650,95,lines)
    if i<4:u.path(f'M220 280 H350 V{y} H540',False)
    else:u.path(f'M220 840 H390 V{y} H540',False)
u.text(650,1210,'Peneliti mewarisi aktivitas pengguna demo; autentikasi tidak diasumsikan.',24)
u.save('bab4-use-case.svg')

# Sequence: no fork; timing is internal to each algorithm invocation.
q=SVG(1600,1550,'Sequence Diagram Perbandingan Rute')
xs=[120,425,745,1070,1420]
heads=[['Pengguna'],['Antarmuka'],['API / Layanan','Perbandingan'],['Layanan dataset'],['Mesin algoritma']]
for x,h in zip(xs,heads):
    q.box(x-110,35,220,95,h);q.path(f'M{x} 130 V1430',False,True)
def msg(i,j,y,t,reply=False):
    q.text((xs[i]+xs[j])/2,y-(42 if isinstance(t,list) else 25),t,23);q.path(f'M{xs[i]} {y} H{xs[j]}',True,reply)
msg(0,1,220,['Pilih dataset, sumber, tujuan','dan mode bandingkan'])
msg(1,2,340,'Kirim permintaan perbandingan')
q.box(650,390,280,75,['Validasi permintaan'])
msg(2,3,550,'Minta graf dataset')
msg(3,2,650,'Kembalikan graf di memori',True)
msg(2,4,760,'Jalankan Dijkstra standar (graf, sumber, tujuan)')
msg(4,2,865,'Hasil standar dan metrik',True)
msg(2,4,975,'Jalankan Dijkstra optimasi (input identik)')
msg(4,2,1080,'Hasil optimasi dan metrik',True)
q.box(590,1140,490,95,['Bandingkan biaya dan status;', 'susun hasil perbandingan'])
msg(2,1,1300,'Kembalikan hasil perbandingan',True)
msg(1,0,1400,'Tampilkan jalur, status, dan metrik',True)
q.text(800,1500,'Alur utama untuk permintaan valid; timer berada di dalam setiap eksekusi algoritma.',24)
q.save('bab4-sequence-perbandingan.svg')

f=SVG(1200,2480,'Flowchart Dijkstra Optimasi')
f.box(440,30,260,60,['Mulai'],True)
f.box(300,130,540,90,['Graf tersedia; masukan sumber','dan tujuan'])
f.diamond(570,305,440,110,['Kedua titik valid?'])
f.box(880,260,260,90,['Kembalikan error'])
f.box(300,415,540,130,['Mulai timer; inisialisasi jarak,','pendahulu, settled, dan metrik;', 'masukkan (0, sumber) ke heap'])
f.diamond(570,650,440,120,['Heap tidak kosong?'])
f.box(300,780,540,85,['Ambil entri minimum (jarak, u)'])
f.diamond(570,975,490,140,['u sudah diproses atau', 'jarak > jarak terbaik u?'])
f.box(300,1115,540,95,['Tandai u telah diproses;', 'tambah penghitung simpul'])
f.diamond(570,1320,440,120,['u adalah tujuan?'])
f.box(300,1460,540,140,['Periksa setiap sisi keluar u;', 'tambah penghitung sisi;', 'hitung kandidat jarak tetangga'])
f.box(300,1660,540,120,['Jika kandidat lebih kecil:', 'perbarui jarak dan pendahulu;', 'masukkan entri baru ke heap'])
f.box(300,1900,540,85,['Hentikan timer; catat durasi'])
f.box(300,2050,540,120,['Tujuan terjangkau: rekonstruksi jalur;', 'jika tidak: jalur kosong, biaya null,', 'status tidak terjangkau'])
f.box(300,2230,540,80,['Kembalikan hasil dan metrik'])
f.box(440,2380,260,60,['Selesai'],True)
for y1,y2 in [(90,130),(220,250),(360,415),(545,590),(710,780),(865,905),(1045,1115),(1210,1260),(1380,1460),(1600,1660),(1985,2050),(2170,2230),(2310,2380)]:f.path(f'M570 {y1} V{y2}')
f.text(625,387,'[ya]',22);f.text(625,744,'[ya]',22);f.text(630,1080,'[tidak]',22);f.text(630,1420,'[tidak]',22)
f.path('M790 305 H880');f.text(830,280,'[tidak]',21)
f.path('M1140 305 H1170 V2410 H700')
f.path('M790 650 H1040 V1942 H840');f.text(910,625,'[tidak]',22)
f.path('M815 975 H940 V575 H570 V590');f.text(880,950,'[ya]',22)
f.path('M790 1320 H1040');f.text(900,1295,'[ya]',22)
f.path('M300 1720 H115 V575 H570')
f.text(190,1855,'Ulangi pencarian',22)
f.save('bab4-flowchart-dijkstra-optimasi.svg')

