$mensagemCommit = "Atualização de código"

Write-Host "Rodando os testes..."
py -m pytest
$codigoSaida = $LASTEXITCODE

if ($codigoSaida -eq 0) {
    Write-Host "Todos os testes passaram!"
    
    $mensagemCommit = Read-Host "Digite a mensagem do commit"

    git add .
    git commit -m $mensagemCommit
    git push origin main

    Write-Host "Commit e push realizados com sucesso!"
} else {
    Write-Host "Alguns testes falharam. Commit e push não realizados."
}
