# Fetch every corpus article into the cache (idempotent; skips cached ones).
$root = Split-Path $PSScriptRoot -Parent
$py = Join-Path $root "venv\Scripts\python.exe"
$corpus = Get-Content (Join-Path $root "data\corpus.json") -Raw | ConvertFrom-Json
foreach ($a in $corpus.articles) {
    & $py (Join-Path $root "pipeline\scrape_sep.py") --article $a.id
    if ($LASTEXITCODE -ne 0) { Write-Error "failed on $($a.id)"; exit 1 }
}
Write-Output "corpus scrape complete"
