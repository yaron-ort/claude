# פירות העט

Static Hebrew (RTL) site for five books: להיות מלך, חיוך ללא סיבה, בנחת, המשחק הגדול, ספר השלום.

- `books.json`: titles, texts, prices, WhatsApp number
- `build.py`: generates `index.html` and `<slug>.html` from `books.json`
- `img/`: front and back covers
- `pdf/`: full books (cover + content + back cover) for free download
- `assets/style.css`: design

To add the בנחת PDF later: put it at `pdf/benachat.pdf`, set `"pdf": "pdf/benachat.pdf"` for that book in `books.json`, and run `python3 build.py`.
