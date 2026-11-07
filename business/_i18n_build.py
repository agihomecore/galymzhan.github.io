# Builds /business/en/ and /business/kk/ from the Russian page /business/index.html (AISun, 07.11.2026).
# Run: python3 business/_i18n_build.py   (edit Russian page first, then rebuild)
import pathlib, re
B = pathlib.Path(__file__).resolve().parent
ru = (B / "index.html").read_text(encoding="utf-8")

# --- language switcher + hreflang (inserted into the RU page too, idempotent) ---
CSS = ".lang{display:flex;gap:6px}.lang a{font-size:12px;letter-spacing:.08em;padding:4px 9px;border:1px solid var(--line);border-radius:999px;color:var(--muted);text-decoration:none}.lang a.on{color:#140f00;background:var(--gold);border-color:var(--gold)}"
HREF = ('<link rel="alternate" hreflang="ru" href="https://galymzhan.com/business/">\n'
        '<link rel="alternate" hreflang="en" href="https://galymzhan.com/business/en/">\n'
        '<link rel="alternate" hreflang="kk" href="https://galymzhan.com/business/kk/">\n'
        '<link rel="alternate" hreflang="x-default" href="https://galymzhan.com/business/en/">\n')
def switcher(cur):
    items = [("ru", "/business/", "РУС"), ("kk", "/business/kk/", "ҚАЗ"), ("en", "/business/en/", "ENG")]
    return '<span class="lang">' + "".join(f'<a href="{h}"{" class=\"on\"" if l == cur else ""} hreflang="{l}">{t}</a>' for l, h, t in items) + "</span>"
def prep(html, cur):
    html = re.sub(r'<link rel="alternate" hreflang[^>]*>\n', "", html)
    html = html.replace("</style>", "" if CSS in html else CSS + "\n</style>", 1) if CSS not in html else html
    html = html.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', HREF + '<link rel="preconnect" href="https://fonts.googleapis.com">', 1)
    html = re.sub(r'<span class="lang">.*?</span>', "", html)
    html = html.replace("</nav>", "</nav>" + switcher(cur), 1)
    return html

T = [  # (ru, en, kk)
 ('<html lang="ru">', '<html lang="en">', '<html lang="kk">'),
 ("Galymzhan для бизнеса — локальный ИИ от ИП SUN", "Galymzhan for business — local AI by IP SUN", "Galymzhan бизнеске — SUN ЖК-ның жергілікті ЖИ-і"),
 ("Локальный искусственный интеллект для бизнеса, школ и агентств Казахстана: SunSchool, SUNSTICK, Agazhan. Данные остаются у вас, модели работают на наших серверах в Астане или на вашем компьютере.",
  "Local artificial intelligence for businesses, schools and agencies in Kazakhstan: SunSchool, SUNSTICK, Agazhan. Your data stays with you; models run on our servers in Astana or on your own computer.",
  "Қазақстандағы бизнеске, мектептерге және агенттіктерге арналған жергілікті жасанды интеллект: SunSchool, SUNSTICK, Agazhan. Деректер сізде қалады, модельдер Астанадағы біздің серверлерде немесе өз компьютеріңізде жұмыс істейді."),
 ('>Решения<', '>Solutions<', '>Шешімдер<'),
 ('>Как работаем<', '>How we work<', '>Қалай жұмыс істейміз<'),
 ('>Связаться<', '>Contact<', '>Байланыс<'),
 ('>ИИ-наставник<', '>AI mentor<', '>ЖИ-тәлімгер<'),
 ("Для бизнеса · школ · агентств", "For business · schools · agencies", "Бизнеске · мектептерге · агенттіктерге"),
 ("Локальный искусственный интеллект, который остаётся у вас", "Local artificial intelligence that stays with you", "Сізде қалатын жергілікті жасанды интеллект"),
 ("ИП SUN из Астаны ставит ИИ-помощников, которые работают на наших серверах в Казахстане или прямо на вашем компьютере. Данные клиентов и учеников никуда не уходят.",
  "IP SUN from Astana sets up AI assistants that run on our servers in Kazakhstan or right on your computer. Customer and student data never leaves.",
  "Астанадағы SUN ЖК Қазақстандағы біздің серверлерде немесе тікелей сіздің компьютеріңізде жұмыс істейтін ЖИ-көмекшілерді орнатады. Клиенттер мен оқушылардың деректері ешқайда кетпейді."),
 ("<b>Казахстан</b> — серверы в Астане", "<b>Kazakhstan</b> — servers in Astana", "<b>Қазақстан</b> — серверлер Астанада"),
 ("<b>Без облака</b> — можно офлайн", "<b>No cloud</b> — works offline", "<b>Бұлтсыз</b> — интернетсіз де жұмыс істейді"),
 ("<b>Казахский и русский</b>", "<b>Kazakh and Russian</b>", "<b>Қазақ және орыс тілдері</b>"),
 (">Обсудить задачу<", ">Discuss your task<", ">Тапсырманы талқылау<"),
 (">Посмотреть решения<", ">See solutions<", ">Шешімдерді көру<"),
 ("Начинаем с малого: пилот на одном отделе, одной школе или одной флешке. Масштабируем, когда видно пользу.",
  "We start small: a pilot in one department, one school or on one USB stick. We scale once the value is clear.",
  "Кішіден бастаймыз: бір бөлімде, бір мектепте немесе бір флешкада пилот. Пайдасы көрінгенде кеңейтеміз."),
 ('<span class="tag gold">пилот</span>', '<span class="tag gold">pilot</span>', '<span class="tag gold">пилот</span>'),
 ("Школам и управлениям образования", "Schools and education departments", "Мектептер мен білім басқармаларына"),
 ("<li>Помощник для учителей и администрации</li><li>Работает в контуре школы, данные учеников остаются внутри</li><li>Казахский и русский язык</li><li>Ежедневные сводки и подсказки по задачам</li>",
  "<li>An assistant for teachers and administration</li><li>Runs inside the school's network; student data stays inside</li><li>Kazakh and Russian</li><li>Daily summaries and task hints</li>",
  "<li>Мұғалімдер мен әкімшілікке арналған көмекші</li><li>Мектеп ішінде жұмыс істейді, оқушылардың деректері ішінде қалады</li><li>Қазақ және орыс тілдері</li><li>Күнделікті шолулар мен тапсырмалар бойынша кеңестер</li>"),
 ("по запросу <small>пилот на договоре</small>", "on request <small>pilot under contract</small>", "сұраныс бойынша <small>шарт бойынша пилот</small>"),
 ("скоро в Kaspi", "coming to Kaspi", "жақында Kaspi-де"),
 ("Офисам и домашним пользователям", "Offices and home users", "Кеңселер мен үй пайдаланушыларына"),
 ("<li>ИИ-помощник Aisulu на флешке</li><li>Вставили в компьютер — работает без интернета</li><li>Свои документы, свой язык, ничего не уходит в сеть</li><li>Поддержка по подписке</li>",
  "<li>Aisulu AI assistant on a USB stick</li><li>Plug it in and it works without internet</li><li>Your documents, your language, nothing goes online</li><li>Support by subscription</li>",
  "<li>Флешкадағы Aisulu ЖИ-көмекшісі</li><li>Компьютерге қосасыз — интернетсіз жұмыс істейді</li><li>Өз құжаттарыңыз, өз тіліңіз, ештеңе желіге кетпейді</li><li>Жазылым бойынша қолдау</li>"),
 ("200 000 ₸ <small>рассрочка Kaspi · поддержка 1 000 ₸/мес</small>", "200 000 ₸ <small>Kaspi instalments · support 1 000 ₸/month</small>", "200 000 ₸ <small>Kaspi бөліп төлеу · қолдау 1 000 ₸/ай</small>"),
 ('<span class="tag ok">работает</span>', '<span class="tag ok">live</span>', '<span class="tag ok">жұмыс істейді</span>'),
 ("Агентствам недвижимости", "Real-estate agencies", "Жылжымайтын мүлік агенттіктеріне"),
 ("<li>Отвечает на заявки за секунды, днём и ночью</li><li>Собирает бюджет, район и телефон</li><li>Передаёт готовый лид агенту</li>",
  "<li>Answers enquiries in seconds, day and night</li><li>Collects budget, district and phone number</li><li>Hands a ready lead to an agent</li>",
  "<li>Өтінімдерге бірнеше секундта, күндіз-түні жауап береді</li><li>Бюджетті, ауданды және телефонды жинайды</li><li>Дайын лидті агентке береді</li>"),
 ("Демо для агентств →", "Demo for agencies →", "Агенттіктерге демо →"),
 ("<h2>Партнёрам</h2>", "<h2>Partners</h2>", "<h2>Серіктестерге</h2>"),
 ("Продавцы компьютеров и сборщики ПК: предустанавливаем Aisulu на ваши машины, вы продаёте компьютер, который умеет думать офлайн.",
  "Computer sellers and PC builders: we pre-install Aisulu on your machines, and you sell a computer that thinks offline.",
  "Компьютер сатушылары мен ДК жинаушылар: Aisulu-ды сіздің компьютерлеріңізге алдын ала орнатамыз, сіз интернетсіз ойлай алатын компьютер сатасыз."),
 ("Предустановка на ПК", "Pre-install on PCs", "ДК-ға алдын ала орнату"),
 ("<small>за компьютер</small>", "<small>per computer</small>", "<small>бір компьютер үшін</small>"),
 ("<li>Модель и программа на диске</li><li>Проверка работы до продажи</li>", "<li>Model and app on the drive</li><li>Checked before sale</li>", "<li>Модель мен бағдарлама дискіде</li><li>Сатудан бұрын тексеріледі</li>"),
 ("Разработчикам", "Developers", "Әзірлеушілерге"),
 ("<li>SunMCP — MCP-клиент для локальных моделей</li><li>Открытое ядро, MIT</li>", "<li>SunMCP — an MCP client for local models</li><li>Open core, MIT</li>", "<li>SunMCP — жергілікті модельдерге арналған MCP-клиент</li><li>Ашық ядро, MIT</li>"),
 ("Своя модель", "Your own model", "Өз модельіңіз"),
 ("<li>Обучение под ваши документы и тон</li><li>Размещение на вашем сервере или у нас</li></ul><div class=\"price\">по запросу</div>",
  "<li>Trained on your documents and tone</li><li>Hosted on your server or ours</li></ul><div class=\"price\">on request</div>",
  "<li>Сіздің құжаттарыңыз бен стиліңізге үйрету</li><li>Сіздің серверіңізде немесе бізде орналастыру</li></ul><div class=\"price\">сұраныс бойынша</div>"),
 ("Без лишних встреч и без обещаний, которые нельзя проверить.", "No extra meetings and no promises you can't check.", "Артық кездесусіз және тексеруге болмайтын уәдесіз."),
 ("<b>Разговор</b><p>30 минут: какая задача, какие данные, кто будет пользоваться.</p>", "<b>Call</b><p>30 minutes: the task, the data, who will use it.</p>", "<b>Әңгіме</b><p>30 минут: қандай тапсырма, қандай деректер, кім пайдаланады.</p>"),
 ("<b>Демо</b><p>Показываем на вашем примере, офлайн, прямо на ноутбуке.</p>", "<b>Demo</b><p>We show it on your example, offline, right on a laptop.</p>", "<b>Демо</b><p>Сіздің мысалыңызда, интернетсіз, тікелей ноутбукта көрсетеміз.</p>"),
 ("<b>Пилот</b><p>Договор, один отдел или одна школа, понятный срок и результат.</p>", "<b>Pilot</b><p>A contract, one department or one school, a clear timeline and result.</p>", "<b>Пилот</b><p>Шарт, бір бөлім немесе бір мектеп, нақты мерзім мен нәтиже.</p>"),
 ("<b>Запуск</b><p>Ставим, обучаем людей, сопровождаем по подписке.</p>", "<b>Launch</b><p>We install, train your people and support you by subscription.</p>", "<b>Іске қосу</b><p>Орнатамыз, адамдарды үйретеміз, жазылым бойынша сүйемелдейміз.</p>"),
 ("<h2>Почему локально</h2>", "<h2>Why local</h2>", "<h2>Неге жергілікті</h2>"),
 ("<b>Данные остаются в стране</b><p>Модели работают на наших серверах в Астане или у вас. Персональные данные не уходят в зарубежные облака.</p>",
  "<b>Data stays in the country</b><p>Models run on our servers in Astana or at your site. Personal data does not go to foreign clouds.</p>",
  "<b>Деректер елде қалады</b><p>Модельдер Астанадағы біздің серверлерде немесе сізде жұмыс істейді. Дербес деректер шетелдік бұлттарға кетпейді.</p>"),
 ("<b>Работает без интернета</b><p>SUNSTICK и локальная установка не зависят от связи и внешних сервисов.</p>",
  "<b>Works without internet</b><p>SUNSTICK and on-site installs do not depend on connectivity or outside services.</p>",
  "<b>Интернетсіз жұмыс істейді</b><p>SUNSTICK пен жергілікті орнату байланысқа және сыртқы қызметтерге тәуелді емес.</p>"),
 ("<b>Предсказуемая цена</b><p>Нет счёта за каждый запрос. Платите за установку и поддержку.</p>",
  "<b>Predictable price</b><p>No bill per request. You pay for installation and support.</p>",
  "<b>Болжамды баға</b><p>Әр сұрау үшін шот жоқ. Орнату мен қолдау үшін төлейсіз.</p>"),
 ("<b>Безопасность по умолчанию</b><p>ИИ не вводит пароли и не трогает банковские окна. Необратимые действия — только с подтверждения человека.</p>",
  "<b>Safe by default</b><p>The AI never types passwords or touches banking windows. Irreversible actions only with a person's confirmation.</p>",
  "<b>Әдепкі бойынша қауіпсіз</b><p>ЖИ құпиясөздерді енгізбейді және банк терезелеріне тимейді. Қайтарылмайтын әрекеттер — тек адамның растауымен.</p>"),
 ("<h2>Обсудим вашу задачу</h2>", "<h2>Let's discuss your task</h2>", "<h2>Тапсырмаңызды талқылайық</h2>"),
 ("Напишите, чем занимается ваша организация и что хотите поручить ИИ. Ответим в течение рабочего дня.",
  "Tell us what your organisation does and what you want the AI to take on. We reply within one working day.",
  "Ұйымыңыз немен айналысатынын және ЖИ-ге не тапсырғыңыз келетінін жазыңыз. Бір жұмыс күні ішінде жауап береміз."),
 ("Galymzhan · ИП SUN · Астана, Казахстан · 2026", "Galymzhan · IP SUN · Astana, Kazakhstan · 2026", "Galymzhan · SUN ЖК · Астана, Қазақстан · 2026"),
]
CYR = re.compile(r"[А-Яа-яЁё]")
for idx, lang in ((1, "en"), (2, "kk")):
    h = ru
    for row in T:
        assert row[0] in h, f"missing RU text: {row[0][:60]}"
        h = h.replace(row[0], row[idx])
    h = prep(h, lang)
    if lang == "en":
        left = [m for m in re.findall(r">[^<>]*<", h) if CYR.search(m) and "ҚАЗ" not in m and "РУС" not in m]
        assert not left, f"untranslated: {left[:5]}"
    (B / lang).mkdir(exist_ok=True)
    (B / lang / "index.html").write_text(h, encoding="utf-8")
(B / "index.html").write_text(prep(ru, "ru"), encoding="utf-8")
print("ok: ru, en, kk")
