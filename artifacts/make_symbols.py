from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
P=Path(__file__).parent/'daftar-simbol';P.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26)
def symbol(kind):
 im=Image.new('RGB',(440,180),'white');d=ImageDraw.Draw(im);k='black';w=4
 def line(x):d.line(x,fill=k,width=w)
 def arrow(x1,y1,x2,y2,dashed=False,filled=False):
  if dashed:
   for x in range(x1,x2,20):line((x,y1,min(x+11,x2),y2))
  else:line((x1,y1,x2,y2))
  pts=[(x2-18,y2-10),(x2,y2),(x2-18,y2+10)]
  if filled:d.polygon(pts,fill=k)
  else:line(pts)
 if kind in ['oval','use']:d.ellipse((70,40,370,140),outline=k,width=w)
 elif kind=='process':d.rectangle((65,40,375,140),outline=k,width=w)
 elif kind=='action':d.rounded_rectangle((65,40,375,140),radius=22,outline=k,width=w)
 elif kind=='io':d.polygon([(100,40),(385,40),(340,140),(55,140)],outline=k,width=w)
 elif kind in ['decision','merge']:d.polygon([(220,20),(360,90),(220,160),(80,90)],outline=k,width=w)
 elif kind in ['arrow','sync','return','include','extend']:
  arrow(45,105,395,105,kind in ['return','include','extend'],kind=='sync')
  if kind in ['include','extend']:d.text((220,60),'«'+kind+'»',font=font,fill=k,anchor='mm')
 elif kind=='connector':d.ellipse((165,35,275,145),outline=k,width=w)
 elif kind=='sub':
  d.rectangle((65,40,375,140),outline=k,width=w);line((90,40,90,140));line((350,40,350,140))
 elif kind=='db':
  d.arc((100,115,340,165),0,180,fill=k,width=w);line((100,45,100,140));line((340,45,340,140));d.ellipse((100,20,340,70),outline=k,width=w)
 elif kind=='actor':
  d.ellipse((200,10,240,50),outline=k,width=w);line((220,50,220,110));line((170,75,270,75));line((220,110,175,165));line((220,110,265,165))
 elif kind=='association':line((50,90,390,90))
 elif kind=='boundary':
  d.rectangle((65,15,375,165),outline=k,width=w);d.text((220,42),'Sistem',font=font,fill=k,anchor='mm')
 elif kind=='initial':d.ellipse((185,55,255,125),fill=k)
 elif kind=='final':d.ellipse((165,35,275,145),outline=k,width=w);d.ellipse((185,55,255,125),fill=k)
 elif kind=='fork':d.rectangle((65,80,375,99),fill=k)
 elif kind=='swim':
  d.rectangle((45,15,395,165),outline=k,width=w);line((220,15,220,165));line((45,60,395,60));d.text((130,38),'Pengguna',font=font,fill=k,anchor='mm');d.text((305,38),'Sistem',font=font,fill=k,anchor='mm')
 elif kind=='participant':
  d.rectangle((65,35,375,140),outline=k,width=w);d.text((220,87),'Antarmuka',font=font,fill=k,anchor='mm')
 elif kind=='lifeline':
  for y in range(10,170,22):line((220,y,220,y+12))
 elif kind=='activation':d.rectangle((200,15,240,165),outline=k,width=w)
 elif kind=='fragment':
  d.rectangle((45,15,395,165),outline=k,width=w);line([(45,60),(120,60),(140,40),(140,15)]);d.text((88,37),'alt',font=font,fill=k,anchor='mm');
  for x in range(45,395,20):line((x,95,x+10,95))
 path=P/(kind+'.png');im.save(path);return path
sections=[('A Simbol Flowchart',[
 ('oval','Terminator','Awal atau akhir proses.'),('process','Process','Kegiatan pengolahan atau perhitungan.'),('io','Input/Output','Masukan atau keluaran data.'),('decision','Decision','Percabangan berdasarkan kondisi.'),('arrow','Flowline','Arah dan urutan proses.'),('connector','On-page Connector','Penghubung alur pada halaman yang sama.'),('sub','Predefined Process','Pemanggilan subproses yang dijelaskan terpisah.'),('db','Database','Tempat penyimpanan data.')]),
 ('B Simbol Use Case Diagram',[
 ('actor','Actor','Peran pengguna atau sistem eksternal.'),('use','Use Case','Fungsi atau layanan sistem bagi aktor.'),('association','Association','Hubungan aktor dengan use case.'),('boundary','System Boundary','Batas sistem yang dirancang.'),('include','Include','Penyertaan perilaku use case lain; panah menuju use case yang disertakan.'),('extend','Extend','Perilaku tambahan bersyarat; panah menuju use case yang diperluas.')]),
 ('C Simbol Activity Diagram',[
 ('initial','Initial Node','Titik awal aktivitas.'),('action','Action','Tindakan pengguna atau sistem.'),('arrow','Control Flow','Arah perpindahan kendali.'),('decision','Decision Node','Pemilihan alur berdasarkan kondisi.'),('merge','Merge Node','Penggabungan alur alternatif. Bentuk sama dengan decision, tetapi susunan alurnya berbeda.'),('fork','Fork/Join Node','Pemisahan atau penyatuan alur paralel.'),('final','Activity Final Node','Akhir seluruh aktivitas.'),('swim','Swimlane','Pembagian tanggung jawab aktivitas.')]),
 ('D Simbol Sequence Diagram',[
 ('participant','Participant','Pihak atau komponen yang berinteraksi.'),('lifeline','Lifeline','Keberadaan partisipan sepanjang interaksi.'),('activation','Activation','Periode pelaksanaan proses oleh partisipan.'),('sync','Synchronous Message','Pemanggilan operasi yang menunggu penyelesaian penerima.'),('return','Return Message','Respons atau hasil yang dikembalikan.'),('fragment','Combined Fragment','Kelompok interaksi: alt untuk alternatif, opt untuk opsional, dan loop untuk pengulangan.')])]
doc=Document();sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.top_margin=Cm(4);sec.bottom_margin=Cm(3);sec.left_margin=Cm(4);sec.right_margin=Cm(3)
for name in ['Normal','Title','Heading 1','Heading 2']:
 s=doc.styles[name];s.font.name='Times New Roman';s.font.size=Pt(12);s.font.color.rgb=RGBColor(0,0,0)
 s.paragraph_format.space_after=Pt(6);s.paragraph_format.line_spacing=1
 for node in list(s.element.xpath('.//w:pBdr')):node.getparent().remove(node)
 rf=s.element.get_or_add_rPr().find(qn('w:rFonts'))
 if rf is not None:
  for a in list(rf.attrib):
   if a.endswith('Theme'):del rf.attrib[a]
def heading(title,first=False):
 if not first:doc.add_page_break()
 h=doc.add_paragraph('DAFTAR SIMBOL',style='Title');h.alignment=1;h.runs[0].bold=True
 h=doc.add_paragraph(title,style='Heading 2');h.runs[0].bold=True
def table(rows,draw=True):
 t=doc.add_table(rows=1,cols=4);t.style='Table Grid';t.autofit=False
 widths=[.9,3.1,3.3,6.7]
 for col,wi in zip(t.columns,widths):col.width=Cm(wi)
 for c,txt in zip(t.rows[0].cells,['No','Simbol','Nama','Keterangan']):c.text=txt
 t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 for i,(sym,name,desc) in enumerate(rows,1):
  cells=t.add_row().cells
  for c,wi in zip(cells,widths):c.width=Cm(wi)
  cells[0].text=str(i);cells[2].text=name;cells[3].text=desc
  if draw:cells[1].paragraphs[0].add_run().add_picture(str(symbol(sym)),width=Cm(2.8))
  else:cells[1].text=sym
 for ri,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for ci,c in enumerate(row.cells):
   c.width=Cm(widths[ci])
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for p in c.paragraphs:
    p.paragraph_format.space_before=Pt(4);p.paragraph_format.space_after=Pt(4)
    if ci<2:p.alignment=1
    for r in p.runs:r.font.size=Pt(11);r.bold=(ri==0)
for i,(title,rows) in enumerate(sections):heading(title,i==0);table(rows)
heading('E Notasi Graf dan Algoritma Dijkstra')
table([(a,b,c) for a,b,c in [
 ('G = (V, E)','Graf','Graf dengan himpunan simpul V dan sisi E.'),('V','Himpunan simpul','Seluruh simpul pada graf.'),('E','Himpunan sisi','Seluruh sisi pada graf.'),('u, v','Simpul','Simpul dalam pembahasan algoritma.'),('(u, v)','Sisi berarah','Sisi dari simpul u menuju v.'),('w(u, v)','Bobot sisi','Panjang ruas dari u menuju v dalam meter.'),('s','Sumber','Simpul awal pencarian.'),('t','Tujuan','Simpul tujuan pencarian.'),('d(v)','Jarak sementara','Jarak terbaik yang diketahui dari s menuju v.'),('prev(v)','Pendahulu','Simpul pendahulu untuk rekonstruksi jalur.'),('Q','Antrean prioritas','Antrean simpul pada implementasi min-heap.'),('P','Lintasan','Lintasan dari sumber menuju tujuan.'),('W(P)','Bobot lintasan','Jumlah bobot sisi pada lintasan P.'),('|V|, |E|','Ukuran graf','Jumlah simpul dan jumlah sisi.'),('∞','Tak hingga','Nilai awal jarak simpul selain sumber.'),('ε','Toleransi','Toleransi numerik pemeriksaan kesetaraan.'),('O(·)','Kompleksitas','Notasi batas atas pertumbuhan kompleksitas.')]],False)
doc.save(P/'Daftar_Simbol_Skripsi.docx');print(P/'Daftar_Simbol_Skripsi.docx')

