# GitHub — publicar a V62 sem alterar `main`

**Repositório:** https://github.com/brNicks/The-Last-Shift  
**Branch de destino:** `feature/sprites-v62`

> **Importante:** a branch já existe. Não faça `git push` para `main` nesta etapa. O pacote preserva a V61. Os arquivos não foram publicados automaticamente durante a consolidação.

## Opção simples: assistente incluído no pacote

1. **Teste a versão consolidada**. O publicador confere a integridade dos arquivos com **PowerShell**; não exige `py` nem `python` para publicar.
2. Tenha **Git para Windows** instalado e acesso autenticado ao GitHub. Windows 10/11 já inclui o PowerShell necessário.
3. Execute `PUBLICAR_NA_FEATURE_V62.bat` **após concluir os testes**.
4. O script faz um clone separado da branch `feature/sprites-v62` na pasta `_GITHUB_PREPARACAO_V62`, confirma o remoto e a branch, copia apenas arquivos da V62, mostra o resumo de alterações e **solicita sua confirmação antes de commit e push**.
5. Se o Git pedir autenticação, conclua pelo método de login configurado. Se pedir nome/e-mail para commit, configure-os no Git antes de repetir.
6. Depois, confira a branch: https://github.com/brNicks/The-Last-Shift/tree/feature/sprites-v62

Esse processo **não remove** arquivos antigos da branch, como backups da V61; não faz `force push`, merge nem troca de branch na sua cópia original. Se o clone falhar, nada será enviado.

## Publicação manual pelo VS Code

Se preferir, clone o repositório, faça checkout de `feature/sprites-v62`, copie para essa pasta o conteúdo consolidado (exceto o assistente de publicação e manifestos de conferência que não desejar versionar), revise `git status` e `git diff`, faça o commit e dê push apenas nessa branch.

**Se aparecer a mensagem “Python não foi encontrado”:** use o publicador corrigido deste pacote; o anterior dependia do comando `py`. Nenhuma alteração foi enviada enquanto essa mensagem interrompeu o script.

**Não faça merge na `main`** até conferir as alterações e decidir que é o momento certo.
