from pathlib import Path
from pypdf import PdfReader
from pdf2image import convert_from_path
from PIL import Image,ImageDraw
import json
p=Path(__file__).resolve().parent
pdf=p/'Skripsi_Zia_Ulhaq_Revisi.pdf'
reader=PdfReader(pdf)
texts=[page.extract_text() or '' for page in reader.pages]
(p/'rendered-text.txt').write_text('\n\n'.join(f'PAGE {i+1}\n{t}' for i,t in enumerate(texts)),encoding='utf-8')
print('Pages',len(texts),'nearly blank',[(i+1,t.strip()) for i,t in enumerate(texts) if len(t.strip())<35])
png=p/'pages';png.mkdir(exist_ok=True)
paths=convert_from_path(str(pdf),dpi=90,fmt='png',output_folder=str(png),paths_only=True,thread_count=2,poppler_path=r'C:\Users\ervid\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
for start in range(0,len(paths),9):
 sheet=Image.new('RGB',(1500,2220),'#dddddd');d=ImageDraw.Draw(sheet)
 for j,path in enumerate(paths[start:start+9]):
  im=Image.open(path);im.thumbnail((480,700));x=(j%3)*500;y=(j//3)*740
  sheet.paste(im,(x,y+25));d.text((x+5,y+4),f'PAGE {start+j+1}',fill='black')
 sheet.save(p/f'contact-{start//9+1:02}.png')
(p/'page-paths.json').write_text(json.dumps(paths),encoding='utf-8')
print('Rendered',len(paths),'pages')
