Nama : Nur Azizah
NPM : 2506547935
Kelas : PBP A

# Portofolio Pribadi - Tugas 1

## Deskripsi Proyek
Tujuan dan Cakupan Utama: Website ini merupakan portofolio pribadi "About Me" yang dibangun menggunakan HTML5 dan CSS3 murni tanpa basis data atau arsitektur MVT, sesuai dengan cakupan materi Tutorial 1.
1. Fitur Section Profile: Menyediakan informasi identitas diri, latar belakang/bio, serta akses cepat ke media sosial dan kontak pribadi.
2. Fitur Section Education: Menyusun riwayat pendidikan lengkap dengan jurusan serta alamat sekolah pada tiap jenjang studi.
3. Fitur Section Skills: Menampilkan peta keahlian teknis maupun non-teknis secara visual bar agar tingkat kemahiran dapat dibaca dengan mudah.
4. Fitur Section Experience: Terdapat informasi sedang mengemban amanah apa saja dan lengkap dengan deskripsi tugasnya.
5. Fitur Section Achievements: Menampilkan prestasi baik akademik maupun non akademik yang telah dicapai serta terdapat foto setiap sertifikat penghargaan yang didapatkan.
6. Fitur Section Certifications: Menampilkan keahlian apa saja yang pernah dicapai dan disediakan juga masa berlaku serta foto sertifikat.

## Tech Stack
- Django: Berfungsi sebagai backend server untuk menyajikan berkas halaman statis dan mengelola rute alur halaman.
- HTML5: Mengatur hirarki dan struktur dokumen menggunakan elemen semantik (<header>, <nav>, <main>, <section>, <footer>).
- CSS3 Murni: Mengelola tata letak dan estetika visual secara responsif menggunakan CSS Grid, Flexbox, Custom Properties, serta Media Queries.

## Cara Menjalankan Proyek
1. Clone repository ini
git clone https://github.com/nurazizah56-dak/myportofolio
cd myportofolio

2. Aktifkan virtual environment
.\env\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Jalankan server
python manage.py runserver

5. Buka browser ke `http://127.0.0.1:8000/`

## Pertanyaan Reflektif

### Tugas 1
1. Saya menerapkan elemen semantik HTML5 untuk membangun struktur dokumen yang jelas secara hirarki, baik bagi pengembang lain, mesin pencari (SEO), maupun perangkat aksesibilitas seperti screen reader. Setiap kelompok informasi utama (Education, Skills, Experience, Achievements, Certifications) dibungkus ke dalam elemen `<section>` tersendiri dengan atribut `id` unik. Atribut ini dimanfaatkan sebagai anchor link pada `<nav>` di dalam `<header>`, lengkap dengan `scroll-behavior: smooth` agar perpindahan antar bagian terasa halus. Saya memutuskan tidak menggunakan `<article>` karena informasi di dalam setiap section (seperti riwayat pendidikan atau skill) bukan berupa konten independen yang dapat berdiri sendiri atau didistribusikan ulang secara mandiri seperti artikel blog, melainkan bagian dari satu kesatuan profil portofolio. Setiap elemen gambar dan ikon dilengkapi atribut `alt` yang informatif untuk mendukung aksesibilitas. Pada iterasi awal, saya sempat keliru membuat elemen `<nav>` terpisah untuk setiap tautan (sehingga terdapat 6 elemen `<nav>`). Setelah dievaluasi, struktur tersebut tidak efisien dan menyalahi prinsip semantik, sehingga saya merapikannya menjadi satu elemen `<nav>` tunggal yang membungkus seluruh daftar tautan navigasi.

2. Tantangan terbesar muncul pada section Education dan Skills yang mengelola data cukup padat (5 riwayat pendidikan dan 10 skills). Di layar desktop, Education ditata menggunakan CSS Grid 3 kolom, sementara Skills menggunakan Flexbox untuk menampilkan bar chart horizontal. Saat diuji pada layar ponsel via Chrome DevTools, layout 3 kolom tersebut mengalami overflow sehingga teks terpotong dan tampilan menjadi terlalu padat. Solusinya, saya menerapkan media query `@media (max-width: 700px)` untuk mengubah Grid Education menjadi 1 kolom penuh, serta menyesuaikan lebar bar chart dan ukuran font pada Skills agar tetap muat dalam satu baris tanpa wrap. Keterbatasan teknis lain yang sempat menghambat adalah kesalahan penutupan tag HTML, salah satunya ketidaksengajaan menutup `<div class="education-grid">` sebelum seluruh elemen di dalamnya selesai ditulis, sehingga aturan CSS Grid tidak terintegrasi dengan benar. Pengalaman ini menekankan pentingnya disiplin memeriksa kerapian tag bersarang (nested HTML) sebelum mendiagnosis kesalahan pada CSS.

3. Karena berbasis static web, seluruh informasi bersifat hardcoded di dalam file HTML. Hal ini membatasi skala pemeliharaan (maintainability): setiap kali ada pembaruan data (misalnya menambah pengalaman atau memperbarui skor skill), berkas HTML harus diubah dan di-deploy ulang secara manual. Selain itu, halaman statis belum mampu menyediakan fitur interaktif kompleks seperti pemfilteran atau pencarian prestasi berdasarkan kategori. Ke depannya, saya berencana menghubungkan situs ini dengan backend berbasis Django, di mana data seperti Education, Experience, dan Achievements akan disimpan ke dalam database relasional sebagai model terpisah, sehingga pembaruan konten dapat dilakukan secara dinamis melalui Django Admin Panel tanpa perlu mengubah kode HTML. Saya juga berencana mengganti fungsi tautan `mailto:` yang ada saat ini dengan contact form dinamis yang terhubung ke backend agar pesan dari pengunjung dapat terkirim dan tersimpan secara real-time.

## AI Disclosure
Tools yang digunakan: Gemini (Google)

### Peran AI dalam Pengembangan:
AI digunakan sebagai thinking partner, reviewer, dan konsultan selama proses pengembangan website, bukan sebagai pengganti keseluruhan proses coding. Penggunaan AI mencakup beberapa tahap berikut:
1. Evaluasi Visual & UI/UX — Mengunggah screenshot hasil render lokal untuk mendapatkan masukan mengenai kontras warna, keterbacaan skill bar, keseimbangan accent color, serta konsistensi tampilan.
2. Responsive Design Review — Menggunakan AI sebagai second opinion untuk mengidentifikasi kemungkinan masalah layout pada ukuran layar yang berbeda. Solusi yang diberikan kemudian diuji secara langsung menggunakan browser dan Chrome DevTools.
3. HTML & CSS Review — Meminta AI untuk membantu meninjau struktur semantic HTML5, penggunaan elemen seperti `<header>`, `<nav>`, `<main>`, `<section>`, dan `<footer>`, serta kemungkinan masalah pada struktur nested HTML dan CSS.
4. Debugging & Problem Solving — Menggunakan AI untuk membantu menganalisis kemungkinan penyebab masalah ketika hasil rendering tidak sesuai dengan ekspektasi. Output AI digunakan sebagai hipotesis awal, kemudian diverifikasi secara manual melalui code editor, browser, dan proses debugging.
5. Git & Version Control — Meminta rekomendasi penulisan pesan commit agar perubahan seperti pembaruan styling dan section dapat terdokumentasi secara konsisten.
6. Penyusunan Refleksi — Menggunakan AI untuk membantu mengorganisasi dan memperjelas penyampaian refleksi teknis mengenai semantic HTML, responsive CSS, debugging, serta rencana pengembangan website.

#### Bagian yang Dibantu AI:
1. Evaluasi visual dan kontras warna berdasarkan screenshot.
2. Rekomendasi accent color (--accent) untuk komponen skill bar.
3. Review struktur HTML dan CSS.
4. Analisis kemungkinan masalah responsive layout dan debugging.
5. Rekomendasi pesan commit.
6. Pengorganisasian dan penyuntingan laporan refleksi.

#### Bagian yang Dikerjakan Manual:
1. Penulisan struktur awal HTML5 dan CSS.
2. Implementasi langsung kode pada code editor.
3. Penentuan dan pengisian konten aktual portofolio.
4. Penerapan perubahan warna dan styling.
5. Eksekusi seluruh perintah Git (git add, git commit, git push).
6. Pengujian dan verifikasi website melalui browser lokal.
7. Pengujian responsive layout menggunakan Chrome DevTools.
8. Pengambilan keputusan akhir terhadap saran yang diberikan AI.

### Refleksi Kritis terhadap Penggunaan AI:
AI tidak selalu menghasilkan solusi yang sesuai dengan kondisi proyek. Beberapa saran dapat bersifat terlalu umum atau tidak mempertimbangkan struktur kode yang sedang digunakan, sehingga setiap rekomendasi AI perlu diperiksa kembali sebelum diterapkan. Dalam proses pengembangan, saya menggunakan output AI sebagai masukan dan hipotesis untuk membantu problem solving, bukan sebagai sumber kebenaran tunggal — solusi akhir ditentukan berdasarkan hasil pengujian langsung pada kode, browser, dan kebutuhan desain website. Penggunaan AI membantu mempercepat proses eksplorasi alternatif dan evaluasi masalah, tetapi pemahaman terhadap struktur HTML, CSS, serta alasan di balik setiap perubahan tetap menjadi tanggung jawab saya sebagai pengembang.