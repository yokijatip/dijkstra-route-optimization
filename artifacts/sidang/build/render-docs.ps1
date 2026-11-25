$ErrorActionPreference='Stop'
$defenseDir='C:\Dev\Web\dijkstra-route-optimization\artifacts\sidang'
$defenseWord=New-Object -ComObject Word.Application
$defenseWord.Visible=$false
$defenseWord.DisplayAlerts=0
try {
 foreach ($defenseName in @('Naskah_Presentasi_Sidang_Zia_Ulhaq','Panduan_Dijkstra_dan_Aplikasi_Zia_Ulhaq')) {
  $defenseDoc=$defenseWord.Documents.Open("$defenseDir\output\$defenseName.docx")
  $defenseDoc.Repaginate()
  $null=$defenseDoc.Fields.Update()
  $defenseDoc.Save()
  $defenseDoc.ExportAsFixedFormat("$defenseDir\build\$defenseName.pdf",17)
  Write-Output "$defenseName pages: $($defenseDoc.ComputeStatistics(2))"
  $defenseDoc.Close(0)
 }
} finally {$defenseWord.Quit()}
