Nama : Nur Azizah
NPM : 2506547935
Kelas : PBP A

# Portofolio Pribadi 

## Deskripsi Proyek
Tujuan dan Cakupan Utama: Website ini merupakan portofolio pribadi "About Me" yang dibangun menggunakan Django dengan arsitektur Model-View-Template (MVT). Seluruh bagian utama meliputi Experience, Education, Skills, Achievements, dan Certifications telah dipisahkan ke dalam halaman dinamis yang datanya diambil dari basis data melalui model Django (Experience, Education, Skill, Achievement, dan Certification). Data pada bagian Education, Skill, Achievement, dan Certification kini dapat dikelola langsung melalui halaman web menggunakan form Create, Update, dan Delete yang dilindungi oleh secret key, selain juga dapat dikelola melalui Django Admin. Setiap bagian juga menyediakan endpoint API dalam format JSON. Sementara itu, bagian Profile dikelola melalui konteks view.
1. Fitur Section Profile: Menyediakan informasi identitas diri, latar belakang/bio, serta akses cepat ke media sosial dan kontak pribadi. Data profil diteruskan dari view melalui context ke template.
2. Fitur Halaman Education (/education/): Menampilkan riwayat pendidikan secara dinamis dari model Education, lengkap dengan nama institusi, jurusan, lokasi, dan tahun studi. Dilengkapi form untuk menambah, mengubah, dan menghapus data secara langsung melalui web (dilindungi secret key), serta endpoint JSON di `/api/education/`.
3. Fitur Halaman Experience (/experience/): Menampilkan seluruh pengalaman organisasi, magang, dan kepanitiaan secara dinamis dari model Experience, termasuk status "sedang berlangsung" atau "selesai". Dilengkapi form tambah dan hapus data (dilindungi secret key), serta endpoint JSON di `/api/experience/`.
4. Fitur Halaman Skills (/skills/): Menampilkan peta keahlian teknis (hard skill) dan non-teknis (soft skill) secara dinamis dari model Skill dengan indikator skill bar visual berdasarkan tingkat kemahiran. Dilengkapi form tambah, ubah, dan hapus data (dilindungi secret key), serta endpoint JSON di `/api/skills/`.
5. Fitur Halaman Achievements (/achievements/): Menampilkan prestasi akademik dan non-akademik secara dinamis dari model Achievement, dilengkapi fitur carousel pratinjau sertifikat untuk penghargaan yang memiliki berkas gambar. Dilengkapi form tambah, ubah, dan hapus data (dilindungi secret key), serta endpoint JSON di `/api/achievements/`.
6. Fitur Halaman Certifications (/certifications/): Menampilkan daftar lisensi dan sertifikasi secara dinamis dari model Certification, mencakup nama penerbit (issuer), rentang masa berlaku, deskripsi, serta tautan pratinjau sertifikat. Dilengkapi form tambah, ubah, dan hapus data (dilindungi secret key), serta endpoint JSON di `/api/certifications/`.

## Tech Stack
- Django: Berfungsi sebagai backend server yang mengelola routing URL, logika *view*, koneksi ke basis data melalui Django ORM, serta rendering *template* dinamis menggunakan Django Template Language.
- SQLite (lokal) / PostgreSQL (PWS): Basis data yang menyimpan seluruh data model (Experience, Education, Skill, Achievement, Certification), memungkinkan konten ditambah, diubah, atau dihapus melalui Django Admin maupun form pada halaman web tanpa mengedit kode secara langsung.
- python-decouple: Mengelola environment variable seperti secret key untuk proteksi form, memisahkan konfigurasi sensitif dari kode sumber agar tidak ikut ter-commit ke repository.
- HTML5: Mengatur hirarki dan struktur dokumen menggunakan elemen semantik (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`), serta Django Template Language untuk menampilkan data dinamis (`{% for %}`, `{% if %}`, `{% url %}`).
- CSS3 Murni: Mengelola tata letak dan estetika visual secara responsif menggunakan CSS Grid, Flexbox, Custom Properties, serta Media Queries.
- JavaScript (Vanilla): Menangani interaksi AJAX untuk proses hapus data secara asinkronus tanpa reload halaman, termasuk validasi secret key dan pembaruan tampilan secara langsung.
- PWS (Pacil Web Service): Platform deployment yang digunakan untuk menjalankan proyek secara live, menggunakan Gunicorn sebagai WSGI server dan Whitenoise untuk menyajikan berkas statis.

## Cara Menjalankan Proyek
1. Clone repository ini
git clone https://github.com/nurazizah56-dak/myportofolio
cd myportofolio

2. Aktifkan virtual environment
env\Scripts\activate

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



### Tugas 2
1. Ketika pengguna membuka halaman portofolio baru, misalnya halaman Education dengan URL `/education/`, browser mengirimkan permintaan GET ke server Django. Permintaan tersebut pertama kali diterima oleh `urls.py` milik proyek (`portofolio/urls.py`), yang mengarahkan URL utama ke URL aplikasi menggunakan `include("main.urls")`. Selanjutnya, permintaan `/education/` diteruskan ke `urls.py` milik aplikasi (`main/urls.py`), yang memetakan path `"education/"` ke fungsi `show_education` pada `views.py`. Fungsi *view* ini berperan sebagai penghubung antara model dan *template*: ia mengambil data dari model `Education` menggunakan `Education.objects.all()`, mengurutkannya berdasarkan tahun mulai, lalu memasukkannya ke dalam dictionary `context` dan meneruskannya ke *template* `education.html` melalui fungsi `render()`. Di dalam *template*, Django Template Language menggunakan data dari `context` untuk menampilkan informasi  `{% for edu in education_list %}` melakukan perulangan pada setiap objek `Education` dan menampilkan field seperti `institution_name`, `degree`, dan `location`, sementara blok `{% empty %}` menampilkan pesan alternatif jika tidak ada data. Setelah *template* selesai diproses, Django menghasilkan HTML dan mengirimkannya sebagai response ke browser.

2. Data untuk bagian portofolio baru sebaiknya disimpan pada model karena model memisahkan data dari tampilan aplikasi. Dari sisi pemeliharaan, penyimpanan data pada model membuat perubahan data menjadi lebih mudah dilakukan. Ketika data pendidikan masih ditulis langsung di HTML pada Tugas 1, perubahan seperti memperbaiki *typo* atau menambahkan riwayat pendidikan mengharuskan saya mengedit file HTML secara langsung. Setelah menggunakan model, data dapat ditambah, diubah, atau dihapus melalui Django Admin tanpa harus menyentuh *template* sama sekali. Pemisahan ini juga mempermudah pengembangan aplikasi — tampilan Education dapat diubah dari bentuk *grid card* menjadi *timeline*, misalnya, tanpa perlu menulis ulang seluruh data, karena *template* hanya bertanggung jawab menampilkan data yang tersimpan di model. Selain itu, pendekatan ini mengurangi risiko ketidakkonsistenan data yang bisa terjadi apabila informasi yang sama ditulis secara *hardcode* di beberapa *template* berbeda, seperti yang pernah saya alami ketika section Education sempat ada di dua tempat (halaman utama dan halaman terpisah) dengan risiko datanya tidak sinkron.

3. `makemigrations` berfungsi membuat file migrasi berdasarkan perubahan yang dilakukan pada `models.py`. File ini berisi instruksi mengenai perubahan struktur database yang perlu diterapkan, tetapi perintah ini sendiri belum benar-benar mengubah database. Sementara itu, `migrate` berfungsi menjalankan file migrasi yang telah dibuat sehingga perubahan struktur benar-benar diterapkan ke database yang digunakan aplikasi. Sebagai contoh, ketika saya membuat model `Education` baru dengan field seperti `institution_name`, `degree`, dan `start_year`, saya menjalankan `python manage.py makemigrations` untuk membuat file migrasi yang mendefinisikan tabel `Education`, lalu menjalankan `python manage.py migrate` agar tabel tersebut benar-benar dibuat di database. Proses yang sama juga perlu saya jalankan ulang secara terpisah di lingkungan PWS, karena database *production* (PostgreSQL) terpisah dari database lokal (SQLite), sehingga strukturnya harus disinkronkan secara manual di kedua environment.

## AI Disclosure
Tools yang digunakan: Claude

#### Peran AI dalam Pengembangan:
Penggunaan AI terutama mencakup:
1. Pemahaman Konsep: Membantu memahami alur MVT pada Django serta hubungan antara urls.py proyek, urls.py aplikasi, view, model, dan template.
2. Debugging: Membantu menganalisis beberapa error teknis selama pengembangan, seperti IndentationError, konfigurasi CSRF_TRUSTED_ORIGINS, serta masalah environment variable saat deployment.

#### Bagian yang Dibantu AI:
1. Penjelasan alur MVT dan hubungan antar komponen (urls, view, model, template).
2. Identifikasi penyebab error teknis (indentasi, konfigurasi CSRF, environment variable).

#### Bagian yang Dikerjakan Manual:
1. Perancangan dan penulisan model `Education` beserta field-nya.
2. Implementasi view, routing, dan template `education.html`.
3. Penulisan dan perbaikan unit test.
4. Eksekusi seluruh perintah migrate, `makemigrations`, dan Git.
5. Pengisian data Education melalui Django Admin, baik di lokal maupun PWS.
6. Pengujian langsung melalui `python manage.py test` dan `runserver`.
7. Pengambilan keputusan akhir terhadap setiap saran yang diberikan AI.

#### Refleksi Kritis terhadap Penggunaan AI:
AI membantu mempercepat proses memahami konsep dan menganalisis beberapa masalah teknis selama pengerjaan. Namun, saran dari AI tidak langsung diterapkan tanpa pemeriksaan. Setiap perubahan tetap diuji melalui terminal, browser, dan Django yang digunakan. AI juga tidak memiliki akses langsung ke lingkungan proyek saya, sehingga beberapa saran awal (misalnya terkait struktur file atau environment) perlu saya sesuaikan sendiri dengan kondisi proyek yang sebenarnya. Penggunaan AI juga menjadi pengingat bahwa memahami alasan di balik suatu solusi tetap penting agar saya dapat menyelesaikan masalah serupa secara mandiri.


### Tugas 3
1. Saya menggunakan `ModelForm` alih-alih membuat form HTML secara manual karena `ModelForm` dapat membuat field form berdasarkan struktur model yang sudah didefinisikan, termasuk tipe data, `max_length`, `choices`, serta validasi `blank` dan `null`. Dengan begitu, saya tidak perlu menulis ulang validasi yang sudah terdapat pada model dan dapat menjaga konsistensi antara model dan form. `ModelForm` juga menyediakan method `save()` yang dapat digunakan untuk menyimpan data ke database tanpa perlu menulis query secara manual. Selain itu, saya menggunakan `{% csrf_token %}` pada form karena Django menerapkan perlindungan terhadap CSRF untuk request yang mengubah data, seperti POST. Token CSRF digunakan oleh Django untuk memverifikasi bahwa request tersebut berasal dari sumber yang sah dan bukan request yang dikirim oleh situs lain atas nama pengguna.

2. Menurut saya, JSON lebih banyak digunakan dibandingkan XML dalam pengembangan aplikasi web modern karena sintaksnya lebih sederhana dan ringkas. JSON menggunakan struktur seperti object dan array sehingga lebih mudah dibaca dan diproses oleh aplikasi web. JSON juga memiliki dukungan bawaan pada JavaScript melalui `JSON.parse()` dan `JSON.stringify()`, serta didukung oleh berbagai bahasa pemrograman seperti Python, Java, dan lainnya. Hal ini membuat JSON mudah digunakan sebagai format pertukaran data antara frontend dan backend, termasuk pada RESTful API. XML tetap digunakan pada beberapa sistem, terutama sistem enterprise dan aplikasi lama, tetapi untuk kebutuhan web seperti proyek saya, JSON lebih praktis digunakan.

3. Ketika fungsi view mengembalikan data dalam bentuk JSON, alurnya dimulai dari client yang mengirim HTTP request ke endpoint tertentu, misalnya `/api/education/`. View kemudian mengambil data dari database menggunakan Django ORM, misalnya melalui `Model.objects.all()`, yang menghasilkan sebuah `QuerySet` berisi objek model. Objek tersebut perlu diubah ke format yang dapat dikirim melalui HTTP. Oleh karena itu, saya menggunakan proses serialization, misalnya dengan `serializers.serialize("json", queryset)`, untuk mengubah data model menjadi representasi JSON. Hasil tersebut kemudian dikembalikan melalui `HttpResponse` dengan `content_type="application/json"` sehingga client dapat mengenali format data yang diterima. Dengan serialization, data yang awalnya berupa objek model Python dapat digunakan sebagai format pertukaran data yang dapat dipahami oleh client atau aplikasi lain.

## AI Disclosure
Tools yang digunakan: Claude

#### Peran AI dalam Pengembangan:
Penggunaan AI terutama mencakup:
1. Memberikan contoh dan arahan dalam menyusun ModelForm, view (create, update, delete, dan JSON delivery), serta URL routing berdasarkan pola dari Tutorial 03.
2. Membantu debugging error seperti `TemplateSyntaxError` akibat penggunaan tag `{% static %}` dan `NoReverseMatch` akibat URL pattern yang belum terdaftar.
3. Memberikan saran terkait styling CSS untuk tampilan responsif dan tata letak tombol aksi.
4. Menjelaskan konsep Git branching dan konvensi commit message yang saya terapkan.

#### Bagian yang Dikerjakan Manual:
1. Pemilihan model Education, Skill, Achievement, dan Certification sebagai bagian tambahan untuk Tugas 3
2. Penyesuaian field form dan struktur data agar sesuai dengan kebutuhan proyek saya
3. Implementasi kode ke dalam proyek, serta pengujian manual seluruh alur CRUD dan JSON delivery melalui browser untuk memastikan implementasi berjalan sesuai yang diharapkan sebelum melakukan commit final.

#### Refleksi Kritis terhadap Penggunaan AI:
AI cukup membantu dalam menyusun kerangka kode awal ModelForm, view CRUD, dan URL routing untuk Education, Skill, Achievement, dan Certification karena pola implementasinya berulang. Namun, hasil AI tetap memerlukan penyesuaian. Beberapa masalah, seperti duplikasi struktur modal delete dan kesalahan path gambar pada Achievement dan Certification, baru ditemukan setelah pengujian langsung di browser. Saya juga tidak mengikuti seluruh saran AI, seperti penggunaan confirm() untuk delete, karena memilih mempertahankan mekanisme AJAX dan secret key agar konsisten dengan Experience pada Tutorial 3. Pengalaman ini menunjukkan bahwa AI membantu mempercepat proses coding dan debugging, tetapi hasilnya tetap perlu disesuaikan dengan kondisi proyek dan diverifikasi secara manual.