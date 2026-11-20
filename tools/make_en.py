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
    'Камінна зала з кріслами й лижним спорядженням': 'The fireplace hall with armchairs and ski gear',
    'Камінна зала · після катання': 'The fireplace hall · after a day on the slopes',
    'Готель «Гук» — номери та котеджі за 1 км від Буковелю': 'Hotel GUK — rooms and cottages 1 km from Bukovel',
    'Готель і котеджі в Поляниці, за кілометр від підйомників Буковеля. Ресторан карпатської кухні, басейн, сауна, джакузі, мангальна зона.': 'A hotel and cottages in Polianytsia, a kilometre from the Bukovel ski lifts. Carpathian restaurant, pool, sauna, jacuzzi and barbecue area.',
    'Готель GUK — на початок сторінки': 'Hotel GUK — back to top',
    'Головне меню': 'Main menu',
    'Мова сайту': 'Site language',
    'Увімкнути темну тему': 'Switch to dark theme',
    'Увімкнути світлу тему': 'Switch to light theme',
    'Забронювати номер': 'Book a room',
    'Забронювати': 'Book now',
    'Закрити ✕': 'Close ✕',
    '>Меню<': '>Menu<',
    '<span>Заїзд</span>': '<span>Check-in</span>',
    '<span>Виїзд</span>': '<span>Check-out</span>',
    '<span>Гості</span>': '<span>Guests</span>',
    '1 гість': '1 guest',
    '2 гостей</option>': '2 guests</option>',
    '3 гостей': '3 guests',
    '4 гостей</option>': '4 guests</option>',
    '5+ гостей': '5+ guests',
    'Перевірити дати': 'Check dates',
    'Пропозиції готелю': 'Hotel offers',
    'Знижка 10% для військових': '10% off for military personnel',
    'Діти до 7 років — безкоштовно в пакетах': 'Children under 7 stay free on packages',
    'Групам від 20 осіб — окремі умови': 'Special terms for groups of 20+',
    '01 · Дім': '01 · The house',
    "Дерев'яний дім, де ранок починається <em>з туману</em> за вікном.": 'A wooden house where mornings <em>begin with mist</em> at the window.',
    'Обрати номер': 'Choose a room',
    '<dt>до підйомника</dt>': '<dt>to the ski lift</dt>',
    '02 · Номери': '02 · Rooms',
    'Номери, люкси <em>і котеджі</em>': 'Rooms, suites <em>&amp; cottages</em>',
    'Попередній номер': 'Previous room',
    'Наступний номер': 'Next room',
    'Номери — гортайте вбік': 'Rooms — scroll sideways',
    'від — ₴ / ніч': 'from — ₴ / night',
    '03 · Відпочинок': '03 · Unwind',
    'Дні, що минають <em>у гірському</em> темпі': 'Days that run <em>on mountain</em> time',
    'Басейн і джакузі': 'Pool &amp; jacuzzi',
    'Ресторан «GUK»': 'GUK Restaurant',
    'Авторська кухня в карпатському стилі на першому поверсі готелю.': "Signature Carpathian-style cooking on the hotel's ground floor.",
    'Камінна зала й мангал': 'Fireplace hall &amp; barbecue',
    'Вечори біля вогню — всередині чи на свіжому повітрі.': 'Evenings by the fire, indoors or out in the fresh air.',
    'Гори з усіх боків.<br><em>Тиша — всередині.</em>': 'Mountains all around.<br><em>Quiet within.</em>',
    '04 · Один день': '04 · One day',
    'Від першого світла <em>до каміна</em>': 'From first light <em>to the fireside</em>',
    '<h3>Ранок</h3>': '<h3>Morning</h3>',
    '<h3>Схили</h3>': '<h3>Slopes</h3>',
    "Дерев'яна купіль у лісі": 'A wooden hot tub in the forest',
    '<h3>Тепло</h3>': '<h3>Warmth</h3>',
    'Сауна і джакузі після холодного дня.': 'Sauna and jacuzzi after a cold day.',
    "Кам'яний будинок і дерев'яна купіль увечері": 'A stone house and wooden hot tub in the evening',
    '<h3>Вечір</h3>': '<h3>Evening</h3>',
    'Вечеря, вогонь і тиша гір.': 'Dinner, the fire and the quiet of the mountains.',
    '05 · Для кожного гостя': '05 · For every guest',
    '<h3>Парковка</h3>': '<h3>Parking</h3>',
    'Сушарка для лиж': 'Ski drying room',
    'Окреме приміщення для спорядження й одягу.': 'A separate room for gear and clothing.',
    '06 · Пропозиції': '06 · Offers',
    'Уточнити умови': 'Ask about terms',
    'Купіль серед засніженого лісу': 'A hot tub in a snowy forest',
    'Гори в тумані': 'Mountains in the mist',
    '07 · Як нас знайти': '07 · Getting here',
    'Поляниця, <em>урочище</em> Стаїще': 'Polianytsia, <em>Staishche</em> tract',
    '<dt>Адреса</dt>': '<dt>Address</dt>',
    'урочище Стаїще, 265, с. Поляниця': '265 Staishche tract, Polianytsia village',
    '<dt>Підйомник</dt>': '<dt>Ski lift</dt>',
    '<dt>Телефон</dt>': '<dt>Phone</dt>',
    '<dt>Пошта</dt>': '<dt>Email</dt>',
    'Прокласти маршрут': 'Get directions',
    'Готель GUK на карті': 'Hotel GUK on the map',
    '08 · Перед поїздкою': '08 · Before you travel',
    'Часті <em>питання</em>': 'Frequently asked <em>questions</em>',
    'Чи можна з домашніми тваринами?': 'Can I bring my pet?',
    'Так, за попередньою домовленістю. Напишіть або зателефонуйте нам перед бронюванням.': 'Yes, by prior arrangement. Please message or call us before booking.',
    'Як працює оплата?': 'How does payment work?',
    'Чи є дитяче ліжечко?': 'Do you have a baby cot?',
    'Чи є знижки для військових?': 'Are there discounts for military personnel?',
    'Так, 10% на номери, у яких проживають військовослужбовці.': 'Yes, 10% off rooms occupied by service members.',
    'Поляниця · Карпати': 'Polianytsia · Carpathians',
    'Приїжджайте <em>в тишу.</em>': 'Come for <em>the quiet.</em>',
    '<p class="footer__title">Адреса</p>': '<p class="footer__title">Address</p>',
    '<p class="footer__title">Контакти</p>': '<p class="footer__title">Contact</p>',
    '<p class="footer__title">Сайт</p>': '<p class="footer__title">Explore</p>',
    '<p class="footer__title">Соцмережі</p>': '<p class="footer__title">Follow</p>',
    'Готель «GUK»': 'Hotel GUK',
    'Нагору ↑': 'Back to top ↑',
    '>Дім<': '>The house<',
    '>Номери<': '>Rooms<',
    '>Відпочинок<': '>Unwind<',
    '>Пропозиції<': '>Offers<',
    '>Контакти<': '>Contact<',
    'Тиша, <em>що чекає</em> поруч з&nbsp;Буковелем': 'Mountain quiet, <em>right next</em> to&nbsp;Bukovel',
    'Готель GUK у Карпатах': 'Hotel GUK in the Carpathians',
    'Рейтинг 9,1 на Booking': 'Rated 9.1 on Booking.com',
    '2,5 км до підйомника': '2.5 km to the ski lift',
    '<dd>2,5 км</dd>': '<dd>2.5 km</dd>',
    '≈ 2,5 км': '≈ 2.5 km',
    '<dd>9,1</dd>': '<dd>9.1</dd>',
    'Можна з тваринами': 'Pets welcome',
    "Стильний готель в урочищі Стаїще. Номери з балконами, ресторан із камінною залою на першому поверсі й екологічні матеріали в інтер'єрах.": 'A stylish hotel in the Staishche tract. Rooms with balconies, a restaurant with a fireplace hall on the ground floor and natural materials throughout.',
    'Кілька хвилин авто — і ви на схилах Буковеля.': "A few minutes by car, and you're on the Bukovel slopes.",
    'типів номерів та великий котедж': 'room types and a large cottage',
    'Від затишного двомісного до котеджу на 180 м² для компанії до 20 осіб.': 'From a cosy double to a 180 m² cottage for groups of up to 20.',
    'рейтинг на Booking.com': 'rating on Booking.com',
    'Тільки чесні відгуки.': 'Only genuine reviews.',
    'Відкритий басейн у теплий сезон, джакузі працює й у морози.': 'An outdoor pool in the warm season; the jacuzzi works even in frosty weather.',
    'Сауна та чан': 'Sauna &amp; hot tub',
    'Глибоке тепло, коли за вікном мінус.': "Deep warmth while it's freezing outside.",
    'Зал для практик та конференцій': 'Practice &amp; conference hall',
    'Зал для практик і конференцій': 'Practice and conference hall',
    'Місце, де можна знайти гармонію з тілом і розумом.': 'A place to find harmony of body and mind.',
    'Або провести тімбілдинг для вашого корпоративу.': 'Or to host a team-building day for your company.',
    'Що входить <em>у проживання</em> взимку': 'Included <em>in your stay</em> in winter',
    '<h3>Сніданок</h3>': '<h3>Breakfast</h3>',
    'У вигляді шведської лінії.': 'Served as a buffet.',
    'Тепле джакузі': 'Warm jacuzzi',
    'Щодня з 18:00 до 22:00.': 'Daily from 18:00 to 22:00.',
    'Безкоштовний для всіх гостей.': 'Free for all guests.',
    'Безкоштовні місця для гостей з авто.': 'Free spaces for guests arriving by car.',
    '<h3>Прибирання</h3>': '<h3>Housekeeping</h3>',
    'Щоденне прибирання номера.': 'Your room is cleaned daily.',
    'Події, <em>що в нас</em> відбуваються': "What's <em>on</em> at GUK",
    'Святкування': 'Celebrations',
    'Незабутній Новий рік': 'An unforgettable New Year',
    'Новорічне святкування із сучасним рок-гуртом і смачною гастровечерею.': "A New Year's party with a live rock band and a gourmet dinner.",
    'Дізнатися більше': 'Learn more',
    'Дозвілля': 'Leisure',
    '<h3>Кіновечір</h3>': '<h3>Movie night</h3>',
    'Щовечора з 20:00 до 22:00 у конференц-залі — кіновечір.': 'Every evening from 20:00 to 22:00, movie night in the conference hall.',
    'Заняття йогою': 'A yoga class',
    '<h3>Йога</h3>': '<h3>Yoga</h3>',
    'Тричі на тиждень з 10:00 до 11:00 — заняття йогою, щоб знайти гармонію душі й тіла.': 'Three times a week from 10:00 to 11:00, yoga to bring body and mind into balance.',
    'Чи є трансфер?': 'Do you offer transfers?',
    'Так, за додаткову плату наші партнери з радістю організують трансфер із залізничного вокзалу або до підйомників.': 'Yes. For an extra fee, our partners will gladly arrange a transfer from the railway station or to the ski lifts.',
    'При бронюванні потрібно внести передоплату 30% від суми. Якщо ви скасовуєте бронювання не пізніше ніж за 21 день до заїзду, передоплату повертаємо в повному обсязі. Решту — при заїзді.': 'A 30% deposit is required when booking. If you cancel at least 21 days before arrival, we refund the deposit in full. The balance is paid on arrival.',
    'Так, за запитом.': 'Yes, on request.',
    'Чи працює басейн узимку?': 'Is the pool open in winter?',
    'На жаль, узимку басейн не працює.': 'Unfortunately, the pool is closed in winter.',
    'с. Поляниця, урочище Стаїще, 265': '265 Staishche tract, Polianytsia',
    '>Про нас<': '>About<',
    '>Події<': '>Events<',
    'Гість у джакузі на терасі з видом на гори': 'A guest in the jacuzzi on a terrace overlooking the mountains',
    "Дерев'яна сауна з теплим світлом": 'A wooden sauna in warm light',
    'Святково накритий стіл у ресторані': 'A table set for a feast in the restaurant',
    'Вечір із гітарою біля каміна': 'An evening with a guitar by the fireplace',
    'Шведська лінія на сніданку': 'The breakfast buffet',
    'Засніжені схили Буковеля в низьких хмарах': 'Snowy Bukovel slopes under low cloud',
    'Гарячий сніданок і туман над ялинами.': 'A hot breakfast and mist over the spruces.',
    'Кілька хвилин авто — і ви на трасах.': "A few minutes by car, and you're on the pistes.",
    'Двомісний номер у готелі': 'A double room in the main hotel',
    '20 м² · 2 гостей · двоспальне ліжко': '20 m² · 2 guests · double bed',
    'Двомісний номер з двоспальним ліжком': 'A double room with a double bed',
    'Двомісний з окремими ліжками': 'A double room with two separate beds',
    '20 м² · 2 гостей · 2 окремі ліжка': '20 m² · 2 guests · 2 single beds',
    'Номер із двома окремими ліжками': 'A room with two single beds',
    'Двомісний з окремим входом з вулиці': 'A double room with its own entrance from outside',
    '20 м² · 2 гостей · двоспальне або 2 окремі ліжка': '20 m² · 2 guests · double or 2 single beds',
    'Двомісний номер з виходом на вулицю': 'A double room with direct outdoor access',
    'Двомісний номер у котеджі': 'A double room in the cottage',
    "20 м² · 2 гостей · дерев'яний інтер'єр": '20 m² · 2 guests · wooden interior',
    "Дерев'яний двомісний номер у котеджі": 'A wood-panelled double room in the cottage',
    'Тримісний номер з балконом': 'A triple room with a balcony',
    '25 м² · 3 гостей · балкон': '25 m² · 3 guests · balcony',
    "Дві кімнати й балкон — для сім'ї": 'Two rooms and a balcony, made for families',
    '43 м² · 4 гостей · 2 кімнати': '43 m² · 4 guests · 2 rooms',
    'Сімейний номер із двох кімнат': 'A two-room family room',
    'Дворівневий номер': 'A two-level room',
    '45–50 м² · 4 гостей · 2 поверхи': '45–50 m² · 4 guests · 2 levels',
    'Дворівневий номер зі сходами': 'A two-level room with a staircase',
    'Однокімнатний чотиримісний': 'A single room that sleeps four',
    '20 м² · 4 гостей · 2 двоспальні ліжка': '20 m² · 4 guests · 2 double beds',
    'Чотиримісний номер із двома двоспальними ліжками': 'A room for four with two double beds',
    '<h3>Люкс із каміном</h3>': '<h3>Suite with Fireplace</h3>',
    'Дві спальні й хол із каміном у котеджі': 'Two bedrooms and a lounge with a fireplace, in the cottage',
    '55 м² · 4 гостей · 3 кімнати': '55 m² · 4 guests · 3 rooms',
    'Камін у люксі': 'The fireplace in the suite',
    '<h3>Мансардний</h3>': '<h3>Attic Room</h3>',
    'Затишний номер під дахом котеджу': 'A cosy room under the cottage roof',
    "Мансардний номер з дерев'яними стінами": 'An attic room with wooden walls',
    '<h3>Котедж повністю</h3>': '<h3>Whole Cottage</h3>',
    'Цілий котедж із кухнею та каміном': 'The entire cottage, with a kitchen and fireplace',
    '180 м² · до 20 гостей · 8 кімнат': '180 m² · up to 20 guests · 8 rooms',
    'Кімната в котеджі': 'A room in the cottage',
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
