# Alur Kerja Gambar: Upload User & URL/Artikel

> Prinsip: gambar di skill ini HANYA berasal dari dua sumber — file yang
> diupload user, atau gambar yang diambil dari URL/artikel. **Dilarang memakai
> gambar hasil generative AI dalam bentuk apa pun.**

## 1. Ingest (kumpulkan ke lokal)

### Dari file upload user
- Baca file dari path yang diberikan user. Catat nama file asli di `provenance.log`.
- Format yang didukung: JPG, PNG, WebP. Selain itu, konversi dulu ke JPG/PNG.

### Dari URL langsung (gambar)
- Download dengan `curl` (bukan urllib bila lewat proxy — urllib sering gagal
  di tengah jalan untuk body besar):
  ```
  curl -sL -m 60 -o images/slide03_hero.jpg "<url-gambar>"
  ```
- Verifikasi hasil download: buka file-nya dan pastikan itu gambar valid
  (bukan halaman HTML error / 1KB redirect).

### Dari URL artikel
1. Buka artikelnya, identifikasi gambar yang RELEVAN dengan topik slide
   (foto isi, bukan logo situs, bukan banner iklan, bukan avatar penulis).
2. Prioritaskan foto yang terlihat natural/autentik dibanding foto studio
   yang terlalu dipoles — kecuali brief meminta kesan premium.
3. Download gambarnya ke lokal seperti URL langsung.
4. Catat `page_url` artikel sebagai provenance. Jika artikel mencantumkan
   kredit fotografer/sumber, cantumkan kredit kecil di caption gambar.

### Aturan umum ingest
- SEMUA gambar disalin ke folder lokal `images/` sebelum render. Render tidak
  boleh hotlink ke URL eksternal (hasil tidak deterministik, bisa gagal offline).
- Beri nama file yang jelas: `slide<NN>_<peran>_<deskripsi-singkat>.jpg`
  (contoh: `slide03_hero_bawang-merah.jpg`).

## 2. Verifikasi visual (HARD GATE — tidak boleh dilewati)

Sebelum gambar dipakai di slide mana pun, LIHAT gambarnya dan jawab checklist:
- [ ] Isinya cocok dengan topik slide yang diminta? (foto bawang untuk slide
      tentang bawang — bukan foto generik yang "mirip-mirip")
- [ ] Tidak ada watermark, logo, atau teks asing di dalam foto?
- [ ] Tidak buram/pecah? Sisi terpendek ≥ 900px untuk pemakaian besar (hero /
      full-bleed), ≥ 500px untuk ilustrasi kecil.
- [ ] Komposisi memungkinkan crop aman? (objek utama tidak menempel ke tepi)

**Satu saja jawaban "tidak" → gambar DITOLAK.** Pilihannya:
(a) minta gambar lain ke user, (b) cari alternatif dari URL/artikel lain, atau
(c) ganti slot gambar dengan elemen grafis (ikon, kartu warna, pola).
Jangan pernah memaksa memakai gambar yang gagal verifikasi.

## 3. Penempatan & crop

- Gambar dipasang di dalam `.img-frame` (rasio bingkai tetap) dengan
  `object-fit: cover; object-position: center;` — tidak pernah di-stretch.
- Kalau objek utama bukan di tengah (mis. wajah di kiri), ubah
  `object-position` (mis. `20% 50%`) agar objek tidak kepotong.
- Full-bleed: tambahkan scrim gradient (gelap di area teks) — teks di atas foto
  tanpa scrim = gagal keterbacaan.
- Satu slide = satu gambar dominan. Pengecualian hanya untuk kolase yang
  memang diminta brief, dengan bingkai seragam.

## 4. Larangan

1. Tidak men-generate gambar dengan AI untuk alasan apa pun.
2. Tidak memakai gambar yang belum dilihat/diverifikasi secara visual.
3. Tidak hotlink gambar eksternal saat render.
4. Tidak memakai gambar yang jelas-jelas berlisensi restrictif/berbayar
   (tanda watermark adalah sinyal paling jelas) — pilih sumber bebas lisensi
   atau foto milik user sendiri.
