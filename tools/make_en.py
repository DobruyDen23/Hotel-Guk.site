"""
ГЕНЕРАТОР АНГЛІЙСЬКОЇ ВЕРСІЇ
---------------------------------------------------------
Бере index.html (українська) і створює en/index.html.
Коментарі в HTML лишаються українською.

Як користуватися (з папки сайту):
    python3 tools/make_en.py

Якщо ви змінили текст в українській версії — додайте пару
"український текст": "English text" у словник T нижче
і запустіть скрипт знову. Скрипт покаже:
  NOT FOUND  — фразу зі словника не знайдено на сторінці;
  Cyrillic left — що лишилось неперекладеним.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
DST = ROOT / "en" / "index.html"

T = {
    # head
    "Готель «Гук» — номери та котеджі за 1 км від Буковелю": "Hotel GUK — rooms and cottages 1 km from Bukovel",
    "Готель і котеджі в Поляниці, за кілометр від підйомників Буковеля. Ресторан карпатської кухні, басейн, сауна, джакузі, мангальна зона.":
        "A hotel and cottages in Polianytsia, a kilometre from the Bukovel ski lifts. Carpathian restaurant, pool, sauna, jacuzzi and barbecue area.",
    # header / menu
    "Готель GUK — на початок сторінки": "Hotel GUK — back to top",
    "Головне меню": "Main menu",
    "Мова сайту": "Site language",
    "Увімкнути темну тему": "Switch to dark theme",
    "Увімкнути світлу тему": "Switch to light theme",
    "Забронювати номер": "Book a room",
    "Забронювати пакет": "Book this package",
    "Забронювати": "Book now",
    "Закрити ✕": "Close ✕",
    ">Меню<": ">Menu<",
    # hero
    "Туман над лісистими схилами Карпат": "Mist over the forested Carpathian slopes",
    "Готель і котеджі · Поляниця, Буковель": "Hotel & cottages · Polianytsia, Bukovel",
    "1 км до підйомника": "1 km to the ski lift",
    "Тиша, <em>що чекає</em> за&nbsp;кілометр від&nbsp;Буковелю": "Mountain quiet, <em>one kilometre</em> from&nbsp;Bukovel",
    "<span>Заїзд</span>": "<span>Check-in</span>",
    "<span>Виїзд</span>": "<span>Check-out</span>",
    "<span>Гості</span>": "<span>Guests</span>",
    "1 гість": "1 guest",
    "2 гостей</option>": "2 guests</option>",
    "3 гостей": "3 guests",
    "4 гостей</option>": "4 guests</option>",
    "5+ гостей": "5+ guests",
    "Перевірити дати": "Check dates",
    "<dd>1 км</dd>": "<dd>1 km</dd>",
    "≈ 1 км": "≈ 1 km",
    # ticker
    "Пропозиції готелю": "Hotel offers",
    "Оплата частинами — половина при заселенні": "Pay in two parts — half on arrival",
    "Знижка 10% для військових": "10% off for military personnel",
    "Діти до 7 років — безкоштовно в пакетах": "Children under 7 stay free on packages",
    "Групам від 20 осіб — окремі умови": "Special terms for groups of 20+",
    "Можна з тваринами за домовленістю": "Pets welcome by arrangement",
    # about
    "01 · Дім": "01 · The house",
    "Дерев'яний дім, де ранок починається <em>з туману</em> за вікном.": "A wooden house where mornings <em>begin with mist</em> at the window.",
    "Триповерховий готель і окремі котеджі в урочищі Стаїще. Номери з балконами, камінна зала, ресторан на першому поверсі й екологічні матеріали в інтер'єрах.":
        "A three-storey hotel and separate cottages in the Staishche tract. Rooms with balconies, a fireplace hall, a ground-floor restaurant and natural materials throughout.",
    "Обрати номер": "Choose a room",
    "Кімната з панорамними вікнами в тумані": "A room with floor-to-ceiling windows in the mist",
    "Ранок у горах · вид з номера": "Morning in the mountains · the view from a room",
    "<dt>до підйомника</dt>": "<dt>to the ski lift</dt>",
    "Пішки або кілька хвилин авто — і ви на схилах Буковеля.": "A short walk or a few minutes by car, and you're on the Bukovel slopes.",
    "типів номерів і котеджів": "types of rooms and cottages",
    "Від затишного двомісного до котеджу на 180 м² для компанії.": "From a cosy double to a 180 m² cottage for a group.",
    "<dt>рецепція</dt>": "<dt>front desk</dt>",
    "Заселимо пізно ввечері й допоможемо з будь-яким питанням.": "We'll check you in late at night and help with anything you need.",
    # rooms
    "02 · Номери": "02 · Rooms",
    "Номери, люкси <em>і котеджі</em>": "Rooms, suites <em>&amp; cottages</em>",
    "Попередній номер": "Previous room",
    "Наступний номер": "Next room",
    "Номери — гортайте вбік": "Rooms — scroll sideways",
    "Ліжко з білою постіллю і дерев'яним узголів'ям": "A bed with white linen and a wooden headboard",
    "Двомісний New": "Double New",
    "20 м² · 2 гостей · балкон": "20 m² · 2 guests · balcony",
    "від — ₴ / ніч": "from — ₴ / night",
    "Ліжко біля вікна з видом на ліс": "A bed by a window overlooking the forest",
    "Сімейний номер": "Family Room",
    "43 м² · 2 кімнати": "43 m² · 2 rooms",
    "Ліжко з лампою біля дерев'яної стіни": "A bed and lamp against a wooden wall",
    ">Дуплекс<": ">Duplex<",
    "45–50 м² · 4 гостей · 2 рівні": "45–50 m² · 4 guests · 2 levels",
    "Піч у дерев'яному будиночку": "A wood stove in a timber cabin",
    "Люкс із каміном": "Suite with Fireplace",
    "Котедж · 55 м² · 3 кімнати": "Cottage · 55 m² · 3 rooms",
    "Котедж зі світлом у вікнах серед засніженого лісу": "A cottage with lit windows in a snowy forest",
    "Котедж повністю": "Whole Cottage",
    "180 м² · 8 кімнат": "180 m² · 8 rooms",
    # experiences
    "Гаряча купіль серед засніженого лісу": "A hot tub in a snowy forest",
    "Дерев'яна сауна з піччю": "A wooden sauna with a stove",
    "Довгий стіл зі свічками": "A long table with candles",
    "Піч у дерев'яній вітальні": "A stove in a wooden living room",
    "03 · Відпочинок": "03 · Unwind",
    "Дні, що минають <em>у гірському</em> темпі": "Days that run <em>on mountain</em> time",
    "Басейн і джакузі": "Pool &amp; jacuzzi",
    "Відкритий басейн у теплий сезон, джакузі — після лиж чи гірського маршруту.": "An outdoor pool in the warm season, and a jacuzzi after skiing or a mountain hike.",
    "<h3>Сауна</h3>": "<h3>Sauna</h3>",
    "Глибоке тепло, коли за вікном мінус. Входить у пакети відпочинку.": "Deep warmth while it's freezing outside. Included in our stay packages.",
    "Ресторан «GUK»": "GUK Restaurant",
    "Авторська кухня в карпатському стилі на першому поверсі готелю.": "Signature Carpathian-style cooking on the hotel's ground floor.",
    "Камінна зала й мангал": "Fireplace hall &amp; barbecue",
    "Вечори біля вогню — всередині чи на свіжому повітрі.": "Evenings by the fire, indoors or out in the fresh air.",
    # panorama
    "Гори з усіх боків.<br><em>Тиша — всередині.</em>": "Mountains all around.<br><em>Quiet within.</em>",
    # day
    "04 · Один день": "04 · One day",
    "Від першого світла <em>до каміна</em>": "From first light <em>to the fireside</em>",
    "Ялини в ранковому тумані": "Spruces in the morning mist",
    "<h3>Ранок</h3>": "<h3>Morning</h3>",
    "Туман над ялинами і гарячий сніданок.": "Mist over the spruces and a hot breakfast.",
    "Гора в низьких хмарах": "A mountain in low cloud",
    "<h3>Схили</h3>": "<h3>Slopes</h3>",
    "Кілометр до підйомника — і ви на трасах.": "One kilometre to the lift, and you're on the pistes.",
    "Дерев'яна купіль у лісі": "A wooden hot tub in the forest",
    "<h3>Тепло</h3>": "<h3>Warmth</h3>",
    "Сауна і джакузі після холодного дня.": "Sauna and jacuzzi after a cold day.",
    "Кам'яний будинок і дерев'яна купіль увечері": "A stone house and wooden hot tub in the evening",
    "<h3>Вечір</h3>": "<h3>Evening</h3>",
    "Вечеря, вогонь і тиша гір.": "Dinner, the fire and the quiet of the mountains.",
    # included
    "05 · Для кожного гостя": "05 · For every guest",
    "Що входить <em>у проживання</em>": "Included <em>in your stay</em>",
    "Безкоштовний для всіх гостей.": "Free for all guests.",
    "<h3>Парковка</h3>": "<h3>Parking</h3>",
    "Безкоштовні місця для гостей з авто.": "Free spaces for guests arriving by car.",
    "Сушарка для лиж": "Ski drying room",
    "Окреме приміщення для спорядження й одягу.": "A separate room for gear and clothing.",
    "<h3>Прибирання</h3>": "<h3>Housekeeping</h3>",
    "Рушники — щодня, постіль — раз на три дні.": "Fresh towels daily, bed linen every three days.",
    "<h3>Трансфер</h3>": "<h3>Transfers</h3>",
    "Зустрінемо й відвеземо — за запитом.": "We'll pick you up and drop you off, on request.",
    "Дитяче ліжечко": "Baby cot",
    "За запитом, як і додаткове ліжко.": "On request, as is an extra bed.",
    # packages
    "06 · Пропозиції": "06 · Offers",
    "Причини <em>залишитися</em> довше": "Reasons to <em>stay</em> a little longer",
    "Уточнити умови": "Ask about terms",
    "Купіль серед засніженого лісу": "A hot tub in a snowy forest",
    "Все включено": "All inclusive",
    "Без жодних турбот": "Nothing to worry about",
    "Триразове харчування, напої, басейн, сауна, джакузі та мангальна зона. Діти до 7 років — безкоштовно.":
        "Three meals a day, drinks, pool, sauna, jacuzzi and barbecue area. Children under 7 stay free.",
    "Гори в тумані": "Mountains in the mist",
    "Оксамитовий сезон": "Velvet season",
    "Від 600 грн з особи": "From 600 UAH per person",
    "Сніданок, басейн, джакузі та мангал.": "Breakfast, pool, jacuzzi and barbecue.",
    "Святковий стіл": "A table set for a celebration",
    "Групи від 20 осіб": "Groups of 20+",
    "Для команд і турів": "For teams and tours",
    "Шведська лінія, мангал, місця для керівника й водія — безкоштовно.": "Buffet, barbecue area, and free places for the group leader and driver.",
    # location
    "07 · Як нас знайти": "07 · Getting here",
    "Поляниця, <em>урочище</em> Стаїще": "Polianytsia, <em>Staishche</em> tract",
    "<dt>Адреса</dt>": "<dt>Address</dt>",
    "урочище Стаїще, 265, с. Поляниця": "265 Staishche tract, Polianytsia village",
    "<dt>Підйомник</dt>": "<dt>Ski lift</dt>",
    "<dt>Телефон</dt>": "<dt>Phone</dt>",
    "<dt>Пошта</dt>": "<dt>Email</dt>",
    "Прокласти маршрут": "Get directions",
    "Готель GUK на карті": "Hotel GUK on the map",
    # faq
    "08 · Перед поїздкою": "08 · Before you travel",
    "Часті <em>питання</em>": "Frequently asked <em>questions</em>",
    "Чи можна з домашніми тваринами?": "Can I bring my pet?",
    "Так, за попередньою домовленістю. Напишіть або зателефонуйте нам перед бронюванням.": "Yes, by prior arrangement. Please message or call us before booking.",
    "Як працює оплата?": "How does payment work?",
    "Половину вартості проживання ви сплачуєте при заселенні, решту — при виїзді.": "You pay half the cost of your stay at check-in and the rest at check-out.",
    "Чи є дитяче ліжечко?": "Do you have a baby cot?",
    "Так, за запитом. Також у номери можна поставити додаткове ліжко.": "Yes, on request. We can also add an extra bed to most rooms.",
    "Чи є знижки для військових?": "Are there discounts for military personnel?",
    "Так, 10% на номери, у яких проживають військовослужбовці.": "Yes, 10% off rooms occupied by service members.",
    "Чи приймаєте групи?": "Do you host groups?",
    "Так, для груп від 20 осіб є окремі умови: шведська лінія, мангальна зона, безкоштовні місця для керівника та водія.":
        "Yes. Groups of 20 or more get special terms: a buffet, the barbecue area, and free places for the group leader and driver.",
    # footer
    "Поляниця · Карпати": "Polianytsia · Carpathians",
    "Приїжджайте <em>в тишу.</em>": "Come for <em>the quiet.</em>",
    "<p class=\"footer__title\">Адреса</p>": "<p class=\"footer__title\">Address</p>",
    "с. Поляниця, урочище Стаїще, 265<br>Рецепція працює цілодобово": "265 Staishche tract, Polianytsia<br>Front desk open 24/7",
    "<p class=\"footer__title\">Контакти</p>": "<p class=\"footer__title\">Contact</p>",
    "<p class=\"footer__title\">Сайт</p>": "<p class=\"footer__title\">Explore</p>",
    "<p class=\"footer__title\">Соцмережі</p>": "<p class=\"footer__title\">Follow</p>",
    "Готель «GUK»": "Hotel GUK",
    "Фото: Unsplash (тимчасові)": "Photos: Unsplash (temporary)",
    "Нагору ↑": "Back to top ↑",
    # nav (short words last; whole tags to avoid accidental matches)
    ">Дім<": ">The house<",
    ">Номери<": ">Rooms<",
    ">Відпочинок<": ">Unwind<",
    ">Пропозиції<": ">Offers<",
    ">Контакти<": ">Contact<",
}

html = open(SRC, encoding="utf-8").read()

# 1. Ховаємо коментарі, щоб не перекладати їх
comments = []
def stash(m):
    comments.append(m.group(0))
    return f"\x00{len(comments)-1}\x00"
html = re.sub(r"<!--.*?-->", stash, html, flags=re.S)

# 2. Переклад: довші фрази першими; пробіли/переноси в оригіналі — гнучкі
for src in sorted(T, key=len, reverse=True):
    pattern = r"\s+".join(re.escape(part) for part in src.split())
    html, n = re.subn(pattern, lambda m, d=T[src]: d, html)
    if n == 0:
        print("NOT FOUND:", src[:60])

# 3. Шляхи: сторінка лежить у папці en/
html = html.replace('<html lang="uk">', '<html lang="en">')
html = html.replace('href="css/', 'href="../css/').replace('src="js/', 'src="../js/')
html = html.replace('hreflang="uk" href="index.html"', 'hreflang="uk" href="../index.html"')
html = html.replace('hreflang="en" href="en/index.html"', 'hreflang="en" href="index.html"')
html = html.replace('<a href="index.html" aria-current="true" lang="uk">', '<a href="../index.html" lang="uk">')
html = html.replace('<a href="en/index.html" lang="en">', '<a href="index.html" aria-current="true" lang="en">')

# 4. Повертаємо коментарі
html = re.sub(r"\x00(\d+)\x00", lambda m: comments[int(m.group(1))], html)

open(DST, "w", encoding="utf-8").write(html)

# Перевірка: чи лишилась кирилиця у видимому тексті
visible = re.sub(r"<!--.*?-->", "", html, flags=re.S)
left = sorted(set(re.findall(r"[^<>\"]*[А-Яа-яЇїІіЄєҐґ][^<>\"]*", visible)))
print("Cyrillic left:", [x.strip() for x in left if x.strip()])
