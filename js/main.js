/* =========================================================
   MAIN.JS — уся інтерактивність сайту
   ---------------------------------------------------------
   1. Шапка: світлий фон після прокрутки
   2. Мобільне меню: відкрити / закрити
   3. Поточний рік у футері
   4. Перемикач теми: світла / темна
   5. Анімації появи при прокрутці (.reveal)
   6. Панель бронювання в hero
   7. Номери й відгуки: гортання стрілками й перетягуванням
   8. Відпочинок: перемикання фото
   9. Паралакс фото (data-parallax)
   10. Відео-«гіфки»: пауза, якщо вимкнені анімації
   ========================================================= */

// Позначка, що JS працює — тоді CSS ховає .reveal до появи
document.documentElement.classList.add("js");

// Чи просив користувач менше анімацій (налаштування системи)
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

document.addEventListener("DOMContentLoaded", () => {

  /* ---------- 1. ШАПКА ПІСЛЯ ПРОКРУТКИ ---------- */
  const header = document.getElementById("header");

  const updateHeader = () => {
    // Після 40px прокрутки додаємо клас .is-scrolled (див. css/header.css)
    header.classList.toggle("is-scrolled", window.scrollY > 40);
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });


  /* ---------- 2. МОБІЛЬНЕ МЕНЮ ---------- */
  const menu = document.getElementById("menu");
  const openBtn = document.querySelector(".menu-toggle");
  const closeBtn = document.querySelector(".menu__close");

  const openMenu = () => {
    menu.classList.add("is-open");
    menu.setAttribute("aria-hidden", "false");
    openBtn.setAttribute("aria-expanded", "true");
    document.body.classList.add("is-locked"); // блокуємо прокрутку сторінки
    closeBtn.focus();
  };

  const closeMenu = () => {
    menu.classList.remove("is-open");
    menu.setAttribute("aria-hidden", "true");
    openBtn.setAttribute("aria-expanded", "false");
    document.body.classList.remove("is-locked");
  };

  openBtn.addEventListener("click", openMenu);
  closeBtn.addEventListener("click", closeMenu);

  // Закриваємо меню після кліку на будь-яке посилання в ньому
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  // Закриваємо меню клавішею Esc
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.classList.contains("is-open")) {
      closeMenu();
      openBtn.focus();
    }
  });


  /* ---------- 3. РІК У ФУТЕРІ ---------- */
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();


  /* ---------- 4. ПЕРЕМИКАЧ ТЕМИ ----------
     Початкову тему ставить маленький скрипт у <head> index.html.
     Вибір користувача зберігається в localStorage ("theme"),
     тож при наступному візиті сайт відкриється в тій самій темі.
     Якщо користувач нічого не обирав — береться тема системи. */
  const root = document.documentElement;
  const themeBtn = document.querySelector(".theme-toggle");

  const isDark = () => root.getAttribute("data-theme") === "dark";

  // Оновлюємо підпис кнопки для екранних читачів
  const syncThemeButton = () => {
    themeBtn.setAttribute("aria-pressed", String(isDark()));
    // Підписи беруться з data-атрибутів кнопки — так вони
    // правильні й для української, і для англійської сторінки
    themeBtn.setAttribute(
      "aria-label",
      isDark() ? themeBtn.dataset.labelLight : themeBtn.dataset.labelDark
    );
  };

  const setTheme = (theme) => {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.removeAttribute("data-theme");
    }
    try { localStorage.setItem("theme", theme); } catch (e) { /* приватний режим */ }
    syncThemeButton();
  };

  if (themeBtn) {
    syncThemeButton();
    themeBtn.addEventListener("click", () => {
      setTheme(isDark() ? "light" : "dark");
    });
  }


  /* ---------- 5. АНІМАЦІЇ ПОЯВИ ----------
     Коли елемент з класом .reveal потрапляє в екран,
     йому додається .is-visible (стилі — components.css).
     Сусідні елементи з'являються з невеликою затримкою «драбинкою». */
  const revealItems = document.querySelectorAll(".reveal");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach((el) => el.classList.add("is-visible"));
  } else {
    // Затримка для елементів-сусідів: 0, 0.1, 0.2 с ...
    revealItems.forEach((el) => {
      const siblings = [...el.parentElement.children].filter((c) => c.classList.contains("reveal"));
      const index = siblings.indexOf(el);
      if (index > 0) el.style.setProperty("--delay", `${Math.min(index, 5) * 0.1}s`);
    });

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target); // анімуємо лише раз
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });

    revealItems.forEach((el) => revealObserver.observe(el));
  }


  /* ---------- 6. ПАНЕЛЬ БРОНЮВАННЯ ----------
     Не даємо обрати виїзд раніше заїзду. */
  const checkin = document.querySelector('.booking-bar input[name="checkin"]');
  const checkout = document.querySelector('.booking-bar input[name="checkout"]');

  if (checkin && checkout) {
    const today = new Date().toISOString().split("T")[0];
    checkin.min = today;
    checkout.min = today;
    checkin.addEventListener("change", () => {
      checkout.min = checkin.value || today;
      if (checkout.value && checkout.value < checkin.value) checkout.value = "";
    });
  }


  /* ---------- 7. СТРІЧКИ НОМЕРІВ І ВІДГУКІВ: СТРІЛКИ + ПЕРЕТЯГУВАННЯ ----------
     Одна функція для обох стрічок. name = "rooms" або "reviews":
     у HTML це атрибути data-<name>-track, data-<name>-prev, data-<name>-next. */
  const initTrack = (name, cardSelector) => {
    const track = document.querySelector(`[data-${name}-track]`);
    if (!track) return;

    // Крок гортання = ширина однієї картки + проміжок
    const step = () => {
      const card = track.querySelector(cardSelector);
      return card ? card.offsetWidth + parseFloat(getComputedStyle(track).gap || 0) : 400;
    };

    document.querySelector(`[data-${name}-prev]`)?.addEventListener("click", () => {
      track.scrollBy({ left: -step(), behavior: "smooth" });
    });
    document.querySelector(`[data-${name}-next]`)?.addEventListener("click", () => {
      track.scrollBy({ left: step(), behavior: "smooth" });
    });

    // Перетягування мишею (на телефоні працює звичайний свайп)
    let isDown = false;
    let startX = 0;
    let startScroll = 0;

    track.addEventListener("pointerdown", (e) => {
      if (e.pointerType !== "mouse") return;
      isDown = true;
      startX = e.clientX;
      startScroll = track.scrollLeft;
      track.classList.add("is-dragging");
    });

    window.addEventListener("pointermove", (e) => {
      if (!isDown) return;
      track.scrollLeft = startScroll - (e.clientX - startX);
    });

    window.addEventListener("pointerup", () => {
      if (!isDown) return;
      isDown = false;
      track.classList.remove("is-dragging");
    });
  };

  initTrack("rooms", ".room");
  initTrack("reviews", ".review");


  /* ---------- 8. ВІДПОЧИНОК: ПЕРЕМИКАННЯ ФОТО ----------
     Клік (або Enter) на пункт списку показує
     відповідне фото: data-exp="1" ↔ data-exp-image="1". */
  const expItems = document.querySelectorAll("[data-exp]");
  const expImages = document.querySelectorAll("[data-exp-image]");

  /* На телефоні (до 900px) блок з фото переїжджає ВСЕРЕДИНУ
     обраного пункту — фото з'являється одразу під його назвою.
     На комп'ютері фото повертається на своє місце поруч зі списком. */
  const expMedia = document.querySelector(".experiences__media");
  const expMediaHome = expMedia?.parentElement;    // де фото стоїть на комп'ютері
  const expMediaNext = expMedia?.nextElementSibling;
  const mobileQuery = window.matchMedia("(max-width: 900px)");

  const placeExpMedia = () => {
    if (!expMedia) return;
    const active = document.querySelector("[data-exp].is-active");

    if (mobileQuery.matches && active) {
      if (expMedia.parentElement === active) return;
      // Запам'ятовуємо положення пункту, щоб сторінка не «стрибнула»,
      // коли фото зникає з пункту вище
      const before = active.getBoundingClientRect().top;
      active.appendChild(expMedia);
      const after = active.getBoundingClientRect().top;
      // behavior "instant": інакше спрацьовує плавна прокрутка сайту
      // і пункт ще секунду «пливе» по екрану
      if (after !== before) window.scrollBy({ top: after - before, behavior: "instant" });
    } else if (!mobileQuery.matches && expMedia.parentElement !== expMediaHome) {
      expMediaHome.insertBefore(expMedia, expMediaNext);
    }
  };

  const showExperience = (id) => {
    expItems.forEach((item) => item.classList.toggle("is-active", item.dataset.exp === id));
    expImages.forEach((img) => img.classList.toggle("is-active", img.dataset.expImage === id));
    placeExpMedia();
  };

  placeExpMedia();
  mobileQuery.addEventListener("change", placeExpMedia);

  expItems.forEach((item) => {
    // Пункт перемикається лише по кліку (на комп'ютері й телефоні),
    // наведення миші нічого не змінює — так попросив власник.
    item.addEventListener("click", () => showExperience(item.dataset.exp));
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        showExperience(item.dataset.exp);
      }
    });
  });


  /* ---------- 10. ВІДЕО-«ГІФКИ» ----------
     Короткі відео (autoplay muted loop) грають як гіфки.
     Якщо в системі вимкнені анімації — ставимо їх на паузу. */
  if (reduceMotion) {
    document.querySelectorAll("video[autoplay]").forEach((v) => {
      v.removeAttribute("autoplay");
      v.pause();
    });
  }


  /* ---------- 9. ПАРАЛАКС ----------
     Фото з атрибутом data-parallax рухається повільніше
     за сторінку — виникає відчуття глибини. */
  const parallaxItems = document.querySelectorAll("[data-parallax]");

  if (parallaxItems.length && !reduceMotion) {
    let ticking = false;

    const updateParallax = () => {
      parallaxItems.forEach((img) => {
        const rect = img.parentElement.getBoundingClientRect();
        // -1 (блок унизу екрана) … 1 (блок угорі)
        const progress = (window.innerHeight / 2 - (rect.top + rect.height / 2)) / window.innerHeight;
        img.style.transform = `translateY(${progress * 10}%)`;
      });
      ticking = false;
    };

    window.addEventListener("scroll", () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }, { passive: true });

    updateParallax();
  }

});
