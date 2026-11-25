from pathlib import Path
from pdf2image import convert_from_path
from pypdf import PdfReader
from PIL import Image,ImageDraw
p=Path(__file__).parent
for name in ['Naskah_Presentasi_Sidang_Zia_Ulhaq','Panduan_Dijkstra_dan_Aplikasi_Zia_Ulhaq']:
 dest=p/name;dest.mkdir(exist_ok=True)
 pages=convert_from_path(str(p/(name+'.pdf')),dpi=90,poppler_path=r'C:\Users\ervid\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
 texts=[page.extract_text() or '' for page in PdfReader(p/(name+'.pdf')).pages]
 (dest/'text.txt').write_text('\n\n'.join(f'PAGE {i+1}\n{t}' for i,t in enumerate(texts)),encoding='utf8')
 for i,im in enumerate(pages):im.save(dest/f'page-{i+1}.png')
 for start in range(0,len(pages),6):
  sheet=Image.new('RGB',(1500,1420),'#dddddd');draw=ImageDraw.Draw(sheet)
  for j,im in enumerate(pages[start:start+6]):
   im=im.copy();im.thumbnail((480,680));x=(j%3)*500;y=(j//3)*710;sheet.paste(im,(x,y+20));draw.text((x+5,y+2),str(start+j+1),fill='black')
  sheet.save(dest/f'contact-{start//6+1}.png')
 print(name,len(pages),'pages',[(i+1,len(t)) for i,t in enumerate(texts)])
