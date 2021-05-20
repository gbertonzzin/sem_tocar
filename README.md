# SEM TOCAR

Sem Tocar é um aplicativo para automatização de entrada em edifícios comerciais que recebem clientes por agendamento, como consultórios, escritórios etc.
Desenvolvido para ser executado continuamente em um Raspberry Pi atrelado a uma webcam e porta magnética.

O funcionamento é o seguinte:
- Os eventos são adicionados ao Google Calendar (suporte para múltiplos calendários em uma única conta)
- Por meio do API do GCal o aplicativo checa periodicamente por novos eventos, mantendo logs dos requests
- Uma vez encontrado um novo evento (ou vários), é gerado um código QR criptografado para acesso
- Através do API do GMail, os convidados do evento são notificados e recebem o QR em anexo
- Na portaria do edifício, o convidado apresenta o QR à webcam
- Se o QR for válido e o horário do evento bater com o horário atual (TO DO:suporte para tolerância de horário), o Pi aciona um relé com optoacoplador que libera a entrada na porta magnética através de uma fonte 12v independente (TO DO: a parte do relé e da porta)

## Execucao

Para a execucao desse programa eh necessario o uso da ferramenta [Poetry](https://python-poetry.org/). 

Apos instalar a ferramenta, execute

```bash
poetry install
poetry run python sem_tocar.py
```

### Credenciais

Para que o programa tenha acesso aos seus calendarios e possa mandar emails pra alguem, defina as variaveis de ambiente
- `GCAL_TOKEN_FILE` para armazenamento de tokens para Calendar
- `MAIL_TOKEN_FILE` para armazenamento de tokens para GMail
- `GCAL_CREDENTIALS_FILE` para credenciais de Calendar
- `MAIL_CREDENTIALS_FILE` para credenciais do GMail
- `ENCRYPT_KEY_FILE` para armazenamento da chave criptografica

Para a obtencao das credenciais, falar com Guilherme. :P