# Deploy via systemd

Como rodar o bot em produção sem contêiner, com venv dedicada e serviço systemd.

## 1. Pré-requisitos

- Pasta autoritativa do projeto (ex.: `/home/<user>/projetos/<projeto>`).
- Venv dedicada na raiz (ex.: `.venv/`).
- `bot/.env` preenchido (nunca versionado).

## 2. Preparação da venv

```bash
cd /home/<user>/projetos/<projeto>
python3 -m venv .venv
.venv/bin/pip install -r bot/requirements.txt
```

## 3. Unit systemd

Arquivo `bot/<nome>-bot.service`:

```ini
[Unit]
Description=<Nome> Bot Telegram
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/<user>/projetos/<projeto>
ExecStart=/home/<user>/projetos/<projeto>/.venv/bin/python -m bot.main
Restart=on-failure
RestartSec=5
EnvironmentFile=/home/<user>/projetos/<projeto>/bot/.env

[Install]
WantedBy=default.target
```

Instalação (usuário):
```bash
mkdir -p ~/.config/systemd/user
cp bot/<nome>-bot.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now <nome>-bot.service
```

## 4. Aplicar alterações (o commit NÃO faz deploy)

```bash
sudo systemctl restart <nome>-bot.service && sleep 3
sudo systemctl status <nome>-bot.service
sudo journalctl -u <nome>-bot.service -n 30 --no-pager
```

## 5. Regras

- **Instância única:** duas instâncias causam `409 Conflict` no `getUpdates` do Telegram.
- Manter o logger `httpx`/`httpcore` em `WARNING` para o token do bot não vazar nos logs.
- Ordem padrão: validar local → commit sob autorização → restart → validar → tag.

## 6. Rollback

```bash
# 1) Reverter arquivo pelo backup operacional
cp backup/<nome>_<TS>.bak <caminho-original>
sudo systemctl restart <nome>-bot.service

# 2) Ou reverter commit (preserva histórico)
git revert <commit>
sudo systemctl restart <nome>-bot.service
```

## 7. Alternativa com contêiner

Se usar Docker/Swarm, manter `replicas: 1`. O systemd continua sendo o caminho padrão simples para
este ambiente.
