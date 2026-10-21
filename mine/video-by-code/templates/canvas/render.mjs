// Рендер ролика из index.html: браузер без окна рисует кадр за кадром, ffmpeg собирает видео.
//
//   node render.mjs --sheet          лист-превью: первый кадр + середина каждой сцены (sheet.png)
//   node render.mjs                  весь ролик -> out.mp4 (видео + синтезированная музыка)
//   node render.mjs --out x.mp4 --fps 30 --no-audio
//
// Нужны: Node 18+, ffmpeg в PATH, пакет playwright и его Chromium
// (npm i playwright && npx playwright install chromium).

import { spawn, execSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { writeFileSync, rmSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const arg = (name, def) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : def; };
const has = (name) => process.argv.includes(name);
const OUT = path.resolve(arg('--out', path.join(HERE, 'out.mp4')));

async function loadPlaywright() {
  try { return await import('playwright'); } catch {}
  // поставлен глобально (npm i -g playwright) — достаём из глобальной папки
  const root = execSync('npm root -g').toString().trim();
  return createRequire(path.join(root, 'noop.js'))('playwright');
}

function ffmpeg(args, label) {
  const p = spawn('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', ...args], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((ok, fail) => p.on('close', (c) => c === 0 ? ok() : fail(new Error(`ffmpeg (${label}) вышел с кодом ${c}`))));
  return { stdin: p.stdin, done };
}

const write = (stream, buf) => new Promise((ok) => stream.write(buf) ? ok() : stream.once('drain', ok));

const { chromium } = await loadPlaywright();
const browser = await chromium.launch();
const page = await browser.newPage();
page.on('pageerror', (e) => console.error('Ошибка на странице:', e.message));
await page.goto(pathToFileURL(path.join(HERE, 'index.html')).href);
await page.waitForFunction(() => window.renderFrame && window.TIMELINE);
await page.evaluate(() => window.fontsReady);
const fontsOk = await page.evaluate(() => document.fonts.check('800 64px "Inter"'));
if (!fontsOk) console.warn('⚠️ Шрифт Inter не загрузился (нет интернета?) — кадры будут системным шрифтом.');

const TL = await page.evaluate(() => window.TIMELINE);
const fps = Number(arg('--fps', TL.fps));

// Кадр(ы) из браузера: canvas -> PNG -> байты. Пачкой, чтобы не гонять мост на каждый кадр.
async function frames(times) {
  const b64 = await page.evaluate((ts) => ts.map((t) => {
    window.renderFrame(t);
    return document.getElementById('c').toDataURL('image/png').split(',')[1];
  }), times);
  return b64.map((s) => Buffer.from(s, 'base64'));
}

if (has('--sheet')) {
  // Превью до долгого рендера: первый кадр (это обложка в ленте) и середина каждой сцены.
  const starts = [0, ...TL.cuts], ends = [...TL.cuts, TL.duration];
  const times = [0, ...starts.map((s, i) => s + (ends[i] - s) * 0.6)];
  const out = path.join(HERE, 'sheet.png');
  const ff = ffmpeg(['-f', 'image2pipe', '-c:v', 'png', '-i', '-', '-vf', `scale=270:-1,tile=${times.length}x1:padding=8:color=white`, '-frames:v', '1', out], 'лист');
  for (const f of await frames(times)) await write(ff.stdin, f);
  ff.stdin.end(); await ff.done;
  console.log(`Лист превью: ${out} (${times.length} кадров: ${times.map((t) => t.toFixed(1) + 'с').join(', ')})`);
} else {
  const total = Math.round(TL.duration * fps);
  let audio = null;
  if (!has('--no-audio')) {
    audio = path.join(HERE, '_audio.wav');
    writeFileSync(audio, Buffer.from(await page.evaluate(() => window.renderAudioWav()), 'base64'));
  }
  const args = ['-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-'];
  if (audio) args.push('-i', audio);
  args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p');
  // Громкость под соцсети: −14 LUFS, пики не выше −1.5 дБ (иначе ролик тише соседних в ленте).
  if (audio) args.push('-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000',
                       '-c:a', 'aac', '-b:a', '192k', '-shortest');
  args.push('-movflags', '+faststart', OUT);
  const ff = ffmpeg(args, 'ролик');
  const BATCH = 8, t0 = Date.now();
  for (let i = 0; i < total; i += BATCH) {
    const ts = []; for (let j = i; j < Math.min(i + BATCH, total); j++) ts.push(j / fps);
    for (const f of await frames(ts)) await write(ff.stdin, f);
    if (i % (BATCH * 30) === 0) process.stdout.write(`\rкадр ${i}/${total}`);
  }
  ff.stdin.end(); await ff.done;
  if (audio) rmSync(audio, { force: true });
  console.log(`\rГотово: ${OUT} — ${total} кадров, ${TL.duration.toFixed(1)} с, за ${((Date.now() - t0) / 1000).toFixed(0)} с`);
}
await browser.close();
