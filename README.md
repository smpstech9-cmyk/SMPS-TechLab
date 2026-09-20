# SMPS Tech Lab — Master Web Application & CMS Architecture

Welcome to the official repository for **SMPS Tech Lab** (`smpstechlab.com`), India's premier deep-tech innovation, power electronics engineering, and talent incubation ecosystem.

---

## 🚀 Key Highlights & Capabilities

- **Deep-Tech Visual Aesthetics**: Modern dark/light theme, interactive particle grids, glassmorphism, responsive bento boxes, and dynamic tech nodes.
- **Enterprise-Grade CMS**: Manage all site content dynamically via the `/admin` portal or automated REST APIs.
- **Centralized Source Fallback**: Centralized configuration (`assets/js/siteContent.js`) ensures zero downtime and instant resilience against network partitions or database outages.
- **Local Media Library**: Native `/assets/uploads/` asset management with drag-and-drop uploads, instant photo replacement, copy-link badges, and preview modals.
- **Ordered Gallery Engine**: High-performance gallery automatically ordered newest-first (`ORDER BY created_at DESC, id DESC`).
- **Dynamic Innovation Landscape**: Redesigned node system showcasing Core R&D, Strategic Alliances, Quantum AI, Power Electronics, 5G/6G, and ESDM Skilling.
- **Complete Success Stories System**: Manageable partnership tracks (Bharat Industries, VTU Bridge, TechVista) with metrics and instant visual indicators.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Vanilla HTML5, CSS3, Modern ES6+ JavaScript, Lucide Icons |
| **Backend API** | Python 3, Flask, SQLite3, PyJWT |
| **Database** | SQLite (`smps.db`) with automatic schema migration |
| **Media Storage** | Local filesystem (`/assets/uploads/`) with static serving |
| **Admin Panel** | Vanilla JS Single Page Application (`/admin/admin.html`) |

---

## 🏁 Quick Start & Local Development

### 1. Prerequisites
- Python 3.10+ (virtual environment located in `./venv`)

### 2. Running the Backend Server
```bash
# From project root:
./venv/bin/python app.py
```
The server starts on `http://127.0.0.1:5002`.

### 3. Accessing the Applications
- **Public Portal**: Open `http://127.0.0.1:5002/index.html` or any static HTML page (`about.html`, `products.html`, `execom.html`, `events.html`, `gallery.html`, `collaborate.html`).
- **Admin CMS Dashboard**: Open `http://127.0.0.1:5002/admin/admin.html`.
  - Default Username: `admin`
  - Default Password: `smps2026`

---

## 🧪 Automated Testing
Run the CMS test suite to verify all APIs and authentication:
```bash
./venv/bin/python /Users/shivabhakle/.gemini/antigravity-ide/brain/b23162c8-5843-41d6-adaa-18d9522ef5fd/scratch/test_cms_suite.py
```

---

## 📚 Documentation Index

- [Admin User Guide](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/ADMIN_GUIDE.md) — How to manage members, events, gallery, and media.
- [Content Management Guide](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/CONTENT_MANAGEMENT.md) — Data schema, siteContent.js fallback, and API contracts.
- [Production Deployment Guide](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/DEPLOYMENT.md) — Gunicorn, Nginx, Systemd, SSL, and backup guides.
