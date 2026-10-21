// Ролик, нарисованный кодом. Каждый кадр — вызов renderFrame(t), где t — секунды от начала.
//
// Главное правило: кадр зависит ТОЛЬКО от t. Никаких Date.now(), Math.random(), таймеров и
// анимаций CSS. Тогда рендер покадрово даёт ровно то, что видно в окне, и любую сцену можно
// перерисовать отдельно. Случайность нужна — берите seeded(…) ниже.
//
// Чтобы сделать свой ролик, меняйте СЦЕНЫ (массив SCENES внизу) и цвета C. Остальное — общие
// рисовалки, их обычно трогать не нужно.

const W = 1080, H = 1920, FPS = 30;
const SAFE = 90;   // поля: в Reels/Shorts верх и низ закрыты интерфейсом, текст туда не ставим

const C = {
  bg: '#07080d', panel: '#11131c', line: 'rgba(255,255,255,0.10)',
  text: '#f4f5f8', muted: '#8b90a5', a: '#8b7cff', b: '#3dd6f5', ok: '#3ee08f',
};

const cv = document.getElementById('c');
const g = cv.getContext('2d');

// Шрифты для холста надо загрузить явно: сам браузер качает шрифт, только когда им пишут
// обычный текст на странице, а рисование на canvas не в счёт. Без этого кадры выйдут
// системным шрифтом. Поменяли шрифт или вес — допишите сюда.
const FONTS = ['400 40px "Inter"', '600 40px "Inter"', '800 40px "Inter"', '500 40px "JetBrains Mono"'];
window.fontsReady = Promise.all(FONTS.map((f) => document.fonts.load(f)));

// ---------- время и плавность ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const easeOut = (k) => 1 - Math.pow(1 - clamp(k), 3);              // быстро начал, мягко встал
const easeInOut = (k) => { k = clamp(k); return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
// appear(t, start, dur) — от 0 до 1: «насколько появился» элемент к моменту t
const appear = (t, start, dur = 0.6) => easeOut((t - start) / dur);
const lerp = (a, b, k) => a + (b - a) * k;
function seeded(seed) {             // повторяемая «случайность»: одинаковая на каждом рендере
  return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
}

// ---------- рисовалки ----------
const font = (weight, size, family = 'Inter') => `${weight} ${size}px "${family}", sans-serif`;

function text(str, x, y, f, color, align = 'left', alpha = 1) {
  g.save(); g.globalAlpha *= alpha; g.font = f; g.fillStyle = color;
  g.textAlign = align; g.textBaseline = 'alphabetic'; g.fillText(str, x, y); g.restore();
}

// Перенос по ширине. Возвращает строки — их удобно проявлять по одной.
function wrap(str, f, maxW) {
  g.save(); g.font = f;
  const out = []; let line = '';
  for (const word of str.split(' ')) {
    const test = line ? line + ' ' + word : word;
    if (g.measureText(test).width > maxW && line) { out.push(line); line = word; } else line = test;
  }
  if (line) out.push(line);
  g.restore(); return out;
}

function card(x, y, w, h, r = 36, fill = C.panel) {
  g.save(); g.beginPath(); g.roundRect(x, y, w, h, r);
  g.fillStyle = fill; g.fill(); g.strokeStyle = C.line; g.lineWidth = 2; g.stroke(); g.restore();
}

function gradient(x0, y0, x1, y1) {
  const q = g.createLinearGradient(x0, y0, x1, y1);
  q.addColorStop(0, C.a); q.addColorStop(1, C.b); return q;
}

function background(t) {
  g.fillStyle = C.bg; g.fillRect(0, 0, W, H);
  // мягкое свечение, медленно плывёт — фон «живой», но не отвлекает
  const x = W / 2 + Math.sin(t * 0.4) * 160, y = H * 0.35 + Math.cos(t * 0.3) * 120;
  const q = g.createRadialGradient(x, y, 0, x, y, 900);
  q.addColorStop(0, 'rgba(139,124,255,0.22)'); q.addColorStop(1, 'rgba(139,124,255,0)');
  g.fillStyle = q; g.fillRect(0, 0, W, H);
}

// Строка, которая «печатается» сама: к моменту t видно столько букв, сколько успело.
// last — это последняя строка: после неё курсор остаётся мигать. У остальных строк курсор
// виден, только пока строка печатается.
function typing(str, x, y, f, color, t, start, cps = 22, last = true) {
  if (t < start) return;
  const n = Math.floor(clamp((t - start) * cps, 0, str.length));
  text(str.slice(0, n), x, y, f, color);
  const active = n < str.length;
  if (active || (last && Math.floor(t * 2) % 2 === 0)) {     // курсор
    g.save(); g.font = f; const w = g.measureText(str.slice(0, n)).width; g.restore();
    g.fillStyle = C.b; g.fillRect(x + w + 6, y - 44, 4, 54);
  }
}

// Полоска прогресса сверху: «шаг 2 из 3».
function progress(i, n, k) {
  const w = (W - 2 * SAFE) / n;
  for (let j = 0; j < n; j++) {
    g.fillStyle = j < i ? C.a : (j === i ? gradient(SAFE, 0, W - SAFE, 0) : 'rgba(255,255,255,0.12)');
    const fillW = j === i ? (w - 12) * k : w - 12;
    g.fillRect(SAFE + j * w, SAFE + 40, j === i ? fillW : w - 12, 8);
  }
}

// ---------- сцены ----------
// Сцена = длительность + функция рисования. t внутри сцены считается от её начала (0..dur).
const STEPS = [
  { title: 'Папка проекта', say: 'Прочитай CLAUDE.md и скажи, что понял' },
  { title: 'Одна скучная задача', say: 'Каждое утро собирай мне сводку почты' },
];

const SCENES = [
  { dur: 3.5, draw(t) {                                          // обложка
      // Начало появления — ДО нуля: первый кадр уже с заголовком (он станет обложкой),
      // а движение всё равно видно — буквы досаживаются на место.
      background(t);
      const k = appear(t, -0.6, 1.2);
      text('ПЕРВЫЙ', W / 2, 820 - 40 * (1 - k), font(800, 120), C.text, 'center', k);
      g.save(); g.globalAlpha = appear(t, -0.4, 1.2);
      text('AI-АГЕНТ', W / 2, 960, font(800, 120), gradient(250, 0, 830, 0), 'center');
      g.restore();
      text('за 2 шага', W / 2, 1080, font(400, 54), C.muted, 'center', appear(t, 0.6));
  } },
  ...STEPS.map((s, i) => ({ dur: 5, draw(t) {                   // шаг
      background(t + i * 5);
      progress(i, STEPS.length, clamp(t / 5));
      text(String(i + 1).padStart(2, '0'), SAFE, 400, font(800, 64, 'JetBrains Mono'), C.a, 'left', appear(t, 0));
      wrap(s.title, font(800, 92), W - 2 * SAFE).forEach((ln, j) =>
        text(ln, SAFE, 520 + j * 104 + 30 * (1 - appear(t, 0.15 + j * 0.1)), font(800, 92), C.text, 'left', appear(t, 0.15 + j * 0.1)));
      const ky = appear(t, 1.0, 0.7);                              // карточка «скажи агенту» выезжает снизу
      const y = lerp(1500, 1180, ky);
      g.save(); g.globalAlpha = ky; card(SAFE, y, W - 2 * SAFE, 300); g.restore();
      text('СКАЖИ АГЕНТУ', SAFE + 50, y + 80, font(600, 34), C.muted, 'left', ky);
      const lines = wrap(s.say, font(500, 46, 'JetBrains Mono'), W - 2 * SAFE - 100);
      let start = 1.6;
      lines.forEach((ln, j) => {
        typing(ln, SAFE + 50, y + 170 + j * 64, font(500, 46, 'JetBrains Mono'), C.text, t, start, 22, j === lines.length - 1);
        start += ln.length / 22;
      });
  } })),
  { dur: 3.5, draw(t) {                                          // финал
      background(t + 20);
      text('Сохрани', W / 2, 860, font(800, 110), C.text, 'center', appear(t, 0.1));
      STEPS.forEach((s, i) => text('✓  ' + s.title, W / 2, 1010 + i * 80, font(600, 52), C.ok, 'center', appear(t, 0.5 + i * 0.25)));
  } },
];

// ---------- сборка таймлайна (не трогать) ----------
const STARTS = []; let acc = 0;
for (const s of SCENES) { STARTS.push(acc); acc += s.dur; }
window.TIMELINE = { duration: acc, fps: FPS, width: W, height: H, cuts: STARTS.slice(1) };

window.renderFrame = function (t) {
  let i = SCENES.length - 1;
  while (i > 0 && t < STARTS[i]) i--;
  const local = t - STARTS[i];
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1;
  SCENES[i].draw(local);
  // короткая смена сцен: затемнение 0.15 с на стыках. Самый первый кадр не затемняем:
  // по нему соцсети делают обложку, чёрная обложка — потерянный просмотр.
  const tail = SCENES[i].dur - local;
  const edge = i === 0 ? tail : (i === SCENES.length - 1 ? local : Math.min(local, tail));
  if (edge < 0.15) { g.fillStyle = `rgba(7,8,13,${1 - edge / 0.15})`; g.fillRect(0, 0, W, H); }
};
