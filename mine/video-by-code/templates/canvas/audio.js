// Музыка, написанная кодом: синтезатор браузера (Web Audio) играет её не в динамики, а в файл
// (OfflineAudioContext — «проиграй быстрее реального времени и отдай звук»). Сэмплов нет:
// аккорды — из пилообразных волн через фильтр, бочка — из синуса с падающей частотой,
// хэт и «шелест» на сменах сцен — из шума. Всё повторяемо: одинаковый код = одинаковый звук.
//
// Что менять: BPM, аккорды CHORDS, громкости в VOL. Шелест сам встаёт на стыки сцен
// (TIMELINE.cuts), поэтому смены кадров слышны в такт.

const BPM = 104;
const CHORDS = [   // MIDI-ноты; 60 = до первой октавы. Am9 – Fmaj7 – C(add9) – G6
  [57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 55, 60, 62, 64], [55, 59, 62, 64, 67]];
const BASS = [33, 29, 36, 31];
const VOL = { pad: 0.05, bass: 0.16, kick: 0.5, hat: 0.05, whoosh: 0.12, master: 0.8 };

async function buildAudio() {
  const SR = 44100, dur = window.TIMELINE.duration;
  const ac = new OfflineAudioContext(2, Math.ceil(SR * dur), SR);
  const beat = 60 / BPM;
  const hz = (m) => 440 * Math.pow(2, (m - 69) / 12);

  const master = ac.createGain(); master.gain.value = VOL.master;
  const comp = ac.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 3;
  master.connect(comp); comp.connect(ac.destination);

  // общий кусок шума (повторяемый)
  let s = 7; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647 * 2 - 1; };
  const noise = ac.createBuffer(1, SR * 2, SR); const nd = noise.getChannelData(0);
  for (let i = 0; i < nd.length; i++) nd[i] = rnd();

  // пэд: аккорд на такт, две чуть расстроенные пилы на ноту, мягкая атака и спад
  const padF = ac.createBiquadFilter(); padF.type = 'lowpass'; padF.frequency.value = 1300;
  const padG = ac.createGain(); padG.gain.value = VOL.pad; padF.connect(padG); padG.connect(master);
  const bar = 4 * beat;
  for (let b = 0; b * bar < dur; b++) {
    const t0 = b * bar, t1 = Math.min(t0 + bar + 0.3, dur);
    for (const m of CHORDS[b % 4]) for (const det of [-7, 7]) {
      const o = ac.createOscillator(); o.type = 'sawtooth'; o.frequency.value = hz(m); o.detune.value = det;
      const e = ac.createGain(); e.gain.setValueAtTime(0, t0);
      e.gain.linearRampToValueAtTime(1, t0 + 0.4); e.gain.setValueAtTime(1, t1 - 0.4);
      e.gain.linearRampToValueAtTime(0, t1);
      o.connect(e); e.connect(padF); o.start(t0); o.stop(t1);
    }
    const o = ac.createOscillator(); o.type = 'triangle'; o.frequency.value = hz(BASS[b % 4]);
    const e = ac.createGain(); e.gain.setValueAtTime(VOL.bass, t0); e.gain.exponentialRampToValueAtTime(0.001, t1);
    o.connect(e); e.connect(master); o.start(t0); o.stop(t1);
  }

  // ритм: бочка на каждую долю после вступления, хэт на слабые доли
  for (let i = 4; i * beat < dur - 0.3; i++) {
    const t = i * beat;
    const k = ac.createOscillator(); k.frequency.setValueAtTime(130, t); k.frequency.exponentialRampToValueAtTime(45, t + 0.12);
    const kg = ac.createGain(); kg.gain.setValueAtTime(VOL.kick, t); kg.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
    k.connect(kg); kg.connect(master); k.start(t); k.stop(t + 0.3);
    const h = ac.createBufferSource(); h.buffer = noise;
    const hf = ac.createBiquadFilter(); hf.type = 'highpass'; hf.frequency.value = 7000;
    const hg = ac.createGain(); const th = t + beat / 2;
    hg.gain.setValueAtTime(VOL.hat, th); hg.gain.exponentialRampToValueAtTime(0.001, th + 0.05);
    h.connect(hf); hf.connect(hg); hg.connect(master); h.start(th, rnd() * 0.5 + 0.5, 0.06);
  }

  // шелест на каждой смене сцен: шум через фильтр, частота которого «проезжает» вверх
  for (const cut of window.TIMELINE.cuts) {
    const t = Math.max(0, cut - 0.35);
    const w = ac.createBufferSource(); w.buffer = noise;
    const f = ac.createBiquadFilter(); f.type = 'bandpass'; f.Q.value = 1.2;
    f.frequency.setValueAtTime(400, t); f.frequency.exponentialRampToValueAtTime(5000, t + 0.45);
    const wg = ac.createGain(); wg.gain.setValueAtTime(0, t);
    wg.gain.linearRampToValueAtTime(VOL.whoosh, t + 0.3); wg.gain.linearRampToValueAtTime(0, t + 0.55);
    w.connect(f); f.connect(wg); wg.connect(master); w.start(t, 0.2, 0.6);
  }

  // мягкое затухание в конце
  master.gain.setValueAtTime(VOL.master, Math.max(0, dur - 1.2));
  master.gain.linearRampToValueAtTime(0, dur);
  return ac.startRendering();
}

// Отдать звук render.mjs: WAV (16 бит, стерео) строкой base64.
window.renderAudioWav = async function () {
  const buf = await buildAudio();
  const n = buf.length, ch = 2, out = new DataView(new ArrayBuffer(44 + n * ch * 2));
  const w = (o, str) => { for (let i = 0; i < str.length; i++) out.setUint8(o + i, str.charCodeAt(i)); };
  w(0, 'RIFF'); out.setUint32(4, 36 + n * ch * 2, true); w(8, 'WAVE'); w(12, 'fmt ');
  out.setUint32(16, 16, true); out.setUint16(20, 1, true); out.setUint16(22, ch, true);
  out.setUint32(24, buf.sampleRate, true); out.setUint32(28, buf.sampleRate * ch * 2, true);
  out.setUint16(32, ch * 2, true); out.setUint16(34, 16, true); w(36, 'data'); out.setUint32(40, n * ch * 2, true);
  const L = buf.getChannelData(0), R = buf.getChannelData(1);
  for (let i = 0, o = 44; i < n; i++) for (const c of [L, R]) {
    const v = Math.max(-1, Math.min(1, c[i])); out.setInt16(o, v < 0 ? v * 0x8000 : v * 0x7fff, true); o += 2;
  }
  const bytes = new Uint8Array(out.buffer); let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(bin);
};
