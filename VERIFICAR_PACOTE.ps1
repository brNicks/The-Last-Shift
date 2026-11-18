# Verificador offline da V62 para Windows PowerShell 5.1+.
# Nao precisa do comando Python para preparar a publicacao no Git.
$ErrorActionPreference = 'Stop'
$manifestPath = Join-Path $PSScriptRoot 'MANIFEST_SHA256.txt'
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    Write-Host 'ERRO: MANIFEST_SHA256.txt nao encontrado.'
    exit 1
}
$errors = New-Object 'System.Collections.Generic.List[string]'
$count = 0
$pngCount = 0
try {
    $lines = Get-Content -LiteralPath $manifestPath -Encoding UTF8
    foreach ($line in $lines) {
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith('#')) { continue }
        if ($line -notmatch '^([0-9a-fA-F]{64}) {2}(.+)$') {
            $errors.Add('Linha de manifesto invalida: ' + $line)
            continue
        }
        $expectedHash = $Matches[1].ToLowerInvariant()
        $rel = $Matches[2]
        # Um manifesto malformado nao pode ler fora da pasta do pacote.
        if ([IO.Path]::IsPathRooted($rel) -or (($rel -split '[\\/]') -contains '..')) {
            $errors.Add('Caminho invalido: ' + $rel)
            continue
        }
        $filePath = Join-Path $PSScriptRoot ($rel.Replace('/', [IO.Path]::DirectorySeparatorChar))
        if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) {
            $errors.Add('Arquivo ausente: ' + $rel)
            continue
        }
        try {
            $actualHash = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($actualHash -ne $expectedHash) {
                $errors.Add('Hash divergente: ' + $rel)
                continue
            }
            if ($rel.EndsWith('.png', [StringComparison]::OrdinalIgnoreCase)) {
                # O SHA256 protege a imagem inteira; validar tambem sua assinatura PNG.
                $stream = [IO.File]::OpenRead($filePath)
                try {
                    $signature = New-Object byte[] 8
                    if ($stream.Read($signature, 0, 8) -ne 8 -or
                        ([BitConverter]::ToString($signature) -ne '89-50-4E-47-0D-0A-1A-0A')) {
                        $errors.Add('PNG sem assinatura valida: ' + $rel)
                        continue
                    }
                } finally { $stream.Dispose() }
                $pngCount++
            }
            $count++
        } catch {
            $errors.Add(('Erro no arquivo {0}: {1}' -f $rel, $_.Exception.Message))
        }
    }
} catch {
    Write-Host ('ERRO ao ler o manifesto: ' + $_.Exception.Message)
    exit 1
}
Write-Host ('Verificacao do pacote: {0} arquivos, {1} imagens PNG.' -f $count, $pngCount)
if ($errors.Count -gt 0) {
    Write-Host ('ERRO: {0} problema(s) encontrado(s).' -f $errors.Count)
    foreach ($e in $errors) { Write-Host (' - ' + $e) }
    exit 1
}
if ($count -lt 100) {
    Write-Host 'ERRO: manifesto incompleto.'
    exit 1
}
Write-Host 'OK: todos os hashes SHA256 conferem. Publicacao pode prosseguir.'
exit 0
