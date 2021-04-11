# SEM TOCAR

Faz algo que eu nao tenho ideia do que seja ainda, mas um dia eu descubro! ;)

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