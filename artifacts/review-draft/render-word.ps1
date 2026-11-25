$ErrorActionPreference = 'Stop'
$reviewPath = 'C:\Dev\Web\dijkstra-route-optimization\artifacts\review-draft\Skripsi_Zia_Ulhaq_Revisi.docx'
$reviewPdf = 'C:\Dev\Web\dijkstra-route-optimization\artifacts\review-draft\Skripsi_Zia_Ulhaq_Revisi.pdf'
$wordReview = New-Object -ComObject Word.Application
$wordReview.Visible = $false
$wordReview.DisplayAlerts = 0
$wordReview.AutomationSecurity = 3
try {
  $reviewDoc = $wordReview.Documents.Open($reviewPath, $false, $false)
  $reviewDoc.Repaginate()
  $null = $reviewDoc.Fields.Update()
  foreach ($reviewToc in $reviewDoc.TablesOfContents) { $reviewToc.Update() }
  foreach ($reviewTof in $reviewDoc.TablesOfFigures) { $reviewTof.Update() }
  $reviewDoc.Repaginate()
  foreach ($reviewToc in $reviewDoc.TablesOfContents) { $reviewToc.UpdatePageNumbers() }
  foreach ($reviewTof in $reviewDoc.TablesOfFigures) { $reviewTof.UpdatePageNumbers() }
  $reviewDoc.Save()
  $reviewDoc.ExportAsFixedFormat($reviewPdf, 17)
  Write-Output ('Pages: ' + $reviewDoc.ComputeStatistics(2))
  $reviewDoc.Close(0)
} finally { $wordReview.Quit() }
