# Histórico — V62 (Fase 1)

Esta consolidação utiliza a **V62 Parte 22.2**, última versão aprovada.

## Personagens e ambiente
- Protagonista com animações direcionais e movimentação revisada.
- Clara atrás do balcão da recepção, com animação durante diálogos.
- Chefe com cinco estágios visuais, patrulhas e comportamento de perseguição no Escritório B.
- Polimento visual da recepção e dos Escritórios A/B, incluindo luminárias, mesas, computadores e elementos corporativos.
- Documentos coletáveis representados por pastas; saídas com aparência de portas corporativas.

## Progressão
- Interações com crachá, documentos e avaliações preservadas.
- Saída do Escritório B bloqueada até o momento apropriado da fuga, com aviso `[E] Sair`.
- Encerramento com Clara bloqueia a movimentação e novas interações durante a cena.

## Abertura e interface
- Menu inicial com JOGAR, CONTROLES e SAIR.
- Ônibus chega, abre a porta e mostra o desembarque do protagonista.
- Caminhada até a sede da THE LAST SHIFT e portas de vidro abrindo antes da entrada.
- Movimento da câmera pela fachada, transição à recepção e surgimento do protagonista no hall inferior, olhando para Clara.
- Possibilidade de pular a abertura com Espaço/Esc sem deslocar o spawn.

## Consolidação da Fase 1
- Remoção dos manifests e registros intermediários da pasta de distribuição; nenhuma mecânica do jogo alterada.
- README, guia de GitHub, checklist de teste, manifesto SHA-256 e script de verificação adicionados.
- Atalhos opcionais de teste mantidos separadamente.

**Verificação automática** cobre sintaxe, integridade dos arquivos e PNGs. **Teste real no Windows/Pygame** segue sendo a etapa necessária para confirmar o funcionamento de ponta a ponta.

## Ajuste do publicador (sem alterações na jogabilidade)

- Corrigido o assistente de GitHub para verificar o pacote com PowerShell sem exigir `py` ou `python` no terminal.
- Preservadas as garantias de branch `feature/sprites-v62`, verificação do remoto, Git limpo, atualização fast-forward, confirmação e ausência de force push.
