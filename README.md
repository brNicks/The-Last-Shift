# The Last Shift — V62 | Fase 1 consolidada

**Jogo 2D de suspense psicológico**, desenvolvido em Python e Pygame. O primeiro expediente começa com o protagonista chegando de ônibus à sede da corporação **THE LAST SHIFT**. Lá dentro, ele conversa com Clara, recebe o crachá, realiza tarefas nos Escritórios A e B e presencia as transformações de seu supervisor.

> **Estado:** versão consolidada da Fase 1, baseada na **V62 Parte 22.2**, testada e aprovada pelo desenvolvedor no Windows. O projeto **V61** e a branch **`main`** não foram alterados.

## Requisitos

- Windows 10/11, Python 3 instalado e comando `py` disponível;
- Pygame 2.5.0 ou mais recente (o atalho de execução tenta instalar a dependência, quando necessário).

## Executar

1. Extraia o ZIP **inteiro** em uma pasta (não execute diretamente dentro do ZIP).
2. Abra `EXECUTAR_NO_WINDOWS.bat`.
3. No menu, escolha **JOGAR** ou veja a tela **CONTROLES**.
4. A abertura mostra ônibus, desembarque, caminhada, portas automáticas, fachada e entrada pelo hall inferior da recepção.

**No terminal / VS Code:**

```bash
python -m pip install -r requirements.txt
python baldisoffice/main.py
```

Em Windows também é possível usar `py` no lugar de `python`.

## Controles

| Tecla | Ação |
| --- | --- |
| `W`, `A`, `S`, `D` | Movimentar |
| `Shift` | Correr (gasta estamina) |
| `E` | Conversar, coletar itens, interagir com portas e terminais |
| `1` a `4` | Selecionar resposta em avaliações |
| `Esc` | Fechar diálogos/interfaces ou pular a abertura |
| `Espaço` | Pular apenas a abertura; confirmar no menu |
| `↑/↓` ou `W/S` | Navegar no menu |
| `Enter` e mouse | Confirmar opções do menu |

O protagonista fica parado durante o encerramento com Clara. Pular a animação inicial preserva o mesmo ponto de entrada no hall inferior.

## Estrutura

- `baldisoffice/main.py` — inicialização do jogo.
- `baldisoffice/game.py` — cenas, mecânicas, avaliações, interfaces e progresso da fase.
- `baldisoffice/opening_cutscene.py` — abertura cinematográfica.
- `baldisoffice/assets/` — artes da recepção, Escritórios A/B, ônibus, fachada, personagens e itens.
- `TESTES_OPCIONAIS/` — atalhos de verificação de cenas específicas.
- `VERIFICAR_PROJETO.py` — verificação opcional em Python (sintaxe, integridade dos arquivos e PNG).
- `VERIFICAR_PACOTE.ps1` — verificação de integridade SHA256 e assinatura PNG com PowerShell, sem Python.
- `CHECKLIST_FASE1_FINAL.md` — checklist de teste no jogo real.
- `CHANGELOG_V62.md` — resumo das mudanças.
- `PUBLICAR_NA_FEATURE_V62.bat` — assistente **opcional** para publicar apenas na branch de desenvolvimento, depois de validar tudo.

## Antes do GitHub

1. Execute `powershell -NoProfile -ExecutionPolicy Bypass -File .\VERIFICAR_PACOTE.ps1` para conferir o pacote mesmo sem o comando `py` disponível.
2. O teste completo no Windows já foi aprovado pelo desenvolvedor; repita se alterar arquivos.
3. Publique na branch **`feature/sprites-v62`**, mantendo a **`main`** intocada; instruções em `GITHUB_PUBLICACAO.md`.
4. Faça o merge na `main` somente se e quando decidir, após conferir o diff.

**Nenhum conteúdo foi enviado ao GitHub por este pacote.** O teste gráfico no Windows foi confirmado pelo desenvolvedor; o empacotamento não executou o Pygame novamente.
