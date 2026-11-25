from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
out=Path(__file__).parent
def start(w,h,title):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{title}</title><rect width="100%" height="100%" fill="white"/>']
def text(s,x,y,t,size=25,anchor='start',bold=False):
 s.append(f'<text x="{x}" y="{y}" font-family="Times New Roman,Times,serif" font-size="{size}" text-anchor="{anchor}" font-weight="{"bold" if bold else "normal"}">{escape(t)}</text>')
def box(s,x,y,w,title,rows):
 h=60+len(rows)*34+16
 s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="black" stroke-width="2"/><path d="M{x} {y+52} H{x+w}" stroke="black" stroke-width="2"/>')
 text(s,x+w/2,y+35,title,28,'middle',True)
 for i,r in enumerate(rows):text(s,x+18,y+85+i*34,r)
 return h
def line(s,d,dash=False):s.append(f'<path d="{d}" fill="none" stroke="black" stroke-width="2"'+(' stroke-dasharray="8 6"' if dash else '')+'/>')
def save(s,name):
 p=out/name;p.write_text('\n'.join(s)+ '</svg>',encoding='utf-8');ET.parse(p)

s=start(1500,1320,'Model Hubungan Data Konseptual')
text(s,750,42,'Model Hubungan Data Konseptual',32,'middle',True)
s.append('<rect x="25" y="80" width="1450" height="650" fill="none" stroke="black" stroke-dasharray="9 7"/>')
text(s,55,120,'Dataset jaringan jalan — file JSON',28,bold=True)
box(s,550,155,410,'Dataset',['id, version','name, source, region','networkType, weightUnit','extractedAt'])
box(s,120,440,430,'Simpul',['id (unik dalam dataset)','name','latitude, longitude'])
box(s,970,440,430,'Sisi',['from → id simpul asal','to → id simpul tujuan','weight','bidirectional'])
line(s,'M650 367 V400 H335 V440');text(s,615,390,'1',22);text(s,350,430,'1..*',22)
line(s,'M860 367 V400 H1185 V440');text(s,875,390,'1',22);text(s,1200,430,'0..*',22)
line(s,'M550 500 H970');text(s,760,480,'asal: satu simpul → banyak sisi',23,'middle');text(s,565,525,'1',21);text(s,915,525,'0..*',21)
line(s,'M550 610 H970');text(s,760,590,'tujuan: satu simpul → banyak sisi',23,'middle');text(s,565,635,'1',21);text(s,915,635,'0..*',21)
s.append('<rect x="25" y="815" width="1450" height="405" fill="none" stroke="black" stroke-dasharray="9 7"/>')
text(s,55,855,'Hasil eksperimen — Firestore',28,bold=True)
box(s,150,890,500,'Eksperimen',['experimentId','datasetId, datasetVersion','konfigurasi, statistik, createdAt'])
box(s,925,890,490,'Hasil Eksekusi (Run)',['id, experimentId','datasetId, datasetVersion','sourceId, destinationId','algorithm, algorithmVersion','path, totalCost, metrik, status'])
line(s,'M650 1000 H925');text(s,785,975,'memiliki',24,'middle');text(s,672,1028,'1',22);text(s,860,1028,'0..*',22)
line(s,'M550 250 H65 V780 H700 V870 H400 V890',True);text(s,850,770,'referensi datasetId + versi',23,'middle');text(s,80,700,'1',22);text(s,412,882,'0..*',22)
text(s,750,1262,'Garis putus-putus: referensi logis lintas penyimpanan, bukan foreign key Firestore.',24,'middle')
text(s,750,1298,'Satu run merujuk satu sumber dan satu tujuan pada versi dataset yang dicatat.',24,'middle')
save(s,'bab4-hubungan-data.svg')

s=start(1300,1250,'Struktur Koleksi Firestore')
text(s,650,48,'Struktur Koleksi Firestore',32,'middle',True)
box(s,70,105,460,'Koleksi: experiments',['Menampung dokumen eksperimen'])
box(s,215,300,980,'Dokumen: {experimentId}',['experimentId, datasetId, datasetVersion','testCaseCount, repeatCount, warmupRuns','pairMode, randomSeed, correctnessMismatchCount','standard, optimized, improvement, createdAt'])
line(s,'M110 215 V260 H255 V300')
box(s,360,590,460,'Subkoleksi: runs',['Menampung hasil setiap eksekusi'])
line(s,'M255 512 V555 H400 V590')
box(s,500,785,710,'Dokumen: {experimentId}-run-{nomorUrut}',['id, experimentId, datasetId, datasetVersion','sourceId, destinationId','algorithm, algorithmVersion','executionTimeNs, executionTimeMs','visitedNodes, processedEdges','totalCost, path, pathLength, status, createdAt'])
line(s,'M400 700 V745 H540 V785')
text(s,650,1155,'Path: experiments/{experimentId}/runs/{runId}',26,'middle')
text(s,650,1205,'Simpul dan sisi graf disimpan dalam JSON, bukan pada koleksi di atas.',25,'middle')
save(s,'bab4-struktur-firestore.svg')
print('Generated two SVG diagrams')

