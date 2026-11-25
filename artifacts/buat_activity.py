from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

s=['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="2220" viewBox="0 0 1400 2220">
<title>Activity Diagram Pencarian dan Perbandingan Rute</title>
<desc>Swimlane Pengguna dan Sistem, validasi input dengan alur perbaikan, pemilihan mode standar, optimasi, atau perbandingan secara berurutan, lalu penyajian hasil.</desc>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="black"/></marker></defs>
<rect width="1400" height="2220" fill="white"/>
<g stroke="black" stroke-width="2" fill="white">
<rect x="25" y="25" width="1350" height="2160"/>
<path d="M480 25 V2185 M25 100 H1375"/>
''']
def text(x,y,lines,size=27):
    s.append(f'<text x="{x}" y="{y-(len(lines)-1)*16+9}" text-anchor="middle" fill="black" stroke="none" font-family="Times New Roman,Times,serif" font-size="{size}">')
    for i,line in enumerate(lines):s.append(f'<tspan x="{x}" dy="{32 if i else 0}">{escape(line)}</tspan>')
    s.append('</text>')
def box(x,y,w,h,lines):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/>');text(x+w/2,y+h/2,lines)
def diamond(x,y):s.append(f'<path d="M{x} {y-24} L{x+28} {y} L{x} {y+24} L{x-28} {y} Z"/>')
def arrow(d):s.append(f'<path d="{d}" fill="none" marker-end="url(#a)"/>')
text(252,64,['Pengguna'],32);text(927,64,['Sistem'],32)
s.append('<circle cx="250" cy="145" r="13" fill="black"/>')
box(90,195,320,85,['Memilih dataset'])
box(730,320,450,100,['Memuat dan memvalidasi graf;', 'menampilkan jaringan'])
box(80,465,340,110,['Menentukan sumber, tujuan,', 'dan mode; menjalankan', 'pencarian'])
box(730,620,450,80,['Memvalidasi titik pencarian'])
diamond(955,760)
box(530,720,310,80,['Menampilkan pesan', 'kesalahan'])
box(80,720,340,80,['Memperbaiki masukan'])
box(730,850,450,80,['Memeriksa mode pencarian'])
diamond(955,1000)
box(535,1100,240,110,['Menjalankan', 'Dijkstra standar'])
box(815,1100,240,110,['Menjalankan', 'Dijkstra optimasi'])
box(1095,1100,240,110,['Menjalankan', 'Dijkstra standar'])
box(1095,1280,240,110,['Menjalankan', 'Dijkstra optimasi', 'pada input sama'])
box(1050,1455,305,120,['Memeriksa kesetaraan', 'biaya dan status;', 'menandai ketidaksesuaian'])
diamond(955,1650)
box(720,1740,480,110,['Menampilkan jalur, biaya, metrik,', 'dan status hasil / tidak terjangkau'])
box(80,1910,340,100,['Meninjau hasil pencarian', 'atau perbandingan'])
s.append('<circle cx="250" cy="2110" r="23"/><circle cx="250" cy="2110" r="15" fill="black"/>')
arrow('M250 158 V195');arrow('M250 280 V370 H730');arrow('M955 420 V445 H250 V465')
arrow('M420 520 H955 V620');arrow('M955 700 V736')
arrow('M927 760 H840');text(885,735,['[tidak valid]'],20)
arrow('M530 760 H420');arrow('M80 760 H55 V590 H455 V520 H420')
arrow('M955 784 V850');text(1020,815,['[valid]'],21)
arrow('M955 930 V976')
arrow('M927 1000 H655 V1100');text(725,974,['[standar]'],23)
arrow('M955 1024 V1060 H935 V1100');text(870,1057,['[optimasi]'],23)
arrow('M983 1000 H1215 V1100');text(1215,974,['[bandingkan]'],23)
arrow('M1215 1210 V1280');arrow('M1215 1390 V1455')
arrow('M655 1210 V1650 H927');arrow('M935 1210 H1005 V1600 H955 V1626');arrow('M1202 1575 V1650 H983')
arrow('M955 1674 V1740');arrow('M955 1850 V1875 H250 V1910');arrow('M250 2010 V2087')
s.append('</g></svg>')
p=Path(__file__).with_name('activity-pencarian-perbandingan.svg');p.write_text('\n'.join(s),encoding='utf-8');ET.parse(p);print(p)
