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
    'Обрати номер': 'Choose a room',
    '<dt>до підйомника</dt>': '<dt>to the ski lift</dt>',
    '02 · Номери': '02 · Rooms',
    'Попередній номер': 'Previous room',
    'Наступний номер': 'Next room',
    'Номери — гортайте вбік': 'Rooms — scroll sideways',
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
    '05 · Для кожного гостя': '05 · For every guest',
    '<h3>Парковка</h3>': '<h3>Parking</h3>',
    'Сушарка для лиж': 'Ski drying room',
    'Окреме приміщення для спорядження й одягу.': 'A separate room for gear and clothing.',
    '06 · Пропозиції': '06 · Offers',
    'Уточнити умови': 'Ask about terms',
    '08 · Як нас знайти': '08 · Getting here',
    'Поляниця, <em>урочище</em> Стаїще': 'Polianytsia, <em>Staishche</em> tract',
    '<dt>Адреса</dt>': '<dt>Address</dt>',
    'урочище Стаїще, 265, с. Поляниця': '265 Staishche tract, Polianytsia village',
    '<dt>Підйомник</dt>': '<dt>Ski lift</dt>',
    '<dt>Телефон</dt>': '<dt>Phone</dt>',
    '<dt>Пошта</dt>': '<dt>Email</dt>',
    'Прокласти маршрут': 'Get directions',
    'Готель GUK на карті': 'Hotel GUK on the map',
    '09 · Перед поїздкою': '09 · Before you travel',
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
    'Місце спокою, де ранок починається <em>з туману</em> за вікном.': 'A place of calm, where mornings <em>begin with mist</em> at the window.',
    'Номери <em>та котедж на велику компанію</em>': 'Rooms <em>and a cottage for a big group</em>',
    'Кіновечір у конференц-залі': 'Movie night in the conference hall',
    'Новорічне святкування в GUK': "New Year's celebration at GUK",
    # ---------- 10. Відгуки ----------
    '07 · Відгуки': '07 · Reviews',
    'Гості скажуть <em>краще</em> за нас': 'Our guests <em>say it</em> best',
    'Попередній відгук': 'Previous review',
    'Наступний відгук': 'Next review',
    'Відгуки — гортайте вбік': 'Reviews — scroll sideways',
    'Усі відгуки в Google': 'All reviews on Google',
    '#reviews">Відгуки<': '#reviews">Reviews<',
    'Оцінка 5 з 5': 'Rated 5 out of 5',
    'Оцінка 4 з 5': 'Rated 4 out of 5',
    "Не вперше, і знову задоволені. Чудовий вид із вікон номера, тиша й сімейна атмосфера. Відпочивали і взимку, і восени — у номерах завжди тепло. Сніданки ситні, а млинці з вишнями та маком — то любов. Обов'язково завітаємо ще!": "Not our first stay, and happy once again. Great views from the room, peace and quiet, a real family feel. We've stayed in winter and in autumn — the rooms are always warm. Hearty breakfasts, and the cherry and poppy-seed pancakes are pure love. We'll definitely be back!",
    '<small>Google · з друзями</small>': '<small>Google · with friends</small>',
    "Дуже затишне місце. Гарний, але ненав'язливий сервіс, смачна домашня кухня, і можна поспілкуватися з шеф-кухарем особисто. Чан, сауна, джакузі — усе прямо при готелі. У цього місця є душа.": 'A really cosy place. Attentive but unobtrusive service, delicious home cooking, and you can chat with the chef in person. Hot tub, sauna, jacuzzi — all right at the hotel. This place has a soul.',
    'Нас без проблем заселили раніше й завжди йшли назустріч. Було відчуття справжньої турботи про гостей. Сніданки — окрема любов! Атмосфера чудова, а ставлення до гостей і домашніх улюбленців просто прекрасне.': 'They checked us in early without any fuss and always met us halfway. You could feel they genuinely care about their guests. The breakfasts deserve a love letter of their own! A wonderful atmosphere, and lovely to guests and pets alike.',
    '<strong>Оксана С.</strong>': '<strong>Oksana S.</strong>',
    '"true">О</span>': '"true">O</span>',
    "<small>Google · із сім'єю</small>": '<small>Google · with family</small>',
    'Ресторан із панорамним видом на гори, дуже затишно. Персонал привітний і турботливий — відчула себе як удома. А кухня — клас: борщ найкращий у всьому Буковелі!': 'A restaurant with a panoramic mountain view — so cosy. Warm, caring staff; I felt right at home. And the food is superb: the best borscht in all of Bukovel!',
    '<small>Google · ресторан</small>': '<small>Google · restaurant</small>',
    "Через три дні відпочинку знали весь персонал на ім'я — і в результаті найвищий бал! Особливо сподобалося, що в номері був камін і нам дозволили його розпалювати: це +100 до затишку.": 'Three days in, we knew every member of staff by name — top marks! We especially loved having a fireplace in our room that we were allowed to light: +100 to cosiness.',
    'Дуже привітний персонал. У номерах чисто, прибирання щодня, є все необхідне. Комфортні матраци й тепла ковдра. Є зал для практик і кіно на проєкторі. Дуже класне джакузі та гаряча лазня.': "Very friendly staff. The rooms are spotless, cleaned daily, with everything you need. Comfy mattresses and warm duvets. There's a practice hall and movies on a projector. A great jacuzzi and a hot bathhouse.",
    'Чудовий готель для тихого сімейного відпочинку. Доброзичливі люди й сервіс на високому рівні: якщо треба перенести заселення чи виселення — завжди йдуть назустріч. Тихий мальовничий куточок, а до центру Буковеля — невеличка прогулянка пішки.': 'A wonderful hotel for a quiet family break. Kind people and top-notch service: if you need to move check-in or check-out, they always accommodate. A peaceful, picturesque spot — and the centre of Bukovel is just a short walk away.',
    '<strong>Юлія Д.</strong>': '<strong>Yuliia D.</strong>',
    '"true">Ю</span>': '"true">Y</span>',
    "Приємна атмосфера, доброзичливий персонал і власники. Відпочили на повну завдяки джакузі, спа й чану. Їжа смачна — обов'язково спробуйте узвар, він повертає в дитинство. Обов'язково приїду ще!": "A lovely atmosphere, and friendly staff and owners. We fully recharged thanks to the jacuzzi, spa and hot tub. Tasty food — be sure to try the uzvar, it takes you straight back to childhood. I'll definitely come again!",
    '<strong>Руслан П.</strong>': '<strong>Ruslan P.</strong>',
    '"true">Р</span>': '"true">R</span>',
    '<small>Google · у парі</small>': '<small>Google · as a couple</small>',
    '10 днів відпочивала в цьому готелі. Дуже класне розташування: поруч магазини й кафе, швидко дістатися до популярних місць Буковеля. З номера — чудовий краєвид. Персонал уважний, завжди допоможуть.': "I stayed here for 10 days. A great location: shops and cafés nearby, and Bukovel's popular spots are close. A beautiful view from my room. Attentive staff who are always happy to help.",
    'Дуже затишно й атмосферно. Особливо сподобалося джакузі. У номері чисто, дуже зручне ліжко й красивий вид на одиноку смереку на горі. Персонал приємний, кухня смачна. Однозначно 10/10 :)': 'So cosy and atmospheric. We especially loved the jacuzzi. The room was clean, the bed very comfortable, with a lovely view of a lone spruce on the hill. Pleasant staff, tasty food. A definite 10/10 :)',
    '<strong>Богдана</strong>': '<strong>Bohdana</strong>',
    '"true">Б</span>': '"true">B</span>',
    'Дуже атмосферний ресторан із цікавою історією та неймовірно смачною домашньою кухнею. Дякуємо дівчатам за турботливе обслуговування!': 'A very atmospheric restaurant with an interesting story and incredibly tasty home cooking. Thanks to the girls for such caring service!',
    '<strong>Дарья M.</strong>': '<strong>Daria M.</strong>',
    '"true">Д</span>': '"true">D</span>',
    # ---------- Правки власника ----------
    'Вечеря, вогонь каміну і легка жива музика.': 'Dinner, a crackling fire and light live music.',
    'На жаль, узимку басейн не працює, але працює гаряче джакузі.': "Sadly the pool is closed in winter, but the hot jacuzzi is open.",
    # ---------- 10. Відгуки з Booking + карусель ----------
    'Оцінка 10 з 10': 'Rated 10 out of 10',
    '501 відгук на Booking.com': '501 reviews on Booking.com',
    'Усі відгуки на Booking.com': 'All reviews on Booking.com',
    '"карусель"': '"carousel"',
    "<small>Booking.com · із сім'єю</small>": '<small>Booking.com · with family</small>',
    'Гарне розташування, вид на гори, басейн, джакузі, чан. Дуже комфортно й затишно — приємно бути в будь-якому куточку готелю. Усе продумано й зроблено з турботою. Кухня дуже смачна, сніданки різноманітні.': 'A great location with mountain views, a pool, jacuzzi and hot tub. So comfortable and cosy — every corner of the hotel is a pleasure to be in. Everything is thought through and made with care. Delicious food and varied breakfasts.',
    '<strong>Ірина</strong>': '<strong>Iryna</strong>',
    '"true">І</span>': '"true">I</span>',
    "Дуже сподобалося ставлення: привітний персонал, гарні номери, красивий краєвид, хороший басейн і класне джакузі. Почуваєшся як удома — здебільшого відпочивають сім'ями, тож спокійно й тихо. Ми тут уже вдруге і плануємо приїхати ще.": "We loved how we were treated: friendly staff, lovely rooms, a beautiful view, a good pool and a great jacuzzi. It feels like home — mostly families stay here, so it's calm and quiet. This was our second visit and we're planning to come back.",
    '<strong>Володимир</strong>': '<strong>Volodymyr</strong>',
    '"true">В</span>': '"true">V</span>',
    'Привітний персонал, чудові сніданки, чистий гарний готель і басейни. Дуже смачна кухня. Ціна для такого відпочинку невисока, поруч багато супермаркетів. Раджу для відпочинку!': 'Friendly staff, wonderful breakfasts, a clean and beautiful hotel with pools. Really tasty food. The price is very fair for a holiday like this, and there are plenty of supermarkets nearby. Highly recommended!',
    'Ціна і якість повністю відповідають очікуванням. Затишні номери, чисто, привітний персонал, сніданки на гідному рівні.': 'Price and quality fully lived up to our expectations. Cosy rooms, spotless, friendly staff and breakfasts of a high standard.',
    '<strong>Костянтин</strong>': '<strong>Kostiantyn</strong>',
    '"true">К</span>': '"true">K</span>',
    'Сніданок — бомба, вистачало на цілий день! Джакузі — бомба. Усе було дуже гарно.': 'The breakfast was amazing — it kept us going all day! The jacuzzi was amazing too. Everything was just lovely.',
    '<strong>Лариса</strong>': '<strong>Larysa</strong>',
    '"true">Л</span>': '"true">L</span>',
    # ---------- 10. Відгуки з Booking + карусель ----------
    'Оцінка 10 з 10': 'Rated 10 out of 10',
    '501 відгук на Booking.com': '501 reviews on Booking.com',
    'Усі відгуки на Booking.com': 'All reviews on Booking.com',
    "<small>Booking.com · із сім'єю</small>": '<small>Booking.com · with family</small>',
    'Дуже привітний персонал, на території чисто. Смачна кухня й неймовірні сніданки. Вид на гори — супер. Дуже задоволені, що обрали саме цей готель!': 'Very friendly staff and a spotless property. Tasty food and incredible breakfasts. The mountain view is superb. So glad we chose this hotel!',
    '<strong>Олена</strong>': '<strong>Olena</strong>',
    '"true">О</span>': '"true">O</span>',
    'Чистий і просторий номер із гарними краєвидами на гори! Привітний персонал, гарний великий басейн, смачна кухня!': 'A clean, spacious room with beautiful mountain views! Friendly staff, a lovely big pool and delicious food!',
    '<strong>Микола</strong>': '<strong>Mykola</strong>',
    '"true">М</span>': '"true">M</span>',
    "Дуже смачний сніданок! Розташування — у самому центрі Карпат. Привітний персонал, уся їжа смачна, ціни адекватні. Наступного разу обов'язково знову оберемо готель «Гук»!": "A really delicious breakfast! The location is right in the heart of the Carpathians. Friendly staff, tasty food and fair prices. Next time we'll definitely choose GUK again!",
    '<strong>Воловик</strong>': '<strong>Volovyk</strong>',
    '"true">В</span>': '"true">V</span>',
    'Цікавий стильний готель, смачні сніданки — хочеться повернутися ще!': "An interesting, stylish hotel with tasty breakfasts — we'd love to come back!",
    'Привітний персонал, дуже затишна атмосфера, доступні ціни, смачні сніданки. Рекомендую!': 'Friendly staff, a really cosy atmosphere, affordable prices and tasty breakfasts. Highly recommended!',
    '<strong>Юлія</strong>': '<strong>Yuliia</strong>',
    '"true">Ю</span>': '"true">Y</span>',
    '<small>Booking.com · з друзями</small>': '<small>Booking.com · with friends</small>',
    '<small>Booking.com · сам</small>': '<small>Booking.com · solo trip</small>',
    '389 відгуків у Google': '389 reviews on Google',
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

# Ціни номерів: «від 3 000 ₴ / ніч» → «from 3,000 ₴ / night»
html = re.sub(r"від (\d+) (\d{3}) ₴ / ніч", r"from \1,\2 ₴ / night", html)

# 3. Шляхи: сторінка лежить у папці en/
html = html.replace('<html lang="uk">', '<html lang="en">')
html = html.replace('href="css/', 'href="../css/').replace('src="js/', 'src="../js/')
# Фото й відео лежать у корені сайту, а сторінка — у папці en/
for attr in ("src", "poster"):
    html = html.replace(f'{attr}="./images/', f'{attr}="../images/').replace(f'{attr}="images/', f'{attr}="../images/')
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
