from pathlib import Path
import json, statistics, hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

folder = Path(__file__).resolve().parent
project = folder.parents[1]
payload = json.loads((folder/'benchmark.json').read_text(encoding='utf-8'))
checks = json.loads((folder/'correctness.json').read_text(encoding='utf-8'))
manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
assert len(payload['runs']) == 60 and len(checks) == 10
assert all(c['valid'] and c['runCount']==6 for c in checks)
assert payload['summary']['correctnessMismatchCount'] == 0
def num(value, places=2):
    return f'{value:,.{places}f}'.replace(',', '_').replace('.', ',').replace('_', '.')

summary=payload['summary']
standard=summary['standard']; optimized=summary['optimized']
correctness='**Tabel 5.6 Hasil Pemeriksaan Ketepatan Rute**\n\n| Pasangan | Simpul asal | Simpul tujuan | Jarak acuan (meter) | Kesesuaian seluruh pengulangan |\n|---|---|---|---:|---|\n'
for i,c in enumerate(checks,1):
    correctness+=f"| P{i} | {c['sourceId']} | {c['destinationId']} | {num(c['referenceCost']) if c['referenceCost'] is not None else 'Tidak terjangkau'} | Sesuai |\n"
success=sum(c['referenceCost'] is not None for c in checks)
correctness_text=f'Sebanyak {success} dari 10 pasangan memiliki rute yang dapat dijangkau. Seluruh 60 hasil eksekusi sesuai dengan pemeriksaan status, biaya, dan validitas rute. Tidak ditemukan pasangan yang mengalami ketidaksesuaian antara kedua algoritma pada toleransi yang ditetapkan. Jarak pada tabel dibulatkan untuk penyajian; pemeriksaan dilakukan menggunakan nilai tanpa pembulatan. Hasil ini menunjukkan kesesuaian pada sampel yang diuji, bukan bukti empiris untuk seluruh kemungkinan pasangan simpul.'
metrics=[('Rata-rata waktu (ms)','meanExecutionTimeMs',1),('Median waktu (ms)','medianExecutionTimeNs',1e-6),('Waktu minimum (ms)','minimumExecutionTimeNs',1e-6),('Waktu maksimum (ms)','maximumExecutionTimeNs',1e-6),('Simpangan baku populasi waktu (ms)','standardDeviationExecutionTimeNs',1e-6),('Rata-rata simpul diproses','meanVisitedNodes',1),('Rata-rata sisi diperiksa','meanProcessedEdges',1)]
performance='**Tabel 5.7 Perbandingan Kinerja Algoritma**\n\n| Metrik | Dijkstra standar | Dijkstra optimasi |\n|---|---:|---:|\n'
for label,key,factor in metrics:
    performance+=f'| {label} | {num(standard[key]*factor)} | {num(optimized[key]*factor)} |\n'
improvement=summary['improvement']
ratio=standard['meanExecutionTimeNs']/optimized['meanExecutionTimeNs']
performance_text=f"Pada sesi pengujian ini, rata-rata waktu Dijkstra standar adalah {num(standard['meanExecutionTimeMs'])} ms, sedangkan Dijkstra optimasi adalah {num(optimized['meanExecutionTimeMs'])} ms. Pengurangan rata-rata waktu mencapai {num(improvement['executionTimePct'])}%, dengan rasio waktu standar terhadap optimasi sebesar {num(ratio)} kali. Rata-rata jumlah simpul yang diproses berkurang {num(improvement['visitedNodesPct'])}% dan jumlah sisi yang diperiksa berkurang {num(improvement['processedEdgesPct'])}%. Persentase dihitung sebelum pembulatan nilai pada tabel."
discussion=f"Hasil pengujian menunjukkan bahwa Dijkstra optimasi mempertahankan jarak minimum pada sepuluh pasangan yang diperiksa sekaligus membutuhkan waktu eksekusi lebih rendah secara agregat. Baseline menggunakan pencarian minimum linear dan menyelesaikan seluruh simpul yang dapat dijangkau dari asal. Pada sampel ini, baseline memproses rata-rata {num(standard['meanVisitedNodes'],0)} simpul per eksekusi. Optimasi menggunakan min-heap dan berhenti ketika tujuan diselesaikan, dengan rata-rata {num(optimized['meanVisitedNodes'])} simpul per eksekusi."
discussion+='\n\nBesarnya rasio waktu harus ditafsirkan terhadap baseline yang digunakan. Hasil tersebut tidak berarti bahwa setiap implementasi Dijkstra akan memperoleh percepatan yang sama. Pengujian belum membandingkan min-heap tanpa penghentian dini atau pencarian linear dengan penghentian dini, sehingga kontribusi masing-masing perubahan tidak dapat dinyatakan secara terpisah.'

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
pair_stats=[]
for alg,label,marker,color in [('standard','Dijkstra standar','o','#444444'),('optimized','Dijkstra optimasi','s','#1765a3')]:
    means=[]; lows=[]; highs=[]
    for c in checks:
        values=[r['executionTimeMs'] for r in payload['runs'] if r['algorithm']==alg and r['sourceId']==c['sourceId'] and r['destinationId']==c['destinationId']]
        mean=statistics.mean(values)
        means.append(mean); lows.append(mean-min(values)); highs.append(max(values)-mean)
        pair_stats.append({'pair':f'P{len(means)}','algorithm':alg,'meanMs':mean,'minMs':min(values),'maxMs':max(values)})
    ax.errorbar(range(1,11),means,yerr=[lows,highs],label=label,marker=marker,color=color,capsize=3,linewidth=1.5)
ax.set_yscale('log'); ax.set_xticks(range(1,11),[f'P{i}' for i in range(1,11)])
ax.set_ylabel('Waktu eksekusi (ms; skala logaritmik)'); ax.set_xlabel('Pasangan titik asal–tujuan')
ax.grid(axis='y',alpha=.25); ax.legend(loc='best')
ax.set_title('Kota Bandung: rata-rata tiga pengulangan per pasangan\nGaris galat menunjukkan rentang minimum–maksimum',fontsize=12)
fig.savefig(folder/'grafik-waktu.png',dpi=240)
fig.savefig(folder/'grafik-waktu.svg')
plt.close(fig)
(folder/'pair-statistics.json').write_text(json.dumps(pair_stats,indent=2),encoding='utf-8')
text=(folder/'bab5-template.md').read_text(encoding='utf-8')
for key,value in {'CORRECTNESS_TABLE':correctness,'CORRECTNESS_TEXT':correctness_text,'PERFORMANCE_TABLE':performance,'PERFORMANCE_TEXT':performance_text,'DISCUSSION':discussion}.items():
    text=text.replace('{{'+key+'}}',value)
assert '{{' not in text
dest=project/'docs/BAB_V_Implementasi_dan_Pengujian_Sistem.md'
dest.write_text(text,encoding='utf-8')
evidence={name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ['benchmark.json','manifest.json','correctness.json','raw-runs.csv','pytest.xml','ui-tests.json']}
(folder/'evidence-sha256.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(performance)
print(performance_text)
print(dest)
