# SMPS Tech Lab — Complete Update & Change Log

This document provides an itemized breakdown of all updates, enhancements, bug fixes, and file modifications made to the SMPS Tech Lab website codebase.

---

## 📋 Summary of All Modified, Added, and Deleted Files

| Category | File | Status | Description of Changes |
|---|---|---|---|
| **Documentation** | [`ADMIN_GUIDE.md`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/ADMIN_GUIDE.md) | **NEW** | User guide for content editors on how to manage members, events, gallery, and media library |
| **Documentation** | [`CONTENT_MANAGEMENT.md`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/CONTENT_MANAGEMENT.md) | **NEW** | Architecture guide covering DB schemas, `siteContent.js` fallback structure, and API endpoints |
| **Documentation** | [`DEPLOYMENT.md`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/DEPLOYMENT.md) | **NEW** | Production guide for Linux VPS, Gunicorn, Systemd, Nginx, Let's Encrypt SSL, and backup |
| **Documentation** | [`README.md`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/README.md) | **NEW** | Master project documentation, tech stack overview, quick start, and test suite commands |
| **Admin UI** | [`admin/admin.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/admin/admin.html) | **MODIFIED** | Added tabs and modals for Minds Behind Mission, Advisory Members, Collaborate & Stories, Gallery, and Media Library with photo uploaders |
| **Admin Logic** | [`admin/script.js`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/admin/script.js) | **MODIFIED** | Added full CRUD logic for members, photo uploads, image picker modal, story cards, and dynamic sync |
| **Admin Styles** | [`admin/style.css`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/admin/style.css) | **MODIFIED** | Added dark/light styling for member cards, image pickers, drag-and-drop dropzones, and story badges |
| **Backend & API** | [`app.py`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/app.py) | **MODIFIED** | Added REST endpoints for members, stories, gallery ordering (`ORDER BY created_at DESC, id DESC`), and media asset uploads |
| **Content Config** | [`assets/js/siteContent.js`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/assets/js/siteContent.js) | **NEW** | Centralized fallback data store for all site content ensuring zero-downtime offline resilience |
| **Public Page** | [`about.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/about.html) | **MODIFIED** | Redesigned Innovation Landscape with deep-tech visual nodes instead of star icons; dynamic CMS integration |
| **Public Page** | [`execom.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/execom.html) | **MODIFIED** | Added separate sections for Executive Committee, Minds Behind the Mission, and Strategic Advisors; rendered via CMS API / fallback |
| **Public Page** | [`collaborate.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/collaborate.html) | **MODIFIED** | Integrated dynamic Success Stories cards, metric badges, partnership models, and contact workflows |
| **Public Page** | [`gallery.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/gallery.html) | **MODIFIED** | Connected newest-first gallery loader, category filters (Summit, Workshop, Lab), and lightbox viewer |
| **Public Page** | [`events.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/events.html) | **MODIFIED** | Integrated dynamic events loader with categorized upcoming/past workshops and summits |
| **Public Page** | [`index.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/index.html) | **MODIFIED** | Updated hero banners, stats, innovation highlights, and navigation links |
| **Public Page** | [`products.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/products.html) | **MODIFIED** | Modernized product showcase, spec sheets, and enquiry action triggers |
| **Public Page** | [`ip-portfolio.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/ip-portfolio.html) | **MODIFIED** | Updated patent badges, research publications, and interactive filters |
| **Public Page** | [`careers.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/careers.html) | **MODIFIED** | Updated job positions, application modals, and company culture cards |
| **Public Page** | [`contact.html`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/contact.html) | **MODIFIED** | Verified form validation, Google Maps iframe embed, and direct enquiry channels |
| **Frontend Script** | [`assets/js/main.js`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/assets/js/main.js) | **MODIFIED** | Enhanced smooth scrolling, mobile navbar toggle, active navigation states, and Lucide icons init |
| **Database** | [`smps.db`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/smps.db) | **MODIFIED** | SQLite database populated with complete initial schema, members, stories, events, and gallery records |
| **Configuration** | [`.gitignore`](file:///Volumes/SHIV%20BHALKE/SMPSTHING/SMPS%20WEBSITE%20FOR%20BANGLORE/UPDATESMPSWEB/MAIN%20SMPS%20ROOT%20new/MAIN%20SMPS%20ROOT/.gitignore) | **MODIFIED** | Configured to ignore virtual environments (`venv/`), Python cache, macOS `.DS_Store` / `._*` files, and zip files |
| **Cleanup** | `add_icons.ps1`, `add_logo.py`, `fix_logo_visibility.py`, `fix_nav.py`, `fix_other_links.py`, `index.txt`, `make_redirecting.py`, `replace_port.py`, `update_logo.py`, `update_logo_png.py` | **DELETED** | Removed obsolete one-off migration and replacement utility scripts |

---

## 🔍 Specific Requirements Delivered

### 1. Advisory Members Management
- Added editable access in Admin Panel to add, edit, remove, and update details for Strategic Advisors.
- Integrated direct photo uploading (file picker) as well as existing Media Library photo selection.

### 2. "Minds Behind the Mission" & Team Members
- Added separate dedicated sections under `execom.html` for **Executive Committee**, **Minds Behind the Mission (Core Team)**, and **Strategic Advisors**.
- Provided full admin panel management to edit member bio, achievements, initials, photo, LinkedIn, and email.

### 3. About Section & Visual Refinements
- Replaced star icons in **About &rarr; Our Innovation Landscape** with modern tech-focused node visual elements.
- Enabled content editing through Admin Panel, backed up by centralized source code in `assets/js/siteContent.js`.

### 4. Collaborate & Success Stories
- Created dynamic management for Success Stories on `collaborate.html` (e.g., Bharat Industries, VTU Bridge, TechVista).
- Provided editable fields for case study headline, partner tags, result metric badges, descriptions, and imagery.

### 5. Events Section
- Full editorial access to add, update, and manage upcoming and past events, dates, locations, and descriptions.

### 6. Ordered Gallery (Latest First)
- Updated backend query and frontend rendering to ensure the newest uploaded images and gallery items appear at the very beginning (`ORDER BY created_at DESC, id DESC`).

### 7. Home Page Management
- All hero content, numbers, banners, and feature cards are configurable via the admin panel and fallback script.

### 8. Website Hosting & Repository Setup
- Configured Git author credentials for `smpstech9-cmyk <smpstechlab@gmail.com>`.
- Production deployment architecture documented in `DEPLOYMENT.md` for Nginx + Gunicorn + SSL.
- Created `ADMIN_GUIDE.md` for easy onboarding.

### 9. Complete Website Review
- Inspected and verified all landing pages, navigation bars, footer links, forms, responsiveness, and dark/light styling.
