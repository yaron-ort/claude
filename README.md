# claude

Each project lives in its own folder. Live site: https://yaron-ort.github.io/claude/

| Folder | What it is | Live |
| --- | --- | --- |
| [`books/`](books/) | פירות העט: a Hebrew site for Yaron's five books (covers, free PDF, print prices, WhatsApp orders) | https://yaron-ort.github.io/claude/books/ |
| [`singing-games/`](singing-games/) | Pitch Glider, Pitch Pal and Walk and Sing: singing games and pitch training | https://yaron-ort.github.io/claude/singing-games/ |

## Updating the books site

Prices, the WhatsApp number and book texts are in `books/books.json`. After editing it run:

```
python3 books/build.py
```

That regenerates `books/index.html` and the page for each book.
