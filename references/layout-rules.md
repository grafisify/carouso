# Aturan Layout & Konten Carousel

## Anatomi slide (wajib sama di semua slide)
```
┌─────────────────────────────────┐
│ topbar: brand (kiri) │ 01 / 10  │  ← tinggi tetap, garis pemisah
├─────────────────────────────────┤
│ eyebrow pill (kategori slide)   │
│                                 │
│ JUDUL (display font, dominan)   │  ← zona content: flex vertikal,
│ subjudul/body (1–2 kalimat)     │     konten mengalir, tidak absolut
│ ┌─────────────────────────────┐ │
│ │ kartu pendukung             │ │  ← fakta / langkah / kutipan /
│ │ (ikon/gambar + teks pendek) │ │     gambar ilustrasi
│ └─────────────────────────────┘ │
├─────────────────────────────────┤
│ footer: @handle │ CTA            │  ← absolut bawah, zona aman
└─────────────────────────────────┘
```

## Aturan cover (slide 1)
- Judul cover rata tengah horizontal DAN vertikal (blok teks duduk di tengah
  slide, sekitar 53% tinggi) — bukan menempel ke atas.
- Ukuran judul 1,3–1,5× judul slide isi; boleh ada garis aksen di bawah judul
  (hanya di cover, sebagai pemanis).
- Struktur: eyebrow kategori → judul hook (3–7 kata) → 1 kalimat penjelas →
  1 kartu teaser. CTA footer berbentuk pill yang mengajak (mis. "Simpan ya").
- Cover TIDAK memuat isi/detail — tugasnya membuat orang swipe.

## Aturan slide isi (2..N-1)
- Satu slide = satu ide. Judul memakai label deskriptif, bukan nomor:
  "Dinginkan Bawang 15 Menit" — bukan "Tips 1".
- Kartu pendukung berisi SATU dari: fakta singkat, langkah konkret, kutipan
  pendek, atau gambar ilustrasi + caption 1 baris.
- Slide kutipan: teks pendek dan punchy, bukan paragraf.
- Slide rangkuman/takeaway: 4 poin, masing-masing 1 baris dengan label jelas.

## Aturan penutup (slide N)
- Rangkuman 3–4 poin + CTA eksplisit: Simpan / Share ke grup / Follow.
- CTA ditulis natural sesuai audiens, bukan template kaku.

## Budget teks per slide
| Elemen | Maksimal |
|---|---|
| Judul | 8 kata |
| Subjudul/body | 25 kata |
| Kartu pendukung | 30 kata |
| Total selain footer | ~60 kata |

Kalau konten brief melebihi budget: pangkas kalimatnya, JANGAN perkecil font
di bawah minimum dan JANGAN memadatkan spacing.

## Gambar di dalam layout
- Slot gambar punya bingkai berasio tetap (lihat `.img-frame` di template).
  Gambar mengisi bingkai dengan `object-fit: cover` — tidak pernah stretch.
- Peran yang didukung:
  - **hero**: gambar besar di kartu/area konten (rasio 4:3 atau 16:10).
  - **ilustrasi**: gambar kecil berdampingan dengan teks (rasio 1:1 / 4:3).
  - **full-bleed**: gambar memenuhi sebagian slide dengan scrim gradient
    agar teks di atasnya tetap terbaca.
- Objek utama foto jangan sampai kepotong bingkai — pilih crop yang aman
  (lihat panduan crop di `image-workflow.md`).
- Tiap slide yang memakai gambar: 1 gambar dominan saja. Dua foto besar dalam
  satu slide hampir selalu terlihat berantakan.
