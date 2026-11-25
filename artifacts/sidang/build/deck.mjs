import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const root='C:/Dev/Web/dijkstra-route-optimization';
const work=root+'/artifacts/sidang', build=work+'/build';
const skill='C:/Users/ervid/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.61513/skills/presentations';
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs'));
const data=JSON.parse(await fs.readFile(build+'/slides.json','utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const C={ink:'#142D3D',muted:'#536671',accent:'#007F78',paper:'#F8FAFA',white:'#FFFFFF'};
const font='Arial';
function text(s,t,x,y,w,h,size=28,bold=false,color=C.ink){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=t;sh.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none'};return sh;
}
function lines(s,items,x=76,y=180,w=1100,gap=103,size=31){items.forEach((t,i)=>text(s,t,x,y+i*gap,w,gap-15,size));}
function table(s,values,{x=76,y=185,w=1128,h=350,widths,size=26}={}){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,...(widths?{columnWidths:widths}:{})});
 t.borders.assign({fill:'#D3DFE3',width:1,style:'solid'});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
  const cell=t.getCell(r,c);cell.fill=r===0?C.ink:(r%2?C.white:'#EDF3F4');
  cell.text.style={typeface:font,fontSize:size,bold:r===0,color:r===0?C.white:C.ink};
 }
 return t;
}
async function picture(s,file,x,y,w,h){s.images.add({blob:new Uint8Array(await fs.readFile(root+'/artifacts/bab5/'+file)),contentType:'image/png',fit:'contain',position:{left:x,top:y,width:w,height:h},alt:file});}
for(let i=0;i<data.length;i++){
 const d=data[i],s=p.slides.add();s.background.fill=C.paper;
 if(i===0){
  s.background.fill=C.ink;
  text(s,'SIDANG SKRIPSI',80,65,1000,45,24,true,'#75D6C5');
  text(s,'Optimasi Algoritma\nDijkstra',80,175,1100,175,65,true,C.white);
  text(s,'untuk Penentuan Jalur Terpendek\npada Sistem Navigasi Cerdas',84,366,1060,112,38,false,C.white);
  text(s,'Zia Ulhaq  •  21110383',84,550,1060,45,29,true,C.white);
  text(s,'Teknik Informatika  |  STMIK Mardira Indonesia',84,604,1080,45,24,false,'#CAD8DE');
 }else{
  text(s,d.title,76,53,1128,104,d.title.length>43?40:44,true);
  text(s,String(i+1).padStart(2,'0')+(i>=16?'  /  CADANGAN':''),76,665,470,30,18,false,C.muted);
  switch(d.kind){
   case 'data':
    text(s,'27.172',76,188,500,104,86,true,C.accent);text(s,'simpul',80,292,500,45,30);
    text(s,'61.630',686,188,500,104,86,true,C.accent);text(s,'sisi berarah',690,292,500,45,30);
    lines(s,['Jaringan kendaraan Kota Bandung dari OpenStreetMap','OSMnx membentuk graf dengan bobot panjang ruas dalam meter','Snapshot 16 September 2026, tanpa lalu lintas waktu nyata'],80,405,1110,63,27);break;
   case 'example':
    table(s,[['Dari','Ke','Bobot'],['A','B','4'],['A','C','2'],['C','B','1'],['C','D','8'],['B','D','4'],['D','E','2']],{x:76,y:170,w:540,h:430,size:26});
    lines(s,['Simpul: lokasi','Sisi: hubungan searah','Bobot: panjang atau biaya','Tujuan contoh: A menuju D'],685,200,520,94,30);break;
   case 'walkthrough':
    table(s,[['Simpul diproses','B','C','D','E'],['A','4','2','∞','∞'],['C','3','2','10','∞'],['B','3','2','7','∞'],['D final','3','2','7','∞']],{y:175,h:330,widths:[408,180,180,180,180]});
    text(s,'Rute minimum A–C–B–D = 2 + 1 + 4 = 7',80,548,1120,52,34,true,C.accent);
    text(s,'D pertama ditemukan dengan biaya 10, kemudian membaik menjadi 7.',80,611,1100,40,24);break;
   case 'comparison':
    table(s,[['Aspek','Standar','Optimasi'],['Graf','Adjacency list','Adjacency list yang sama'],['Minimum','Pemindaian linear','Min-heap'],['Batas pencarian','Seluruh simpul terjangkau','Tujuan sudah final'],['Relaksasi','Perbarui jika lebih kecil','Aturan yang sama']],{y:180,h:360,widths:[230,430,468],size:27});
    text(s,'Eksperimen mengukur pengaruh gabungan heap dan penghentian dini.',80,575,1110,60,28,true,C.accent);break;
   case 'screenshot':
    await picture(s,'implementasi-simulator-bandung.png',76,157,1128,467);
    text(s,'Tangkapan pengujian sebelumnya. Data dan peta © OpenStreetMap contributors.',80,627,1110,29,19);break;
   case 'correctness':
    text(s,'60 / 60',76,188,560,124,88,true,C.accent);text(s,'hasil sesuai pada sampel uji',80,313,1050,60,38);
    lines(s,['Rute valid, total biaya sesuai, pembanding NetworkX','9 tes backend dan 6 pemeriksaan antarmuka lulus','Seluruh 10 pasangan terjangkau'],80,417,1100,63,28);break;
   case 'timing':
    table(s,[['Waktu (ms)','Standar','Optimasi'],['Rata-rata','78.697,65','25,88'],['Median','77.896,86','26,65'],['Minimum','77.125,11','7,13'],['Maksimum','86.962,58','40,11']],{y:174,h:336,widths:[408,360,360],size:29});
    text(s,'99,97%',80,544,330,85,62,true,C.accent);
    text(s,'pengurangan rata-rata waktu algoritma\npada baseline dan sesi pengujian ini',430,554,755,78,29);
    break;
   case 'chart':{
    const ch=s.charts.add('bar',{position:{left:76,top:165,width:1128,height:408},categories:['Simpul diselesaikan','Sisi diperiksa'],series:[{name:'Standar',valuesFormatCode:'#,##0.0',values:[25610,59072],fill:'#6C8190'},{name:'Optimasi',valuesFormatCode:'#,##0.0',values:[13084.3,30351.8],fill:C.accent}],barOptions:{direction:'column',grouping:'clustered',gapWidth:150},hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:font,fontSize:24}},yAxis:{min:0,max:70000,numberFormatCode:'#,##0',textStyle:{fontFamily:font,fontSize:21}},xAxis:{textStyle:{fontFamily:font,fontSize:23}},dataLabels:{showValue:true,position:'outEnd',textStyle:{fontFamily:font,fontSize:22}},chartFill:C.paper,plotAreaFill:C.paper});
    applyPresentationChartFont(ch,{fontFamily:font});
    text(s,'Rata-rata per eksekusi. Penurunan simpul 48,91% dan sisi 48,62%.',80,603,1120,52,27,true,C.accent);break;}
   case 'demo':
    await picture(s,'implementasi-comparison-demo.png',76,165,1128,355);
    text(s,'small-demo: soreang ke baleendah, biaya 9,2 satuan bobot demo',80,541,1115,54,29,true,C.accent);
    text(s,'Demo Bandung memakai mode optimized. Hasil benchmark utama berasal dari arsip penelitian.',80,604,1100,50,25);break;
   case 'sources':
    lines(s,d.body,80,180,1100,88,30);
    text(s,'Data jalan © OpenStreetMap contributors\nhttps://www.openstreetmap.org/copyright',80,555,1110,75,24);break;
   default:lines(s,d.body,80,185,1100,d.body.length===3?125:104,d.body.length===3?34:30);
  }
 }
 s.speakerNotes.textFrame.setText(`${d.seconds?`Alokasi ${d.seconds} detik`:'Cadangan di luar 15 menit'}\n\n${d.script}\n\nPetunjuk: ${d.cue}\n\nSumber: ${d.source}`);
}
const draft=build+'/candidate.pptx';await(await PresentationFile.exportPptx(p)).save(draft);
console.log('Draft exported');
const final=work+'/output/Presentasi_Sidang_Zia_Ulhaq_Final.pptx';
await finalizePresentation({workspaceDir:work,candidatePath:draft,finalPath:final,pythonExecutable:'C:/Users/ervid/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...[5,6,7,12].flatMap(n=>['--require-native-table-slide',String(n)])],requiredNativeTableOwnerSlides:[5,6,7,12],requiredNativeChartOwnerSlides:[13],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:build+'/validation-final.json'});
console.log('Finalized '+final);
for(let i=0;i<p.slides.items.length;i++){
 const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});
 await fs.writeFile(build+`/slide-${i+1}.png`,new Uint8Array(await blob.arrayBuffer()));
 console.log('Rendered '+(i+1));
}



