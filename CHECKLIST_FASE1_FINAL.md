# Checklist de validação final — The Last Shift V62

Preencha **durante uma partida real no Windows/Pygame**. Verificação estática de código não substitui testes jogáveis.

## Menu, abertura e recepção
- [ ] O menu mostra JOGAR, CONTROLES e SAIR e responde a teclado e mouse.
- [ ] A tela CONTROLES abre, retorna ao menu e o X fecha a janela.
- [ ] Ônibus aparece, para, abre as portas e protagonista desembarca sem atravessar a lateral.
- [ ] Ônibus parte; protagonista caminha; portas de vidro **abrem antes** de ele entrar.
- [ ] Câmera revela o prédio THE LAST SHIFT e transita para o interior.
- [ ] Protagonista começa no **hall inferior**, olhando para Clara.
- [ ] Ao reiniciar e pular a cena com Espaço/Esc, começa no mesmo lugar.
- [ ] Clara fala e anima a boca; coletar crachá atualiza o objetivo.
- [ ] Movimento, estamina, corrida e colisões funcionam; chefe patrulha sem prender o jogador.

## Escritório A
- [ ] Mesa, armário, iluminação, documentos e avaliação aparecem corretamente.
- [ ] Coletar os 3 documentos funciona; os itens desaparecem depois da coleta.
- [ ] Avaliação aceita respostas e avança o objetivo.
- [ ] Saída corporativa fica disponível apenas depois da conclusão da tarefa.

## Escritório B
- [ ] Iluminação e clima de tensão aumentam conforme o progresso.
- [ ] Documentos, avaliação e transformação do chefe progridem adequadamente.
- [ ] Não é possível fugir cedo; perseguição e aviso de saída funcionam no momento certo.
- [ ] Chefe Insano funciona e a fuga devolve o protagonista à recepção.

## Encerramento
- [ ] Segunda conversa com Clara inicia a cena final.
- [ ] WASD, Shift e E não movimentam o protagonista ou reabrem interações durante a cena.
- [ ] O quadro final aparece sem erro e a janela pode ser encerrada.

## Publicação
- [ ] `py VERIFICAR_PROJETO.py` termina sem falhas.
- [ ] Testei o arquivo `EXECUTAR_NO_WINDOWS.bat` em pasta recém-extraída.
- [ ] Conferi diff e branch `feature/sprites-v62` antes de qualquer push.
- [ ] **Não alterei `main` nem excluí backups da V61.**
