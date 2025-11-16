Minimal portfolio — ultra-low-resource
====================================

What this is
------------

A tiny, static portfolio designed to use the least possible server resources.
No JS frameworks, no external fonts, no images. Serve as static files.

Files added
-----------

- `index.html` — main page (old-school, Wikipedia-like)
- `styles.css` — tiny styling with no external dependencies
- `server.py` — tiny Python wrapper around `http.server` (conservative headers)
- `Dheeraj_REsume (1).pdf` — your resume (already in this folder)

How to run (quick)
------------------

Serve with Python's stdlib HTTP server (fast, tiny):

```bash
# run in the project root (/home/dheeraj/Desktop/minimal_portfolio)
python3 -m http.server 8000
```

Or use the provided wrapper which sets a small Cache-Control header:

```bash
python3 server.py 8000
```

Notes and minimal deployment tips
--------------------------------

- This site is static. For production, point any static file server (nginx, Caddy)
  to this folder and you'll be extremely low on memory and CPU.
- If you must run it on a tiny VM, use nginx to serve these files and let the OS
  handle caching; nginx uses little memory for purely static sites.

Small suggested systemd unit (optional):

```ini
[Unit]
Description=Minimal portfolio

[Service]
WorkingDirectory=/home/dheeraj/Desktop/minimal_portfolio
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Next steps (optional)
---------------------

- Replace sample project text with real project descriptions and links
- Add tiny screenshots (optimize and keep them small) only if necessary
- If you'd like, I can extract text from the PDF resume and pre-populate the
  About/Projects sections (requires reading the PDF). Tell me if you want that.
