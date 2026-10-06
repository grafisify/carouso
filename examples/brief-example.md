# Contoh Brief → Cara Skill Bekerja

## Input brief (dari user)

> Topik: "5 Kesalahan Bikin Kopi Tubruk di Rumah"
> Slide: 10, ukuran 1080×1350
> Brand: Kopi Pagi (@kopipagi), warna: coklat tua #3a2a1e + krem #f5ead9,
> aksen oranye #d97b2b, font display: Baloo 2, font body: Quicksand
> Gambar:
> - Upload: `foto-seduh.jpg` → slide 2, peran hero (proses seduh)
> - URL artikel: https://contoh.id/artikel/grind-size → ambil foto grind
>   size → slide 4, peran ilustrasi

## Yang dilakukan agent (memakai skill)

1. **Brief lengkap?** Ya — topik, jumlah, ukuran, brand, dan peta gambar
   (sumber + slide + peran) semuanya eksplisit. Lanjut.
2. **Konten**: tulis 10 slide — cover hook "Kopi Tubrukmu Pahit Terus?",
   8 slide isi @ 1 kesalahan ("Air Terlalu Mendidih", "Grind Terlalu Halus", …),
   penutup 4 poin + CTA Simpan/Share.
3. **Ingest gambar**:
   - `foto-seduh.jpg` → salin ke `images/slide02_hero_seduh.jpg`
   - Buka URL artikel → pilih foto grind size yang relevan (bukan logo situs)
     → `curl -sL -o images/slide04_ilustrasi_grind.jpg <url>` → catat page_url
4. **Verifikasi visual**: lihat kedua gambar. Keduanya cocok topik, tanpa
   watermark, sisi terpendek > 900px → LOLOS. (Jika gagal → tolak & ganti
   dengan kartu grafis.)
5. **Bangun HTML**: salin `assets/base-template.html`, ubah token `:root`
   (warna/brand/handle/font), isi 10 slide, pasang `<img>` ke file lokal.
6. **Render**: `python3 scripts/render_carousel.py --html kopi-tubruk.html
   --out out/ --width 1080 --height 1350 --slides 10` → semua gate lolos.
7. **Verifikasi akhir**: cek slide 1, 5, 10 — font Baloo 2 ter-render,
   tidak ada overflow, gambar tidak stretch.
8. **Output**: `out/slide_01.jpg … slide_10.jpg` + `kopi-tubruk.html` +
   `images/` + `provenance.log`.

## Yang TIDAK dilakukan agent

- Tidak men-generate gambar AI untuk slide 2/4 (atau slide mana pun).
- Tidak hotlink URL gambar saat render.
- Tidak meloloskan render yang gagal quality gate.
