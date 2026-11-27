#!/usr/bin/env python3
"""Builds the books site from books.json.

Edit books.json (prices, WhatsApp number, texts), then run:
    python3 build.py
It rewrites index.html and one page per book (<slug>.html) in this folder.
"""
import html
import json
import os
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "books.json"), encoding="utf-8"))
BOOKS = DATA["books"]
CUR = DATA.get("currency", "₪")
AUTHOR = DATA.get("author", "")
AUTHOR_FULL = DATA.get("author_full", AUTHOR)
ABOUT = DATA.get("about", [])
SITE = DATA.get("site_title", "")
WA = DATA.get("whatsapp", "").strip()

e = html.escape


def ver(path):
    """Short content hash, appended as ?v= so browsers fetch changed files right away."""
    import hashlib
    with open(os.path.join(HERE, path), "rb") as f:
        return f"{path}?v={hashlib.md5(f.read()).hexdigest()[:8]}"


WA_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 '
    "2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 "
    "9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm0 18.15h-.01a8.23 8.23 0 0 1-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 "
    "8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24a8.24 8.24 0 0 1 8.24 8.25c0 4.54-3.7 8.23-8.23 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.7-.8-.22-.09-.39-.13-.56.12-.16.25-.64.8-.79.97-.14.16-.29.18-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.44.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.44-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48a.92.92 0 0 0-.66.31c-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.29Z\"/></svg>"
)
DL_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 19h16"/></svg>'
)


def wa_link(text):
    return f"https://wa.me/{WA}?text={quote(text)}"


def head(title, desc, image=None):
    og = f'<meta property="og:image" content="{e(image)}">' if image else ""
    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
{og}
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📚</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Amatic+SC:wght@700&family=Assistant:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ver('assets/style.css')}">
</head>
<body>
"""


def topbar(current=None):
    links = "".join(
        f'<a href="{b["slug"]}.html"{" aria-current=page" if b["slug"] == current else ""}>{e(b["title"])}</a>'
        for b in BOOKS
    )
    return f"""<div class="wrap">
<header class="topbar">
  <a class="brand" href="./"><span class="hand">{e(SITE)}</span><small>הספרים של {e(AUTHOR_FULL)}</small></a>
  <nav class="topnav" aria-label="הספרים">{links}</nav>
</header>
</div>
<hr class="scribble">
"""


def footer():
    general = wa_link(f"היי {AUTHOR}, הגעתי מאתר הספרים ואשמח לשמוע עוד 🙂")
    return f"""<footer class="wrap">
  <span class="hand">{e(SITE)}</span>
  כל הספרים זמינים להורדה חינם כקובץ PDF. לעותק מודפס אפשר לכתוב לי <a href="{general}" target="_blank" rel="noopener">בוואטסאפ</a>.
</footer>
<a class="float-wa" href="{general}" target="_blank" rel="noopener" aria-label="שליחת הודעה בוואטסאפ">{WA_ICON}</a>
</body>
</html>
"""


def price_text(b):
    return " · ".join(f"{p['label']} {p['amount']} {CUR}" for p in b["prices"])


def card(b):
    lowest = min(p["amount"] for p in b["prices"])
    from_ = "החל מ־" if len(b["prices"]) > 1 else ""
    return f"""<a class="card" href="{b['slug']}.html" style="--c:{b['color']}">
  <div class="flip"><div class="flip-inner">
    <div class="face front"><img src="{ver('img/' + b['slug'] + '-front.jpg')}" alt="הכריכה של {e(b['title'])}" loading="lazy"></div>
    <div class="face back"><img src="{ver('img/' + b['slug'] + '-back.jpg')}" alt="" loading="lazy"></div>
  </div></div>
  <h3 class="hand">{e(b['title'])}</h3>
  <p>{e(b['tagline'])}</p>
  <span class="more">PDF חינם · מודפס {from_}{lowest} {CUR}</span>
</a>"""


def index():
    cards = "\n".join(card(b) for b in BOOKS)
    out = head(f"{SITE} | הספרים של {AUTHOR_FULL}", "חמישה ספרים קטנים מהלב. להורדה חינם או לעותק מודפס.", "img/lihyot-melech-front.jpg")
    out += topbar()
    out += f"""<main class="wrap">
<section class="hero">
  <h1 class="hand"><span>פירות</span> <span>העט</span></h1>
  <p>חמישה ספרים קטנים שכתבתי וציירתי בעצמי, על חיוך, על נחת, על שלום ועל מסע אחד גדול. אפשר להוריד כל אחד מהם חינם, או להזמין עותק מודפס.</p>
  <span class="pill">✏️ נכתב ואויר ביד על ידי {e(AUTHOR_FULL)}</span>
</section>
<section class="shelf" aria-label="הספרים">
{cards}
</section>
<section class="about" id="about">
  <img src="{ver('img/author.jpg')}" alt="{e(AUTHOR_FULL)}" loading="lazy">
  <div>
    <h2 class="hand">על הכותב</h2>
    <h3>{e(AUTHOR_FULL)}</h3>
    {"".join(f"<p>{e(p)}</p>" for p in ABOUT)}
    <a class="btn btn-whatsapp" href="{wa_link(f'היי {AUTHOR}, הגעתי מאתר הספרים 🙂')}" target="_blank" rel="noopener">{WA_ICON} לכתוב לירון</a>
  </div>
</section>
<section class="how">
  <h2 class="hand">איך זה עובד?</h2>
  <div class="step"><div class="ico">📖</div><b>בוחרים ספר</b><span>לחיצה על ספר פותחת את הכריכה הקדמית והאחורית שלו.</span></div>
  <div class="step"><div class="ico">⬇️</div><b>מורידים חינם</b><span>כל הספרים זמינים כקובץ PDF, בלי הרשמה ובלי תשלום.</span></div>
  <div class="step"><div class="ico">💬</div><b>רוצים עותק ביד?</b><span>שולחים לי הודעה בוואטסאפ ואני אדאג לעותק מודפס.</span></div>
</section>
</main>
"""
    out += footer()
    return out


def book_page(b):
    others = "\n".join(card(o) for o in BOOKS if o is not b)
    blurb = "".join(f"<p>{e(p)}</p>" for p in b["blurb"])
    if b.get("pdf"):
        dl = f"""<a class="btn btn-primary" href="{ver(b['pdf'])}" download>{DL_ICON} להורדת ה־PDF</a>"""
        dl_note = "הספר המלא, כולל הכריכות. חינם."
    else:
        dl = '<span class="btn btn-ghost">ה־PDF יעלה בקרוב</span>'
        dl_note = "בינתיים אפשר לבקש אותו בוואטסאפ."
    rows = ""
    for p in b["prices"]:
        msg = f"היי {AUTHOR}, אשמח להזמין עותק מודפס של \"{b['title']}\" ({p['label']}, {p['amount']} {CUR})."
        rows += f"""<div class="panel">
    <div><h2>{e(p['label'])}</h2><div class="price">{p['amount']} <small>{CUR}</small></div></div>
    <a class="btn btn-whatsapp" href="{wa_link(msg)}" target="_blank" rel="noopener">{WA_ICON} להזמנה בוואטסאפ</a>
  </div>
  """
    out = head(f"{b['title']} | {SITE}", b["tagline"] + " " + " ".join(b["blurb"])[:140], f"img/{b['slug']}-front.jpg")
    out += topbar(b["slug"])
    out += f"""<main class="wrap book" style="--c:{b['color']}">
<div class="crumbs"><a href="./">כל הספרים</a> / {e(b['title'])}</div>
<div class="book-grid">
  <div class="covers">
    <figure><button type="button" data-full="img/{b['slug']}-front.jpg" aria-label="הגדלת הכריכה הקדמית"><img src="{ver('img/' + b['slug'] + '-front.jpg')}" alt="הכריכה הקדמית של {e(b['title'])}"></button><figcaption>כריכה קדמית</figcaption></figure>
    <figure><button type="button" data-full="img/{b['slug']}-back.jpg" aria-label="הגדלת הכריכה האחורית"><img src="{ver('img/' + b['slug'] + '-back.jpg')}" alt="הכריכה האחורית של {e(b['title'])}"></button><figcaption>כריכה אחורית</figcaption></figure>
  </div>
  <div>
    <h1 class="hand">{e(b['title'])}</h1>
    <p class="tagline">{e(b['tagline'])}</p>
    <blockquote>{blurb}</blockquote>
    <div class="actions">
      <div class="panel">
        <div><h2>הורדה חינם</h2><p>{dl_note}</p></div>
        {dl}
      </div>
      {rows}
    </div>
  </div>
</div>
<section class="other">
  <h2 class="hand">ספרים נוספים</h2>
  <div class="shelf">
{others}
  </div>
</section>
</main>
<dialog class="lightbox" id="lightbox"><form method="dialog"><button aria-label="סגירה">×</button></form><img alt=""></dialog>
<script>
  const box = document.getElementById('lightbox');
  document.querySelectorAll('.covers button').forEach(btn => btn.addEventListener('click', () => {{
    box.querySelector('img').src = btn.dataset.full;
    box.querySelector('img').alt = btn.querySelector('img').alt;
    box.showModal();
  }}));
  box.addEventListener('click', ev => {{ if (ev.target === box) box.close(); }});
</script>
"""
    out += footer()
    return out


def write(name, text):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(text)


write("index.html", index())
for b in BOOKS:
    write(f"{b['slug']}.html", book_page(b))
print("built", 1 + len(BOOKS), "pages")
