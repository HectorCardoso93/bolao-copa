# Bolão Copa do Mundo 2026 — Python

## Requisitos
- Python 3.8 ou superior (https://python.org/downloads)
  - Durante a instalação, marque "Add Python to PATH"

## Instalação (apenas uma vez)

Abra o Prompt de Comando na pasta onde descompactou o arquivo e execute:

```
pip install flask
```

## Iniciar o servidor

```
python app.py
```

O servidor vai exibir:

```
  Bolao Copa do Mundo 2026
  Acesse: http://localhost:5000
  Na rede local: http://<seu-ip>:5000
```

## Acesso pela rede da empresa

Para que outras pessoas acessem pelo link, descubra o IP do computador servidor:
- Abra o Prompt de Comando e digite: `ipconfig`
- Procure "Endereço IPv4" (ex: 192.168.1.10)
- Compartilhe o link: `http://192.168.1.10:5000`

## Funcionamento

| Página | Endereço |
|---|---|
| Página inicial | http://localhost:5000 |
| Cadastro | http://localhost:5000/cadastro |
| Palpites | http://localhost:5000/palpites |
| Classificação | http://localhost:5000/classificacao |
| Admin | http://localhost:5000/admin |

## Painel Admin

- Acesse `/admin` com a senha: **copa2026**
- **Aba Resultados**: insira o placar real e marque "Encerrado" — a pontuação é recalculada automaticamente
- **Aba Jogadores**: visualize e remova participantes

## Pontuação

- **5 pontos**: placar exato (ex: palpitou 2x1, resultado foi 2x1)
- **2 pontos**: resultado certo (ex: palpitou 2x1, resultado foi 3x1 — ambos vitória do time da casa)
- **0 pontos**: errou

## Banco de dados

Os dados ficam salvos no arquivo `bolao.db` na mesma pasta do `app.py`.
Faça backup desse arquivo para preservar os palpites!
