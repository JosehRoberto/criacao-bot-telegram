# Arquitetura do código (`bot/`)

Estrutura e padrões reaproveitados do projeto de referência `/home/roberto/projetos/agendatipara-bot`
(**somente leitura**). Copie a **organização**, não o domínio.

## 1. Árvore

```
bot/
├── __init__.py
├── config.py          ← lê .env; sem valores hardcoded
├── main.py            ← inicia a aplicação; error handler; logging
├── requirements.txt
├── .env.example
├── handlers/          ← commands.py (handlers), state_manager.py (ordem dos estados)
├── models/            ← entidades do domínio (+ validadores)
├── schemas/           ← validação/serialização (pydantic v2)
├── services/          ← integrações e regras: parser/editor, backup, histórico, git/API
└── tests/             ← pytest hermético (conftest.py + subpastas)
```

Na raiz do projeto: `pytest.ini`, `requirements-test.txt`, `backup/`, `docs/`.

## 2. Papel de cada camada

- **`config.py`**: única fonte de configuração. Lê `.env`; expõe constantes. Nunca hardcodar
  segredos nem caminhos que variam por ambiente (permitir override para testes).
- **`handlers/commands.py`**: registro de handlers, fluxo da conversa, preview e aprovação.
  Ponto único pós-confirmação.
- **`handlers/state_manager.py`**: define a **ordem dos estados**. Alterá-la exige atualizar também
  o dicionário de perguntas e o preview.
- **`models/`**: entidades do domínio e validadores (campos, formatos).
- **`schemas/`**: contratos de entrada/saída (pydantic v2), separação clara do modelo interno.
- **`services/`**: tudo que toca o mundo externo (arquivos, git, APIs) e as regras pesadas
  (parser/editor, backup, histórico). Idealmente cada serviço é testável sem rede.
- **`main.py`**: monta a `Application`, registra `post_init` uma única vez, inicia o polling.

## 3. Ordem de implementação sugerida

1. `config.py` + `.env.example` + `requirements.txt` + `pytest.ini`.
2. Serviços de dados (parser/editor do recurso alvo) **com testes**.
3. Serviço de backup (pré-condição de escrita).
4. Serviço de histórico (rastreabilidade).
5. `models`/`schemas`.
6. `state_manager` (ordem dos estados + dicionário de perguntas).
7. `handlers` (menu, fluxo, preview, aprovação).
8. Serviço de publicação (git/API) — só sob confirmação explícita.
9. Testes de fluxo + documentação.

## 4. Padrões de código

- `python-telegram-bot>=20`, `pydantic>=2`, `python-dotenv`, `requests`, `pytest`.
- Comentários e documentação em **pt-BR**; não adicionar comentários supérfluos.
- Serviços com dependências externas devem permitir injeção/override de caminhos e clientes para
  facilitar testes (ex.: constantes de caminho que o teste substitui via `monkeypatch`).
- Separar **lógica** (testável, pura quando possível) de **efeitos** (I/O, rede, git).

## 5. Configuração e testes

- `pytest.ini`:
  ```ini
  [pytest]
  testpaths = bot/tests
  python_files = test_*.py
  python_classes = Test*
  python_functions = test_*
  addopts = -v --strict-markers --strict-config
  markers =
      unit: Unit tests
      integration: Integration tests
      slow: Slow tests
      asyncio: Async tests
  ```
- `requirements-test.txt`: `pytest`, `pytest-asyncio`, `pytest-mock`, `pytest-cov`.

## 6. O que NÃO copiar do projeto de referência

- Regras de negócio, textos, integrações e modelos específicos daquele domínio.
- Caminhos e segredos reais (ex.: tokens, hosts, credenciais).
- Qualquer arquivo `.env` real.
