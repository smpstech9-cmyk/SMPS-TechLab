# SMPS Tech Lab — Production Deployment Guide

This guide covers deploying the SMPS Tech Lab website on a Linux VPS (Ubuntu 22.04 / 24.04 LTS) with **Gunicorn**, **Systemd**, **Nginx**, and **Let's Encrypt SSL**.

---

## 1. System Requirements & Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python, pip, venv, and Nginx
sudo apt install -y python3 python3-pip python3-venv nginx git certbot python3-certbot-nginx
```

---

## 2. Setting Up the Application

```bash
# Clone or transfer repository to /var/www/smpstechlab
sudo mkdir -p /var/www/smpstechlab
sudo chown -R $USER:$USER /var/www/smpstechlab
cd /var/www/smpstechlab

# Create Python virtual environment and install dependencies
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install flask flask-cors pyjwt gunicorn
```

---

## 3. Configuring Systemd Service

Create `/etc/systemd/system/smps.service`:

```ini
[Unit]
Description=SMPS Tech Lab Flask & CMS Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/smpstechlab
Environment="PATH=/var/www/smpstechlab/venv/bin"
Environment="SECRET_KEY=your_strong_random_secret_key_here_minimum_32_bytes"
ExecStart=/var/www/smpstechlab/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5002 app:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo chown -R www-data:www-data /var/www/smpstechlab
sudo systemctl daemon-reload
sudo systemctl enable smps
sudo systemctl start smps
sudo systemctl status smps
```

---

## 4. Configuring Nginx Reverse Proxy

Create `/etc/nginx/sites-available/smpstechlab`:

```nginx
server {
    listen 80;
    server_name smpstechlab.com www.smpstechlab.com;

    client_max_body_size 25M;

    # Static uploads with browser caching
    location /assets/uploads/ {
        alias /var/www/smpstechlab/assets/uploads/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Static CSS and JS assets
    location /assets/ {
        alias /var/www/smpstechlab/assets/;
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }

    # Proxy all traffic to Gunicorn/Flask
    location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site configuration:
```bash
sudo ln -s /etc/nginx/sites-available/smpstechlab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 5. Enabling SSL with Let's Encrypt

```bash
sudo certbot --nginx -d smpstechlab.com -d www.smpstechlab.com
```

Certbot will automatically configure HTTPS redirection and renewals.

---

## 6. Automated Backup Strategy

To back up `smps.db` and `/assets/uploads/` daily, add a cron job (`crontab -e`):

```bash
0 3 * * * tar -czf /backups/smps_backup_$(date +\%F).tar.gz /var/www/smpstechlab/smps.db /var/www/smpstechlab/assets/uploads
```
