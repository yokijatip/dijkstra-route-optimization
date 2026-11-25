from pathlib import Path
from copy import deepcopy
import re,json
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[2]
doc=Document(ROOT/'artifacts/draft-review-source.docx')
ps=list(doc.paragraphs)
changes=[]
# Preserve equations/drawings and flatten only reference-manager fields before editing their text.
stack=[]
for e in list(doc.element.iter()):
 if e.tag==qn('w:fldChar'):
  typ=e.get(qn('w:fldCharType'))
  if typ=='begin':stack.append({'nodes':[e],'code':''})
  elif stack:
   stack[-1]['nodes'].append(e)
   if typ=='end':
    f=stack.pop()
    if f['code'].lstrip().startswith('ADDIN'):
     for node in f['nodes']:
      if node.getparent() is not None:node.getparent().remove(node)
 elif e.tag==qn('w:instrText') and stack:
  stack[-1]['code']+=e.text or '';stack[-1]['nodes'].append(e)

def setp(p,text):
 before=p.text
 p.text=text
 for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(12)
 changes.append({'before':before,'after':text})
def patch(p,old,new):
 nodes=p._p.xpath('.//w:t');text=''.join(n.text or '' for n in nodes)
 count=text.count(old)
 for _ in range(count):
  a=text.index(old);b=a+len(old);pos=0;first=True
  for n in nodes:
   s=n.text or '';end=pos+len(s)
   if end>a and pos<b:
    start=max(0,a-pos);stop=min(len(s),b-pos)
    n.text=s[:start]+(new if first else '')+s[stop:];first=False
   pos=end
  text=''.join(n.text or '' for n in nodes)
def fmt(p,single=False):
 p.paragraph_format.line_spacing=1 if single else 2
 p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0)
 p.paragraph_format.widow_control=True
 for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(12);r.font.color.rgb=RGBColor(0,0,0)
def after(p,text,style='Normal',single=False):
 q=doc.add_paragraph(text,style);p._p.addnext(q._p);fmt(q,single);return q

allp=list(doc.paragraphs)+[p for t in doc.tables for row in t.rows for c in row.cells for p in c.paragraphs]
for p in allp:
 for a,b in [('Kabupaten Bandung','Kota Bandung'),('DJIKSTRA','DIJKSTRA'),('Djikstra','Dijkstra'),('Object Penelitian','Objek Penelitian'),('Kebuthan','Kebutuhan'),('Dijkstra Standa\t','Dijkstra Standar\t'),('Dijkstra Standa','Dijkstra Standar')]:
  if a=='Dijkstra Standa' and 'Dijkstra Standar' in p.text:continue
  patch(p,a,b)
 if p.text.startswith('Table '):patch(p,'Table ','Tabel ')
 if '`' in p.text:patch(p,'`','')
 for node in p._p.xpath('.//w:t'):
  if node.text:
   node.text=re.sub(r'\)(?=[A-Za-z])',') ',node.text)
   node.text=node.text.replace(' ,yang',', yang')
for e in doc.element.xpath('//w:instrText'):
 if e.text:e.text=e.text.replace('SEQ Table ','SEQ Tabel ').replace('\\c "Table"','\\c "Tabel"')
setp(ps[13],'2026')

revisions={
218:'Permasalahan yang dikaji adalah sejauh mana perubahan implementasi Dijkstra dapat meningkatkan efisiensi pencarian dengan tetap mempertahankan ketepatan hasil. Kedua implementasi menggunakan adjacency list yang sama. Optimasi yang dibandingkan meliputi penggunaan antrean prioritas berbasis min-heap sebagai pengganti pencarian minimum linear serta penghentian dini ketika simpul tujuan telah diselesaikan. Pengaruh gabungan kedua teknik tersebut dievaluasi melalui eksperimen pada dataset dan pasangan titik yang sama.',
220:'Pelaksanaan eksperimen menggunakan satu graf jaringan jalan Kota Bandung, sepuluh pasangan titik asal–tujuan, satu pemanasan, dan tiga pengulangan terukur untuk setiap algoritma pada setiap pasangan. Dataset demo digunakan untuk pengujian fungsional dan tidak digabungkan ke dalam statistik kinerja Kota Bandung. Waktu algoritma diukur setelah graf tersedia di memori, tanpa mencakup pemuatan dataset, komunikasi jaringan, penyimpanan hasil, maupun penampilan antarmuka. Hasil setiap eksekusi dicatat sebagai data mentah untuk analisis deskriptif.',
237:'Perbandingan kinerja dilakukan pada satu graf Kota Bandung dengan 10 pasangan titik asal–tujuan dan tiga pengulangan terukur untuk setiap algoritma pada lingkungan yang sama. Variasi ukuran graf belum diuji; dataset demo hanya digunakan dalam pengujian fungsional.',
242:'Berdasarkan latar belakang, identifikasi masalah, dan batasan masalah yang telah diuraikan, rumusan masalah dalam penelitian ini adalah bagaimana menerapkan optimasi algoritma Dijkstra menggunakan antrean prioritas berbasis min-heap dan penghentian dini pada sistem navigasi cerdas berbasis web untuk jaringan jalan Kota Bandung, serta bagaimana perbandingan kinerjanya terhadap implementasi standar dengan pencarian minimum linear berdasarkan waktu eksekusi, jumlah simpul yang diproses, dan jumlah sisi yang diperiksa, dengan kedua implementasi menggunakan adjacency list yang sama dan tetap menghasilkan jalur valid dengan total bobot terpendek yang ekuivalen?',
246:'Tujuan penelitian ini adalah menerapkan optimasi algoritma Dijkstra menggunakan antrean prioritas berbasis min-heap dan penghentian dini dalam sistem navigasi cerdas berbasis web untuk jaringan jalan Kota Bandung. Penelitian membandingkan kinerja implementasi tersebut dengan Dijkstra standar yang menggunakan pemilihan minimum linear, berdasarkan waktu eksekusi, jumlah simpul yang diproses, dan jumlah sisi yang diperiksa. Kedua implementasi menggunakan adjacency list yang sama. Penelitian juga memverifikasi validitas rute dan kesetaraan total bobot minimum pada pasangan titik yang diuji.',
262:'Penelitian difokuskan pada perbandingan Dijkstra standar dengan pemilihan minimum linear dan Dijkstra optimasi menggunakan min-heap serta penghentian dini ketika tujuan telah diselesaikan. Kedua implementasi menggunakan adjacency list yang sama. Aspek yang diteliti meliputi waktu eksekusi, jumlah simpul yang diproses, jumlah sisi yang diperiksa, serta validitas rute dan kesetaraan total bobot.',
273:'Perlakuan yang dibandingkan adalah Dijkstra standar dengan pemilihan minimum linear dan pemrosesan seluruh simpul terjangkau, serta Dijkstra optimasi dengan min-heap dan penghentian dini. Representasi adjacency list digunakan pada kedua implementasi. Variabel respons meliputi waktu eksekusi, jumlah simpul yang diproses, dan jumlah sisi yang diperiksa. Ketepatan hasil diperiksa melalui validitas rute serta kesetaraan total bobot minimum.',
280:'Eksperimen kinerja menggunakan satu graf Kota Bandung dan 10 pasangan titik berbeda yang dipilih secara acak dengan seed 42. Setiap pasangan menjalani satu pemanasan dan tiga pengulangan terukur per algoritma. Urutan pelaksanaan selalu Dijkstra standar kemudian Dijkstra optimasi. Urutan algoritma tidak diacak atau diseimbangkan; potensi pengaruh urutan dan beban perangkat dinyatakan sebagai keterbatasan pada BAB V.',
376:'Sebagai ilustrasi, apabila bobot A–B adalah 4, B–C adalah 2, dan A–C adalah 7, maka lintasan A–B–C memiliki total bobot 6, sedangkan lintasan langsung A–C memiliki bobot 7. Contoh ini menunjukkan bahwa lintasan dengan lebih banyak sisi dapat memiliki total bobot yang lebih kecil.',
399:'Sistem navigasi membantu pengguna menentukan rute dari titik awal menuju tujuan. Yovi dan Sekarwati (2024) menerapkan fungsi tersebut dalam aplikasi navigasi supermarket. Kurniawan dan Atmojo (2025) menggunakannya untuk pencarian rute kunjungan wisata, sedangkan Pramestiana dan Anwar (2025) menerapkannya pada pengiriman kendaraan bermotor. Ketiga penelitian menunjukkan penggunaan algoritma pencarian jalur pada konteks perjalanan yang berbeda.',
431:'Dalam penelitian ini, optimasi diarahkan pada penggunaan antrean prioritas berbasis min-heap dan penghentian dini. Adjacency list dipertahankan pada kedua implementasi sehingga perbedaan representasi graf tidak menjadi perlakuan yang diuji.',
476:'Dalam penelitian ini, dataset, pasangan titik asal–tujuan, dan perangkat pengujian dibuat sama. Namun, urutan algoritma tetap standar kemudian optimasi dan beban perangkat belum sepenuhnya dikendalikan. Pemanasan awal dipisahkan dari pengulangan terukur. Dampak potensial urutan, cache, dan aktivitas perangkat dijelaskan sebagai keterbatasan pada pembahasan hasil.',
541:'Kasus batas yang relevan meliputi asal sama dengan tujuan, tujuan tidak terjangkau, bobot negatif, bobot nol, dan beberapa rute minimum yang setara. Bukti pengujian pada penelitian ini mencakup kesetaraan biaya rute, asal sama dengan tujuan, tujuan tidak terjangkau, dan penolakan bobot negatif. Kasus bobot nol serta beberapa rute minimum yang setara belum menjadi kasus uji khusus dalam laporan pengujian ini.',
550:'Jaringan jalan dimodelkan sebagai graf berbobot nonnegatif dalam bentuk adjacency list yang sama untuk kedua implementasi. Perbandingan dilakukan antara Dijkstra standar dengan pencarian minimum linear dan Dijkstra optimasi dengan min-heap serta penghentian dini. Aplikasi berbasis web digunakan untuk visualisasi dan pelaksanaan pengujian.',
664:'Eksperimen final menggunakan satu graf Kota Bandung, sepuluh pasangan acak dengan seed 42, satu pemanasan, dan tiga pengulangan terukur untuk setiap algoritma pada setiap pasangan. Identitas pasangan dan parameter disimpan pada manifest eksperimen. Variasi ukuran graf belum diuji.',
670:'Menjalankan Dijkstra standar terlebih dahulu, kemudian Dijkstra optimasi pada pasangan titik dan pengulangan yang sama. Kedua algoritma tidak dijalankan secara bersamaan. Urutan tetap ini dicatat sebagai keterbatasan eksperimen.',
}
for i,t in revisions.items():setp(ps[i],t)
setp(ps[298],'Pengujian fungsional memeriksa kesesuaian fitur dengan kebutuhan. Pengujian algoritma memeriksa validitas jalur, kesetaraan total bobot, sumber sama dengan tujuan, tujuan tidak terjangkau, serta penolakan bobot negatif. Kasus beberapa jalur minimum yang setara belum diuji secara khusus. Pengujian kinerja dilaksanakan setelah pemeriksaan ketepatan hasil.')
setp(ps[645],'Pengujian juga mencakup tujuan tidak terjangkau dan sumber sama dengan tujuan. Kesetaraan total bobot diperiksa bersama hasil acuan dan validitas jalur. Kasus beberapa jalur dengan bobot minimum yang sama belum menjadi kasus uji khusus dalam laporan ini.')
setp(ps[678],'Statistik waktu berupa rata-rata, median, minimum, maksimum, dan simpangan baku populasi dihitung dari 30 eksekusi terukur per algoritma. Rata-rata tiga pengulangan juga disajikan untuk setiap pasangan rute. Jumlah simpul dan sisi dibandingkan pada input yang sama. Hasil disajikan dalam tabel, grafik, dan persentase perubahan terhadap baseline.')

id_abs='Penelitian ini bertujuan mengevaluasi ketepatan dan kinerja optimasi algoritma Dijkstra untuk pencarian jalur terpendek pada jaringan jalan Kota Bandung. Sistem dikembangkan berbasis web menggunakan Nuxt dan FastAPI, dengan dataset OpenStreetMap yang diolah melalui OSMnx. Dataset terdiri atas 27.172 simpul dan 61.630 sisi berarah dengan bobot panjang ruas dalam meter. Kedua implementasi menggunakan adjacency list yang sama. Dijkstra standar memilih simpul minimum secara linear dan memproses seluruh simpul yang dapat dijangkau, sedangkan Dijkstra optimasi menggunakan min-heap dan berhenti ketika simpul tujuan telah diselesaikan. Pengujian menggunakan 10 pasangan titik acak, satu pemanasan, dan tiga pengulangan terukur per algoritma per pasangan, sehingga menghasilkan 60 eksekusi terukur. Ketepatan diperiksa melalui validitas rute, kesetaraan biaya, dan pembandingan dengan NetworkX. Seluruh hasil sesuai tanpa ketidaksesuaian pada sampel yang diuji. Rata-rata waktu eksekusi berkurang dari 78.697,65 ms menjadi 25,88 ms atau sekitar 99,97%. Rata-rata jumlah simpul yang diproses berkurang 48,91% dan jumlah sisi yang diperiksa berkurang 48,62%. Hasil menunjukkan manfaat gabungan min-heap dan penghentian dini terhadap baseline yang digunakan. Kesimpulan dibatasi pada satu dataset, satu perangkat, dan sepuluh pasangan yang dapat dijangkau. Urutan algoritma tetap serta beban perangkat yang belum sepenuhnya dikendalikan menjadi keterbatasan pengukuran.'
en_abs='This study evaluates the correctness and performance of an optimized Dijkstra implementation for shortest-path search on the road network of Bandung City. A web-based system was developed using Nuxt and FastAPI with OpenStreetMap data processed through OSMnx. The dataset contains 27,172 nodes and 61,630 directed edges weighted by road-segment length in meters. Both implementations use the same adjacency list. The baseline selects the minimum-distance node by linear scanning and processes all reachable nodes, while the optimized version uses a min-heap and stops when the destination is settled. Testing involved 10 randomly selected origin–destination pairs, one warm-up run, and three measured repetitions per algorithm per pair, producing 60 measured runs. Correctness was checked through route validity, cost agreement, and comparison with NetworkX. All sampled results passed these checks. Mean execution time decreased from 78,697.65 ms to 25.88 ms, a reduction of approximately 99.97%. Mean settled-node and examined-edge counts decreased by 48.91% and 48.62%, respectively. These findings indicate the combined benefit of a min-heap and early termination relative to the tested baseline. Conclusions are limited to one dataset, one computer, and ten reachable pairs. Fixed algorithm order and incompletely controlled system load remain measurement limitations.'
for i,t in [(41,id_abs),(42,'Kata kunci: Dijkstra, jalur terpendek, min-heap, penghentian dini, Kota Bandung.'),(45,en_abs),(46,'Keywords: Dijkstra, shortest path, min-heap, early termination, Bandung City.')]:setp(ps[i],t);fmt(ps[i],True);ps[i].alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
setp(ps[49],'Skripsi berjudul “Optimasi Algoritma Dijkstra untuk Penentuan Jalur Terpendek pada Sistem Navigasi Cerdas” disusun untuk memenuhi salah satu syarat penyelesaian pendidikan pada Program Studi Teknik Informatika STMIK Mardira Indonesia. Penelitian ini membahas implementasi dan evaluasi pencarian rute pada jaringan jalan Kota Bandung. Penulis menyampaikan terima kasih kepada pihak-pihak yang mendukung proses penyusunan skripsi ini. Penulis menyadari bahwa penelitian masih memiliki keterbatasan dan mengharapkan kritik serta saran untuk penyempurnaan selanjutnya. Semoga hasil penelitian dapat menjadi bahan pembelajaran dan pengembangan sistem pencarian rute.')
setp(ps[50],'Bandung, September 2026\nPenulis\n\nZia Ulhaq');ps[50].alignment=WD_ALIGN_PARAGRAPH.RIGHT

# Correct metadata supported by publisher pages; retain unverified entries for a separate review note.
bib={
921:'World Wide Web Consortium. (n.d.). Designing for web accessibility. Web Accessibility Initiative. https://www.w3.org/WAI/tips/designing/',
924:'FastAPI. (n.d.). FastAPI documentation. https://fastapi.tiangolo.com/',
925:'Jackson, G., & Kosinski, M. (n.d.). What is the software development lifecycle (SDLC)? IBM. https://www.ibm.com/think/topics/sdlc',
926:'Microsoft. (n.d.). The TypeScript handbook. https://www.typescriptlang.org/docs/handbook/intro.html',
927:'Python Software Foundation. (n.d.). heapq — Heap queue algorithm. Python documentation. https://docs.python.org/3/library/heapq.html',
929:'Nuxt. (n.d.). Introduction. Nuxt documentation. https://nuxt.com/docs/4.x/getting-started/introduction',
930:'Kurniawan, E. K., & Atmojo, W. T. (2025). Penerapan Algoritma Dijkstra dalam Penentuan Rute Terpendek Kunjungan Wisata Jakarta. ZONAsi: Jurnal Sistem Informasi, 7(2), 445–454. https://journal.unilak.ac.id/index.php/zn/article/view/26342',
932:'Lewis, R. (2023). A comparison of Dijkstra’s algorithm using Fibonacci heaps, binary heaps, and self-balancing binary trees [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2303.10034',
933:'Maurer, S. B., & Ralston, A. (2005). Discrete algorithmic mathematics (3rd ed.). A K Peters/CRC Press. https://www.routledge.com/Discrete-Algorithmic-Mathematics/Maurer-Ralston/p/book/9781568811666',
934:'Google. (n.d.). Model data Cloud Firestore. Firebase documentation. https://firebase.google.com/docs/firestore/data-model?hl=id',
935:'Pramestiana, I., & Anwar, A. (2025). Penentuan Rute Terpendek pada Pengiriman Kendaraan Motor menggunakan Algoritma Dijkstra di PT X. Jurnal Logic: Logistics & Supply Chain Center, 3(2), 69–77. https://doi.org/10.33197/jlscc.v3i2.2480',
937:'Tian, T., Wu, H., Wei, H., Wu, F., & Xu, M. (2025). An efficient route planning algorithm for special vehicles with large-scale road network data. ISPRS International Journal of Geo-Information, 14(2), 71. https://doi.org/10.3390/ijgi14020071',
938:'Yovi, M., & Sekarwati, K. A. (2024). Aplikasi Navigasi Supermarket Berbasis Web Menggunakan Algoritma Dijkstra. Jurnal Ilmiah Komputasi, 23(4), 505–512. https://doi.org/10.32409/jikstik.23.4.3606',
}
for i,t in bib.items():setp(ps[i],t);fmt(ps[i],True)
for p in doc.paragraphs:
 for a,b in [('Maurer & Ralston, 2020','Maurer & Ralston, 2005'),('((WAI), n.d.)','(World Wide Web Consortium, n.d.)'),('“FastAPI¶,” n.d.','FastAPI, n.d.'),('“Handbook - The TypeScript Handbook,” n.d.','Microsoft, n.d.'),('“heapq — Heap queue algorithm,” n.d.','Python Software Foundation, n.d.'),('“Introduction · Get Started with Nuxt v4,” n.d.','Nuxt, n.d.'),('“Model data Cloud Firestore\u00a0 |\u00a0 Firebase,” n.d.','Google, n.d.'),('Gita Jackson, n.d.','Jackson & Kosinski, n.d.')]:patch(p,a,b)
# Sort the bibliography paragraphs without moving the document section boundary.
refs=ps[921:939]
for p in refs:
 fmt(p,True)
 p.paragraph_format.left_indent=Cm(1)
 p.paragraph_format.first_line_indent=Cm(-1)
 p.paragraph_format.space_after=Pt(12)
for p in sorted(refs,key=lambda p:p.text.casefold()):ps[919]._p.getparent().insert(ps[919]._p.getparent().index(ps[919]._p)+1,p._p)
# Reverse the preceding insertion sequence to obtain ascending order.
for p in sorted(refs,key=lambda p:p.text.casefold(),reverse=True):ps[919]._p.addnext(p._p)

anchor=ps[207]
head=anchor.insert_paragraph_before('DAFTAR GAMBAR',style='Heading 1');head.paragraph_format.page_break_before=True
field=anchor.insert_paragraph_before();r=field.add_run();b=OxmlElement('w:fldChar');b.set(qn('w:fldCharType'),'begin');r._r.append(b)
code=OxmlElement('w:instrText');code.text=' TOC \\h \\z \\c "Gambar" ';r._r.append(code)
sep=OxmlElement('w:fldChar');sep.set(qn('w:fldCharType'),'separate');r._r.append(sep);field.add_run('Daftar gambar diperbarui otomatis.')
end=OxmlElement('w:fldChar');end.set(qn('w:fldCharType'),'end');field.add_run()._r.append(end)
anchor.paragraph_format.page_break_before=True
setp(ps[208],'G: graf; V: himpunan simpul; E: himpunan sisi; w(u, v): bobot sisi; d(v): jarak sementara dari sumber ke simpul v; P: lintasan; W(P): total bobot lintasan; ∞: tak hingga; ε: toleransi numerik; O: notasi batas kompleksitas.');fmt(ps[208],True)

# Add concise factual appendices based on archived experiment files.
h=doc.add_paragraph('LAMPIRAN',style='Heading 1');h.paragraph_format.page_break_before=True
h=doc.add_paragraph('Lampiran A Metadata dan Konfigurasi Eksperimen',style='Heading 2')
manifest=json.loads((ROOT/'artifacts/bab5/manifest.json').read_text())
q=doc.add_paragraph('Dataset kota-bandung-osm-drive versi 1.0.0; 27.172 simpul dan 61.630 sisi berarah; sumber OpenStreetMap; ekstraksi 16 September 2026 WIB. Pengujian 17 September 2026 menggunakan 10 pasangan, seed 42, satu pemanasan, dan tiga pengulangan per algoritma. Identitas eksperimen: df42b09c75c1402ab235da6b5a2ab4b7.');fmt(q)
q=doc.add_paragraph('SHA-256 dataset: '+manifest['datasetSha256']);fmt(q,True);q.runs[0].font.size=Pt(10)
doc.add_paragraph('Lampiran B Hasil Pemeriksaan Pengujian',style='Heading 2')
q=doc.add_paragraph('Sembilan tes backend dan enam pemeriksaan antarmuka lulus. Pemeriksaan NetworkX dan validitas rute menyatakan seluruh 60 eksekusi terukur sesuai. Daftar pasangan dan jarak acuan tercantum pada Tabel 5.6. Arsip pendukung terdiri atas manifest.json, benchmark.json, raw-runs.csv, correctness.json, pytest.xml, ui-tests.json, dan provenance.json.');fmt(q)
doc.add_paragraph('Lampiran C Ringkasan Waktu per Pasangan',style='Heading 2')
stats=json.loads((ROOT/'artifacts/bab5/pair-statistics.json').read_text())
t=doc.add_table(rows=1,cols=3);t.style='Table Grid'
for c,s in zip(t.rows[0].cells,['Pasangan','Standar (ms)','Optimasi (ms)']):c.text=s
for i in range(1,11):
 vals=[next(x['meanMs'] for x in stats if x['pair']==f'P{i}' and x['algorithm']==a) for a in ['standard','optimized']]
 row=t.add_row()
 for c,s in zip(row.cells,[f'P{i}']+[f'{v:.2f}'.replace('.',',') for v in vals]):c.text=s
for row in t.rows:
 for c in row.cells:
  for p in c.paragraphs:fmt(p,True)
for s in doc.styles:
 if s.type==1 and s.name.startswith('Heading'):
  s.font.color.rgb=RGBColor(0,0,0)
for p in doc.paragraphs:
 if p.text in ['DAFTAR GAMBAR','LAMPIRAN'] or p.text.startswith('Lampiran '):
  pr=p._p.get_or_add_pPr()
  old=pr.find(qn('w:numPr'))
  if old is not None:pr.remove(old)
  num=OxmlElement('w:numPr');val=OxmlElement('w:numId');val.set(qn('w:val'),'0');num.append(val);pr.append(num)
settings=doc.settings.element
# Keep table rows intact and repeat the header when a table spans pages.
for table in doc.tables:
 for index,row in enumerate(table.rows):
  pr=row._tr.get_or_add_trPr()
  if pr.find(qn('w:cantSplit')) is None:pr.append(OxmlElement('w:cantSplit'))
  if index==0 and pr.find(qn('w:tblHeader')) is None:pr.append(OxmlElement('w:tblHeader'))
# The bibliography and appendices use a separate, unnumbered back-matter section.
boundary=ps[919].insert_paragraph_before()
section=deepcopy(doc.sections[-1]._sectPr)
boundary._p.get_or_add_pPr().append(section)
last=doc.sections[-1]
page_number=last._sectPr.find(qn('w:pgNumType'))
if page_number is not None:page_number.attrib.pop(qn('w:start'),None)
last.footer.is_linked_to_previous=False
for p in last.footer.paragraphs:p.clear()
last.first_page_footer.is_linked_to_previous=False
for p in last.first_page_footer.paragraphs:p.clear()
last.even_page_footer.is_linked_to_previous=False
for p in last.even_page_footer.paragraphs:p.clear()
u=OxmlElement('w:updateFields');u.set(qn('w:val'),'true');settings.append(u)
out=ROOT/'artifacts/review-draft/Skripsi_Zia_Ulhaq_Revisi.docx'
doc.save(out)
(out.parent/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
