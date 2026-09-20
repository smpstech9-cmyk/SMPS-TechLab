# SMPS Tech Lab — Content Management & Fallback Architecture

## Overview

The SMPS Tech Lab content ecosystem uses a dual-layer architecture:
1. **Dynamic Database Layer (SQLite via Flask REST APIs)**: Real-time source of truth for editors.
2. **Centralized Codebase Fallback (`assets/js/siteContent.js`)**: Static, version-controlled baseline that guarantees uninterrupted rendering even if the backend is offline or during cold starts.

---

## 1. Centralized Fallback: `assets/js/siteContent.js`

All public pages (`index.html`, `about.html`, `execom.html`, `events.html`, `gallery.html`, `collaborate.html`, `products.html`, `careers.html`) load `assets/js/siteContent.js`.

The `window.SiteContent` object structure:
- `SiteContent.meta`: Site name, tagline, email, phone, location.
- `SiteContent.home`: Hero titles, statistics, badges, CTAs, ticker items.
- `SiteContent.about`: Vision, mission, stats, achievements, innovation landscape categories.
- `SiteContent.execom`:
  - `members`: Minds behind the mission / core team list.
  - `advisors`: Strategic advisory board.
- `SiteContent.collaborate`: Track perspectives (Academia, Industry, Startup, Government), process steps, and `successStories`.
- `SiteContent.events`: Flagship and standard event listings.
- `SiteContent.gallery`: Photo gallery moments with categories and tags.

---

## 2. REST API Endpoints Reference

All endpoints return JSON and accept JSON bodies (unless multipart for upload).

### Public Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Health and server status |
| `/api/execom` | GET | List Execom members (support `?type=advisor`, `?type=execom`, `?type=team`) |
| `/api/events` | GET | List events |
| `/api/gallery` | GET | List gallery items (ordered newest-first) |
| `/api/stories` | GET | List success stories |
| `/api/products` | GET | List products |
| `/api/patents` | GET | List IP assets |
| `/api/media` | GET | List all uploaded media in `/assets/uploads/` |
| `/api/settings/<key>` | GET | Get settings JSON by key (e.g. `homeData`, `aboutData`, `collabData`) |

### Protected Endpoints (Requires `Authorization: Bearer <token>`)
| Endpoint | Method | Description |
|---|---|---|
| `/api/auth/login` | POST | Authenticate admin, returns JWT token |
| `/api/upload` | POST | Upload file to `/assets/uploads/` (multipart/form-data) |
| `/api/execom` | POST / PUT / DELETE | CRUD operations for Execom and Advisors |
| `/api/events` | POST / PUT / DELETE | CRUD operations for Events |
| `/api/gallery` | POST / PUT / DELETE | CRUD operations for Gallery items |
| `/api/stories` | POST / PUT / DELETE | CRUD operations for Success Stories |
| `/api/products` | POST / PUT / DELETE | CRUD operations for Products |
| `/api/media/<filename>` | DELETE | Delete media file from server |
| `/api/settings/<key>` | POST | Save settings JSON |
