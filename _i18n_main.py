# Builds /en/ and /kk/ versions of the main chat page from the Russian /index.html (AISun, 07.11.2026).
# Rule: every page in three languages (RU, KK, EN). Run: python3 _i18n_main.py  (edit the Russian page first)
import pathlib, re
R = pathlib.Path(__file__).resolve().parent
ru = (R / "index.html").read_text(encoding="utf-8")

CSS = "        .lang{display:flex;gap:6px;justify-content:center;margin-top:14px}.lang a{font-size:12px;letter-spacing:.08em;padding:4px 10px;border:1px solid rgba(201,162,39,.35);border-radius:999px;color:var(--text-muted);text-decoration:none}.lang a.on{color:#140f00;background:var(--gold);border-color:var(--gold)}\n"
HREF = ('    <link rel="alternate" hreflang="ru" href="https://galymzhan.com/">\n'
        '    <link rel="alternate" hreflang="en" href="https://galymzhan.com/en/">\n'
        '    <link rel="alternate" hreflang="kk" href="https://galymzhan.com/kk/">\n'
        '    <link rel="alternate" hreflang="x-default" href="https://galymzhan.com/">\n')
def switcher(cur):
    items = [("ru", "/", "РУС"), ("kk", "/kk/", "ҚАЗ"), ("en", "/en/", "ENG")]
    return '        <nav class="lang">' + "".join(f'<a href="{h}"{" class=\"on\"" if l == cur else ""} hreflang="{l}">{t}</a>' for l, h, t in items) + "</nav>\n"
def prep(h, cur):
    h = re.sub(r'    <link rel="alternate" hreflang[^>]*>\n', "", h)
    h = h.replace('    <link rel="preconnect" href="https://fonts.googleapis.com">', HREF + '    <link rel="preconnect" href="https://fonts.googleapis.com">', 1)
    if ".lang{display:flex" not in h: h = h.replace("    </style>", CSS + "    </style>", 1)
    h = re.sub(r'        <nav class="lang">.*?</nav>\n', "", h)
    h = h.replace("    </header>", switcher(cur) + "    </header>", 1)
    return h

T = [  # (ru, en, kk)
 ('<html lang="ru">', '<html lang="en">', '<html lang="kk">'),
 ("<title>Galymzhan — ИИ-наставник для предпринимателей</title>", "<title>Galymzhan — AI mentor for entrepreneurs</title>", "<title>Galymzhan — кәсіпкерлерге арналған ЖИ-тәлімгер</title>"),
 (">Ғалымжан — Душа знающего<", ">Ғалымжан — The Soul of the Knowing<", ">Ғалымжан — Білімдінің жаны<"),
 (">ИИ-наставник для тех, кто строит с нуля<", ">An AI mentor for those who build from scratch<", ">Нөлден бастап құрып жатқандарға арналған ЖИ-тәлімгер<"),
 ('<a href="/business/" style="color:var(--gold-light);text-decoration:none;border-bottom:1px solid rgba(201,162,39,.4)">Для бизнеса, школ и агентств →</a>',
  '<a href="/business/en/" style="color:var(--gold-light);text-decoration:none;border-bottom:1px solid rgba(201,162,39,.4)">For business, schools and agencies →</a>',
  '<a href="/business/kk/" style="color:var(--gold-light);text-decoration:none;border-bottom:1px solid rgba(201,162,39,.4)">Бизнеске, мектептерге және агенттіктерге →</a>'),
 ("Galymzhan онлайн <span>• бесплатная консультация</span>", "Galymzhan online <span>• free consultation</span>", "Galymzhan желіде <span>• тегін кеңес</span>"),
 ('title="Очистить историю">Новый чат<', 'title="Clear history">New chat<', 'title="Тарихты тазарту">Жаңа чат<'),
 ('placeholder="Напиши свой вопрос или идею..."', 'placeholder="Type your question or idea..."', 'placeholder="Сұрағыңызды немесе идеяңызды жазыңыз..."'),
 (">Отправить<", ">Send<", ">Жіберу<"),
 ('· <a href="/business/">Для бизнеса</a>', '· <a href="/business/en/">For business</a>', '· <a href="/business/kk/">Бизнеске</a>'),
 ("ЯЗЫК: Только русский и казахский. Никаких китайских иероглифов или других языков. Только кириллица и латиница.",
  "ЯЗЫК: Отвечай только на английском языке (English). Приветствие: \"Hey, brother!\". Никаких китайских иероглифов.",
  "ЯЗЫК: Отвечай только на казахском языке (қазақ тілінде). Приветствие: \"Сәлем, бауырым!\". Никаких китайских иероглифов. Только кириллица."),
 ("addMessage('Салем, брат! 👋\\n\\nМен Galymzhan — ИИ-наставник для предпринимателей.\\n\\nРасскажи свою идею или задай вопрос. Я помогу разобраться с бизнес-моделью, финансами, стратегией — с чем нужно.');",
  "addMessage('Hey, brother! 👋\\n\\nI am Galymzhan, an AI mentor for entrepreneurs.\\n\\nTell me your idea or ask a question. I will help you sort out the business model, finances, strategy — whatever you need.');",
  "addMessage('Сәлем, бауырым! 👋\\n\\nМен Galymzhan — кәсіпкерлерге арналған ЖИ-тәлімгермін.\\n\\nИдеяңызды айтыңыз немесе сұрақ қойыңыз. Бизнес-модель, қаржы, стратегия — керегінің бәрін бірге талдаймыз.');"),
 ("'Извини, брат. Что-то пошло не так. Попробуй ещё раз.'", "'Sorry, brother. Something went wrong. Please try again.'", "'Кешір, бауырым. Бірдеңе дұрыс болмады. Қайта көріңіз.'"),
 ("'galymzhan_history'", "'galymzhan_history_en'", "'galymzhan_history_kk'"),
]
for idx, lang in ((1, "en"), (2, "kk")):
    h = ru
    for row in T:
        assert row[0] in h, f"missing RU text: {row[0][:70]}"
        h = h.replace(row[0], row[idx])
    h = prep(h, lang)
    (R / lang).mkdir(exist_ok=True)
    (R / lang / "index.html").write_text(h, encoding="utf-8")
(R / "index.html").write_text(prep(ru, "ru"), encoding="utf-8")
print("ok: /, /en/, /kk/")
