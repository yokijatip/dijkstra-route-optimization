from pathlib import Path
from html import escape

parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="2050" viewBox="0 0 1100 2050">
<title>Flowchart Proses Pencarian Rute Standar</title>
<desc>Baseline Dijkstra dengan pemilihan minimum linear, tanpa penghentian dini pada tujuan.</desc>
<defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="black"/></marker></defs>
<rect width="1100" height="2050" fill="white"/>
<g stroke="black" stroke-width="2" fill="white">''']

def label(x,y,lines,size=25):
    start = y - (len(lines)-1)*16 + 8
    parts.append(f'<text x="{x}" y="{start}" fill="black" stroke="none" text-anchor="middle" font-family="Times New Roman,serif" font-size="{size}">')
    for i,line in enumerate(lines):
        parts.append(f'<tspan x="{x}" dy="{0 if i==0 else 32}">{escape(line)}</tspan>')
    parts.append('</text>')

def box(y,lines,h=90):
    parts.append(f'<rect x="310" y="{y}" width="480" height="{h}"/>')
    label(550,y+h/2,lines)

def diamond(y,lines):
    parts.append(f'<path d="M550,{y} L790,{y+65} L550,{y+130} L310,{y+65} Z"/>')
    label(550,y+65,lines)

def arrow(path):
    parts.append(f'<path d="{path}" fill="none" marker-end="url(#a)"/>')

parts.append('<rect x="425" y="25" width="250" height="60" rx="30"/>')
label(550,55,['Mulai'])
box(115,['Graf tersedia di memori;', 'masukan titik awal dan tujuan'])
diamond(235,['Kedua titik tersedia', 'dalam graf?'])
parts.append('<rect x="825" y="255" width="250" height="90"/>')
label(950,300,['Kembalikan error'],22)
box(400,['Mulai timer; inisialisasi jarak,', 'pendahulu, simpul belum diproses,', 'dan penghitung metrik'],120)
diamond(565,['Masih ada simpul', 'belum diproses?'])
box(735,['Pilih simpul u berjarak minimum', 'melalui pemindaian linear'])
diamond(865,['Jarak u = tak hingga?'])
box(1030,['Hapus u dari himpunan;', 'tambah jumlah simpul diproses'])
box(1160,['Periksa seluruh sisi keluar u;', 'hitung sisi yang diperiksa;', 'relaksasi dan perbarui pendahulu'],120)
box(1350,['Hentikan timer;', 'catat durasi pencarian'])
diamond(1480,['Jarak tujuan berhingga?'])
parts.append('<rect x="65" y="1660" width="400" height="100"/>')
label(265,1710,['Rekonstruksi jalur;', 'status berhasil'])
parts.append('<rect x="635" y="1660" width="400" height="100"/>')
label(835,1710,['Jalur kosong; biaya null;', 'status tidak terjangkau'])
box(1820,['Kembalikan hasil dan metrik'])
parts.append('<rect x="425" y="1960" width="250" height="60" rx="30"/>')
label(550,1990,['Selesai'])
for a,b in [(85,115),(205,235),(365,400),(520,565),(695,735),(825,865),(995,1030),(1120,1160),(1440,1480),(1910,1960)]:
    arrow(f'M550,{a} V{b}')
label(585,385,['Ya'],21)
label(585,715,['Ya'],21)
label(595,1010,['Tidak'],21)
arrow('M790,300 H825'); label(807,277,['Tidak'],20)
arrow('M950,345 H1090 V1990 H675')
arrow('M310,630 H125 V1395 H310'); label(225,610,['Tidak'],21)
arrow('M790,930 H945 V1395 H790'); label(830,910,['Ya'],21)
arrow('M310,1220 H220 V545 H550 V565')
arrow('M310,1545 H265 V1660'); label(265,1520,['Ya'],21)
arrow('M790,1545 H835 V1660'); label(845,1520,['Tidak'],21)
arrow('M265,1760 V1790 H550 V1820')
arrow('M835,1760 V1790 H550')
parts.append('</g></svg>')
output = Path(__file__).with_name('flowchart-dijkstra-standar.svg')
output.write_text('\n'.join(parts),encoding='utf-8')
import xml.etree.ElementTree as ET
ET.parse(output)
print(output)
