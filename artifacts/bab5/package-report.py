"""Package the verified chapter and evidence without external assets."""
from pathlib import Path
import re,html,base64,zipfile
folder=Path(__file__).resolve().parent
root=folder.parents[1]
source=root/'docs/BAB_V_Implementasi_dan_Pengujian_Sistem.md'
lines=source.read_text(encoding='utf-8').splitlines()
def inline(s):
    s=html.escape(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
parts=[]; i=0
while i<len(lines):
    line=lines[i].strip()
    if not line:
        i+=1; continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',c) for c in cells): rows.append(cells)
            i+=1
        parts.append('<table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table>')
        continue
    image=re.fullmatch(r'!\[([^]]*)\]\(([^)]+)\)',line)
    if image:
        path=(source.parent/image.group(2)).resolve()
        data=base64.b64encode(path.read_bytes()).decode('ascii')
        caption=''
        j=i+1
        while j<len(lines) and not lines[j].strip(): j+=1
        if j<len(lines) and lines[j].startswith('**Gambar'):
            caption='<figcaption>'+inline(lines[j])+'</figcaption>'
            i=j
        parts.append('<figure><img alt="'+html.escape(image.group(1),quote=True)+'" src="data:image/png;base64,'+data+'">'+caption+'</figure>')
    elif line.startswith('#'):
        level=len(line)-len(line.lstrip('#'))
        parts.append(f'<h{level}>'+inline(line[level:].strip())+f'</h{level}>')
    else:
        parts.append('<p'+(' class="table-caption"' if line.startswith('**Tabel') else '')+'>'+inline(line)+'</p>')
    i+=1
css='''body{font:12pt/1.8 "Times New Roman",serif;color:#111;max-width:820px;margin:40px auto;padding:0 28px}h1{text-align:center;font-size:14pt;margin:0;line-height:1.5}h2{font-size:12pt;margin:24px 0 8px}h3{font-size:12pt;margin:18px 0 8px}p{text-align:justify;margin:0 0 12px}table{border-collapse:collapse;width:100%;font-size:10.5pt;line-height:1.3;margin-bottom:18px}th,td{border:1px solid #555;padding:6px 8px;vertical-align:top}th{background:#f0f0f0;text-align:left}thead{display:table-header-group}tr{break-inside:avoid}.table-caption{font-weight:bold;margin-bottom:6px;break-after:avoid}figure{margin:18px 0;break-inside:avoid}img{width:100%;height:auto;display:block}figcaption{text-align:center;font-size:11pt;line-height:1.35;margin-top:8px}code{font-family:inherit;overflow-wrap:anywhere}h2,h3{break-after:avoid}@page{size:A4;margin:40mm 30mm 30mm 40mm}@media print{body{max-width:none;margin:0;padding:0;line-height:2}p{margin:0;text-indent:1cm}h2,h3{margin:12px 0 0}.table-caption{margin-top:10px;text-indent:0}table{font-size:10pt}figure{margin:10px 0}}'''
html_path=source.with_suffix('.html')
html_path.write_text('<!doctype html><html lang="id"><head><meta charset="utf-8"><title>BAB V Implementasi dan Pengujian Sistem</title><style>'+css+'</style></head><body>'+''.join(parts)+'</body></html>',encoding='utf-8')
names=['README.md','manifest.json','benchmark.json','raw-runs.csv','correctness.json','provenance.json','pytest.xml','ui-tests.json','ui-bandung-route.json','pair-statistics.json','evidence-sha256.json','grafik-waktu.png','grafik-waktu.svg','implementasi-simulator-bandung.png','implementasi-comparison-demo.png','implementasi-benchmark-demo.png','implementasi-history-demo.png','finalize-report.py','package-report.py','capture-ui.cjs','bab5-template.md']
with zipfile.ZipFile(root/'artifacts/BAB_V_Naskah_dan_Bukti.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for path in [source,html_path,root/'backend/scripts/run_thesis_experiment.py']+[folder/n for n in names]:
        archive.write(path,path.relative_to(root))
print(html_path)
print(root/'artifacts/BAB_V_Naskah_dan_Bukti.zip')
