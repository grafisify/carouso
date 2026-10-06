# Carouso — skill untuk AI agent

Skill ini membuat AI agent bisa memproduksi **carousel post siap publish**
(Instagram / TikTok / Facebook) dengan fundamental desain grafis yang benar,
plus **penempatan gambar dari upload user atau URL/artikel** — bukan dari
generative AI.

## Isi paket

```
carouso/
├── SKILL.md                      ← dibaca agent saat skill di-trigger
├── references/
│   ├── design-fundamentals.md    ← hierarki, kontras, tipografi, warna, zona aman
│   ├── layout-rules.md           ← anatomi slide, aturan cover/isi/penutup, budget teks
│   └── image-workflow.md         ← ingest upload/URL, verifikasi visual, crop & placement
├── assets/
│   └── base-template.html        ← template 10 slide + slot gambar, siap diisi
├── scripts/
│   └── render_carousel.py        ← render Playwright + quality gate (jumlah/overflow/dimensi)
└── examples/
    └── brief-example.md          ← contoh brief lengkap → output
```

## Cara pasang

Salin folder `carouso/` ke direktori skills AI agent kamu
(mis. `~/.claude/skills/`, `~/workspace/skills/`, atau folder skills milik
platform agent yang dipakai). Tidak ada dependensi khusus selain **Playwright +
Chromium** untuk render (lihat `scripts/render_carousel.py`).

## Prinsip kunci

1. Gambar **hanya** dari upload user atau URL/artikel — tidak ada gambar AI.
2. Setiap gambar **wajib diverifikasi visual** sebelum dipakai.
3. Render memakai **quality gate otomatis**: jumlah slide, overflow, dan dimensi
   yang salah = render ditolak, bukan diloloskan manual.
4. Font boleh Google Fonts atau lokal — tapi **wajib termuat**: render gate
   `--check-fonts` menolak hasil bila webfont gagal diunduh (mencegah judul
   jatuh ke font fallback).
5. Teks minimal (~80% visual), satu slide satu ide, cover selalu paling hookable.

## Kebutuhan render

- Python 3 + `playwright` (`pip install playwright && playwright install chromium`)
- Font display & body terinstal di sistem (cek: `fc-list | grep -i "<nama-font>"`)
