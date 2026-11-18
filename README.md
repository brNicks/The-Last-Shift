# The Last Shift — V62 | Fase 1

Jogo 2D de suspense psicológico desenvolvido em **Python + Pygame**.

Você chega à corporação **THE LAST SHIFT**, conhece Clara, cumpre tarefas nos escritórios e descobre que seu expediente não será normal.

## Requisitos
- Python 3.10 ou mais recente
- Pygame 2.5 ou mais recente (instalado pelo `requirements.txt`)

## Como executar
Abra um terminal **na pasta principal do repositório** e execute:

```bash
python -m pip install -r requirements.txt
python baldisoffice/main.py
```

No Windows, use `py` no lugar de `python` caso seja o comando disponível. **Não é necessário nenhum arquivo .bat.**

## Controles
| Tecla | Ação |
|---|---|
| W, A, S, D | Movimentar |
| Shift | Correr |
| E | Interagir, falar, coletar documentos |
| 1–4 | Selecionar respostas |
| Enter / mouse | Confirmar no menu |
| Esc | Fechar interfaces / pular a abertura |
| Espaço | Pular a abertura |

## Estrutura
- `baldisoffice/main.py`: inicialização.
- `baldisoffice/game.py`: lógica da Fase 1.
- `baldisoffice/opening_cutscene.py`: abertura cinematográfica.
- `baldisoffice/assets/`: imagens, animações, cenários e itens.
- `requirements.txt`: dependências.

**Versão:** V62, Fase 1 aprovada. Esta branch é `feature/sprites-v62`; a `main` permanece separada.

As ferramentas internas de teste, os backups, os scripts de publicação e os recursos antigos não utilizados foram retirados desta branch para manter somente o necessário para jogar.
