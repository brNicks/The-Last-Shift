# The Last Shift — V62.1 | Fase 1

Jogo 2D de suspense psicologico em **Python + Pygame**.

## Como executar

1. Instale o Python 3.10+ e abra esta pasta no VS Code ou em um terminal.
2. Instale a dependencia: `python -m pip install -r requirements.txt`.
3. Inicie com: `python baldisoffice/main.py`.

No Windows, voce pode usar `py` no lugar de `python` se esse comando estiver disponivel. Tambem e possivel executar `baldisoffice/main.py` pelo botao **Run Python File** do VS Code, escolhendo o interpretador com Pygame instalado. Nao e necessario nenhum arquivo `.bat`.

## Controles

| Tecla | Acao |
|---|---|
| W / A / S / D | Andar |
| Shift | Correr |
| E | Conversar e interagir |
| 1 a 4 | Escolher respostas |
| Enter / mouse | Confirmar no menu |
| Esc / Espaco | Pular a abertura |

## V62.1 — Correcao de progresso

- Escritório A e B ficam fechados apos a conclusao; os avisos `[E] Entrar` desaparecem das portas concluidas.
- As portas mostram `A CONCLUIDO` / `B CONCLUIDO` na recepcao.
- Nao e mais possivel reiniciar documentos, avaliacoes, fases do chefe ou missoes entrando de novo nos setores concluidos.
- Clara tem falas diferentes antes de pegar o cracha, depois dele e apos terminar o Escritorio A.
- O dialogo de encerramento com Clara foi preservado.

A abertura, cenarios, documentos, avaliacoes, perseguição e encerramento da Fase 1 permanecem iguais a V62 aprovada. Esta versao V62.1 foi testada e aprovada no Windows antes da publicacao.

## Estrutura

- `baldisoffice/main.py` — inicia o jogo.
- `baldisoffice/game.py` — mecanicas e cenas.
- `baldisoffice/assets/` — sprites e cenarios.
- `requirements.txt` — dependencias.
