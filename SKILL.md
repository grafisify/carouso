---
name: "carouso"
description: "Carouso: buat carousel post (Instagram/TikTok/Facebook) dengan fundamental desain grafis — hierarki, tipografi, layout anti-tabrakan — dan penempatan gambar. Gambar HANYA dari upload user atau URL/artikel, bukan generative AI. Render deterministik ke JPG via Playwright dengan quality gate."
---

# Carouso

## Purpose
Mengubah sebuah brief topik menjadi carousel siap posting: konten per slide ditulis,
layout dirancang dengan fundamental desain grafis, gambar (upload user / URL)
ditempatkan di slide yang diminta, lalu di-render ke JPG dengan quality gate yang
menolak hasil cacat.

## Workflow

### 1. Kumpulkan brief
Wajib jelas sebelum mulai. Kalau ada yang kosong, tanya — jangan menebak:
- **Topik + angle** (1 kalimat hook)
- **Jumlah slide** (default 10) dan **ukuran** (default 1080×1350; alternatif 1080×1440)
- **Gaya/merek**: nama brand, handle, 2 warna utama + 1 warna aksen, font display + font body
  (kalau tidak disebut, pakai token default di `assets/base-template.html`)
- **Gambar**: untuk tiap gambar — sumbernya (path file upload ATAU url langsung ATAU url
  artikel) + slide ke berapa + peran (hero/full-bleed, ilustrasi kartu, thumbnail).
  Tanpa peta penempatan yang eksplisit, JANGAN memakai gambar.

### 2. Tulis konten per slide
Struktur baku:
- **Slide 1 (cover)**: hook 3–7 kata, 1 subjudul penjelas maks 2 baris, TANPA isi detail.
  Cover harus beda dan paling hookable dibanding slide lain.
- **Slide 2..N-1**: 1 ide per slide. Judul deskriptif (bukan "Tips 1", melainkan
  "Dinginkan Bawang 15 Menit"), 1–2 kalimat penjelasan, 1 kartu pendukung
  (fakta singkat / langkah / kutipan).
- **Slide N (penutup)**: rangkuman 3–4 poin + CTA (Simpan / Share / Follow).
- Budget teks: judul ≤ 8 kata, body ≤ 25 kata per slide. Prinsipnya ~80% visual,
  teks seminimal mungkin. Detail aturan konten ada di
  [references/layout-rules.md](references/layout-rules.md).

### 3. Ingest & verifikasi gambar (HARD GATE)
Ikuti persis [references/image-workflow.md](references/image-workflow.md):
1. Download/salin tiap gambar ke folder kerja lokal (JANGAN hotlink saat render).
2. **Lihat gambarnya secara visual** sebelum dipakai. Tolak bila: tidak cocok dengan
   topik slide, ada watermark/logo asing, buram, atau resolusi sisi terpendek < 900px
   untuk pemakaian besar.
3. Catat provenance (sumber URL / nama file upload) di log.
4. **DILARANG KERAS memakai gambar hasil generative AI.** Skill ini tidak men-generate
   gambar dalam bentuk apa pun.

### 4. Bangun HTML dari template
- Salin `assets/base-template.html` → file kerja. Jangan menulis layout dari nol
  kecuali brief meminta gaya yang template tidak dukung.
- Isi slot konten dan slot gambar (`<!-- IMG: ... -->`). Gambar direferensikan
  sebagai **path file lokal** relatif terhadap HTML.
- Terapkan fundamental desain di [references/design-fundamentals.md](references/design-fundamentals.md):
  hierarki (judul dominan), kontras, alignment konsisten, whitespace, dan zona aman.
- Font: boleh **Google Fonts** (uncomment blok `<link>` di template, selalu
  pakai `display=swap`) ATAU font yang terinstal lokal (cek `fc-list`). Render
  dengan flag `--check-fonts "Baloo 2,Quicksand"` agar webfont yang gagal
  dimuat menggagalkan render — jangan biarkan judul jatuh ke font fallback.
  Di lingkungan tanpa akses fonts.googleapis.com, install TTF font-nya lokal
  (nama family tetap sama).

### 5. Render dengan quality gate
Jalankan `scripts/render_carousel.py`:
```
python3 scripts/render_carousel.py --html <file.html> --out <dir-output> \
    --width 1080 --height 1350 --slides 10 \
    --check-fonts "Baloo 2,Quicksand"
```
Script ini otomatis menggagalkan (exit 1) bila:
- jumlah `.slide` ≠ jumlah yang diminta,
- ada konten yang overflow keluar zona (teks kepotong / elemen tabrakan),
- dimensi bounding box slide ≠ width×height yang diminta.
Perbaiki HTML dan render ulang sampai lolos. Jangan pernah "meloloskan manual".

### 6. Verifikasi visual akhir
Buka 3 file: slide 1 (cover), 1 slide tengah, slide terakhir. Cek:
- font display ter-render sesuai (bukan fallback serif),
- tidak ada teks kepotong atau elemen bertumpuk,
- gambar tampil benar (tidak stretch, objek utama tidak kepotong),
- brand/handle/CTA konsisten di semua slide.

## Output Contract
- `<dir-output>/slide_01.jpg … slide_NN.jpg` — tepat N file, dimensi sesuai brief.
- File HTML sumber yang dipakai render (simpan di samping output).
- `images/` berisi semua gambar yang dipakai (lokal), + `provenance.log`
  (gambar → sumber URL / nama file upload).

## Operating Rules
1. Gambar hanya dari upload user atau URL/artikel. Tidak ada gambar AI-generatif,
   tanpa pengecualian.
2. Setiap gambar dipakai HANYA setelah verifikasi visual. Gambar tak terverifikasi
   = tidak dipakai, dan slotnya diganti elemen grafis (ikon/kartu).
3. Render gagal di quality gate = perbaiki, bukan bypass.
4. Teks minimal; satu slide satu ide; cover selalu paling menonjol.
5. Konsistensi antar slide: topbar (brand + nomor), footer (handle + CTA),
   palet, dan pasangan font yang sama di seluruh carousel.
6. Jangan menebak brief yang kosong — tanya dulu.
