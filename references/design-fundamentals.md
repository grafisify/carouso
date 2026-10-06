# Fundamental Desain Grafis untuk Carousel

Aturan main yang dipakai skill ini saat menyusun setiap slide. Ditulis sebagai
checklist keputusan, bukan teori.

## 1. Hierarki visual
Setiap slide punya SATU hal yang dilihat pertama. Urutan baca yang ditargetkan:
**judul → visual → body → kartu pendukung → footer.**
Caranya:
- Judul = elemen terbesar dan paling tebal di slide (display font, 84–132px pada
  kanvas 1080×1350; cover 1,3–1,5× lebih besar dari slide isi).
- Satu kata/frasa kunci dalam judul diberi warna aksen — jangan lebih dari itu.
- Body copy jauh lebih kecil (24–28px) dan lebih muda warnanya dari judul.

## 2. Kontras
- Teks di atas gambar/foto: wajib ada lapisan (scrim gradient atau kartu solid
  semi-transparan) — jangan pernah taruh teks langsung di atas foto yang ramai.
- Rasio kontras teks-body minimal terasa "jelas dibaca sekilas"; kalau ragu,
  gelapkan background atau terangkan teks.
- Warna aksen dipakai hemat: 1 warna aksen untuk sorotan kata kunci, garis aksen,
  dan CTA. Sisanya netral.

## 3. Alignment & grid
- Semua slide memakai margin dalam yang SAMA (contoh: 60–64px kiri/kanan).
- Elemen rata kiri sebagai default; cover boleh rata tengah sebagai pengecualian
  yang disengaja (judul cover rata tengah horizontal DAN vertikal).
- Jangan campur rata kiri dan rata tengah dalam satu slide isi.

## 4. Whitespace
- Jarak antar blok minimal 1× tinggi baris body. Slide yang sesak = konten
  dipangkas, bukan diperkecil fontnya sampai tak terbaca.
- Kartu pendukung selalu punya padding dalam (≥ 32px) dan radius sudut konsisten.

## 5. Tipografi
- Pasangan baku: 1 display font (judul, berkarakter — mis. handwritten/bold
  rounded untuk kesan playful) + 1 body font (bersih, sangat terbaca).
- Maksimal 2 family font per carousel. Jangan tambah font ketiga.
- Sumber font: Google Fonts (via `<link>` dengan `display=swap`) atau font lokal.
  Yang dilarang adalah font yang TIDAK termuat — render gate (`--check-fonts`)
  menolak hasil bila webfont gagal diunduh dan judul jatuh ke fallback.
- Ukuran minimum: body 24px, label kecil 14–15px HANYA untuk teks non-esensial
  (counter, footer). Semua yang harus dibaca ≥ 24px.

## 6. Warna (aturan 60-30-10)
- 60% warna dasar background, 30% warna sekunder (kartu/panel), 10% aksen.
- Background boleh berlapis (gradient + tekstur halus + vignette) asal tidak
  mengganggu keterbacaan — tekstur harus nyaris tak terlihat.
- Teks utama = warna tergelap dari palet; teks sekunder = versi dimudakannya.

## 7. Konsistensi & repetisi
Elemen yang muncul di SEMUA slide dan tidak boleh berubah gaya:
topbar (brand + penomoran `01 / 10`), footer (handle + CTA), eyebrow pill,
gaya kartu, radius sudut, dan shadow. Konsistensi inilah yang membuat 10 slide
terasa sebagai satu kesatuan, bukan 10 desain lepas.

## 8. Zona aman
- 64px dari tiap tepi = zona aman. Tidak ada teks penting di luar zona ini.
- Footer diposisikan absolut di bawah dengan jarak aman dari tepi bawah.

## 9. Prinsip anti-tabrakan
Layout memakai zona tetap (topbar / content / footer), bukan posisi absolut
bebas antar elemen konten. Konten mengalir vertikal dengan flex; overflow
tersembunyi dan terdeteksi otomatis saat render (lihat `scripts/render_carousel.py`).
Elemen yang "nempel" satu sama lain = desain gagal, perbaiki spacing-nya.
