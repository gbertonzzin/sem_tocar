# SEM TOCAR

Sem Tocar é um aplicativo para automatização de entrada em edifícios comerciais que recebem clientes por agendamento, como consultórios, escritórios etc.
Desenvolvido para ser executado continuamente em um Raspberry Pi atrelado a uma webcam e porta magnética.

O funcionamento é o seguinte:
- Os eventos são adicionados ao Google Calendar (suporte para múltiplos calendários em uma única conta)
- Por meio do API do GCal o aplicativo checa periodicamente por novos eventos, mantendo logs dos requests
- Uma vez encontrado um novo evento (ou vários), é gerado um código QR criptografado para acesso
- Através do API do GMail, os convidados do evento são notificados e recebem o QR em anexo
- Na portaria do edifício, o convidado apresenta o QR à webcam
- Se o QR for válido e o horário do evento bater com o horário atual (com suporte para tolerância de horário), o Pi aciona um relé com optoacoplador que libera a entrada na porta magnética através de uma fonte 12v independente (TO DO: testar o relé na porta)

## Execucao

Para a execucao desse programa é necessario o uso da ferramenta [Poetry](https://python-poetry.org/). 

Apos instalar a ferramenta, execute

```bash
poetry install
poetry run python sem_tocar.py
```

### Variáveis de ambiente

TODO: passar os parâmetros do config para variáveis de ambiente
