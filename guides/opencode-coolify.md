# Deploying OpenCode via `code.kaufmann.dev` with Coolify

---

## Overview

| Component | Role |
|---|---|
| OpenCode (Systemd) | Runs on the VPS, Port 4096 |
| `.env` file | Stores credentials as environment variables |
| Nginx (Docker / Coolify) | Reverse proxy for the domain |
| Coolify | Domain management + automatic SSL via Let's Encrypt |

---

## Step 1 — Create the Environment File

Store your credentials in a dedicated env file on the VPS. This keeps them out of the systemd unit file and makes them easy to update.

```bash
sudo nano /etc/opencode.env
```

```env
OPENCODE_SERVER_USERNAME=kaufmann
OPENCODE_SERVER_PASSWORD=your-secure-password
```

Lock down the permissions so only root can read it:

```bash
sudo chmod 600 /etc/opencode.env
```

---

## Step 2 — Create the Systemd Service

```bash
sudo nano /etc/systemd/system/opencode.service
```

```ini
[Unit]
Description=OpenCode Web Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/your-user
EnvironmentFile=/etc/opencode.env
ExecStart=/usr/local/bin/opencode web --hostname 0.0.0.0 --port 4096
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now opencode

# Verify it's running:
sudo systemctl status opencode
```

To update the password or username later, just edit `/etc/opencode.env` and restart:

```bash
sudo systemctl restart opencode
```

---

## Step 3 — Set the DNS Record

Add an A record with your DNS provider:

```
code.kaufmann.dev  →  <your VPS IP>
```

---

## Step 4 — Set Up the Coolify Reverse Proxy

In Coolify, go to **New Resource → Docker Based → Docker Compose Empty**.

You need two files:

### `docker-compose.yml`

```yaml
services:
  opencode-proxy:
    image: nginx:alpine
    restart: always
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
```

### `nginx.conf`

Create this as an additional file in the Coolify editor (there is a tab for extra files next to the Compose editor):

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://host.docker.internal:4096;
        proxy_http_version 1.1;

        # Required for WebSockets (OpenCode uses them)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Step 5 — Configure the Domain in Coolify

In the **Settings** of your new resource:

- **Domains:** `https://code.kaufmann.dev`
- SSL certificate is issued automatically via Let's Encrypt

Hit **Deploy**.

---

## Accessing OpenCode

Navigate to `https://code.kaufmann.dev` in any browser. You will be prompted for:

- **Username:** the value of `OPENCODE_SERVER_USERNAME` in `/etc/opencode.env`
- **Password:** the value of `OPENCODE_SERVER_PASSWORD` in `/etc/opencode.env`

---

## Updating Credentials

```bash
sudo nano /etc/opencode.env   # edit username / password
sudo systemctl restart opencode
```

No changes needed in Coolify — the proxy is credential-agnostic.
