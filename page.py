"""Wraps a folium-saved map in a centered page: title, framed map, footer.

Not a standalone script — imported by plot.py, so it carries no
`# /// script` block of its own.
"""

from pathlib import Path

STYLE = """
<style>
  html, body {
    margin: 0;
    padding: 0;
    background: #f6f4ef;
    color: #2d3a35;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica,
      Arial, sans-serif;
  }

  .page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-sizing: border-box;
    padding: 56px 24px 32px;
  }

  .page-header {
    max-width: 640px;
    text-align: center;
    margin-bottom: 28px;
  }

  .page-header h1 {
    font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    font-weight: 400;
    font-size: 2.2rem;
    line-height: 1.25;
    margin: 0 0 12px;
  }

  .page-header p {
    margin: 0;
    font-size: 0.98rem;
    line-height: 1.55;
    color: #5c6a62;
  }

  .map-frame {
    position: relative;
    width: 100%;
    max-width: 900px;
    height: 560px;
    border: 1px solid #d8dcd4;
    border-radius: 6px;
    overflow: hidden;
  }

  /* Folium draws the map as a full-viewport, absolutely-positioned div.
     Pin it to fill this fixed frame instead of the whole page. */
  .folium-map {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100% !important;
    height: 100% !important;
  }

  .page-footer {
    max-width: 640px;
    margin-top: 22px;
    text-align: center;
    font-size: 0.85rem;
    color: #8b9590;
  }

  .page-footer a {
    color: #64766a;
  }

  @media (max-width: 600px) {
    .page { padding: 36px 16px 24px; }
    .page-header h1 { font-size: 1.7rem; }
    .map-frame { height: 420px; }
  }
</style>
"""


def wrap_page(out_path: Path, map_id: str, title: str, subtitle: str, source_html: str) -> None:
    """Add a title, a constrained map frame, and a footer around the map
    that folium already saved to out_path, editing the file in place."""

    html = out_path.read_text(encoding="utf-8")

    header = f"""
<div class="page">
  <header class="page-header">
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </header>
  <div class="map-frame">
"""
    footer = f"""
  </div>
  <footer class="page-footer">
    <p>{source_html}</p>
  </footer>
</div>
"""

    html = html.replace("</head>", STYLE + "</head>")
    html = html.replace(f'<div class="folium-map" id="{map_id}"', header + f'<div class="folium-map" id="{map_id}"')
    html = html.replace("</body>", footer + "</body>")

    out_path.write_text(html, encoding="utf-8")