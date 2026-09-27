Nama : Nur Azizah
NPM : 2506547935
Kelas : PBP A

# Portofolio Pribadi 

## Deskripsi Proyek
Tujuan dan Cakupan Utama: Website ini merupakan portofolio pribadi "About Me" yang dibangun menggunakan Django dengan arsitektur Model-View-Template (MVT). Seluruh bagian utama meliputi Experience, Education, Skills, Achievements, dan Certifications telah dipisahkan ke dalam halaman dinamis yang datanya diambil dari basis data melalui model Django (Experience, Education, Skill, Achievement, dan Certification). Website ini kini menerapkan sistem autentikasi bawaan Django dengan empat peran akses: pengunjung tanpa akun (hanya dapat membaca data), pengguna terdaftar (dapat membaca data serta memberi atau membatalkan star), editor (memiliki hak pengguna biasa dan dapat mengubah data), serta pemilik portofolio/superuser (memiliki akses penuh untuk membuat, mengubah, dan menghapus data). Setiap bagian juga menyediakan endpoint API dalam format JSON yang aman dari kebocoran data sensitif. Sementara itu, bagian Profile dikelola melalui konteks view dan menampilkan informasi sesi login terakhir menggunakan cookie.
1. Fitur Section Profile: Menyediakan informasi identitas diri, latar belakang/bio, serta akses cepat ke media sosial dan kontak pribadi. Data profil diteruskan dari view melalui context ke template. Halaman ini juga menampilkan waktu sesi login terakhir (`last_login`) yang disimpan melalui cookie.
2. Fitur Autentikasi (Register, Login, Logout): Pengunjung dapat mendaftar akun baru melalui `/register/`, login melalui `/login/`, dan logout melalui `/logout/`. Status login pengguna ditampilkan secara dinamis di navbar.
3. Fitur Halaman Education (/education/): Menampilkan riwayat pendidikan secara dinamis dari model Education, lengkap dengan nama institusi, jurusan, lokasi, dan tahun studi. Dilengkapi form untuk menambah, mengubah, dan menghapus data sesuai hak akses pengguna (superuser dan editor), fitur star bagi pengguna terdaftar, serta endpoint JSON di `/api/education/`.
4. Fitur Halaman Experience (/experience/): Menampilkan seluruh pengalaman organisasi, magang, dan kepanitiaan secara dinamis dari model Experience, termasuk status "sedang berlangsung" atau "selesai". Dilengkapi form tambah, ubah, dan hapus data (khusus superuser), fitur star bagi pengguna terdaftar, serta endpoint JSON di `/api/experience/`.
5. Fitur Halaman Skills (/skills/): Menampilkan peta keahlian teknis (hard skill) dan non-teknis (soft skill) secara dinamis dari model Skill dengan indikator skill bar visual berdasarkan tingkat kemahiran. Dilengkapi form tambah, ubah, dan hapus data sesuai hak akses, fitur star, serta endpoint JSON di `/api/skills/`.
6. Fitur Halaman Achievements (/achievements/): Menampilkan prestasi akademik dan non-akademik secara dinamis dari model Achievement, dilengkapi fitur carousel pratinjau sertifikat untuk penghargaan yang memiliki berkas gambar. Dilengkapi form tambah, ubah, dan hapus data sesuai hak akses, fitur star, serta endpoint JSON di `/api/achievements/`.
7. Fitur Halaman Certifications (/certifications/): Menampilkan daftar lisensi dan sertifikasi secara dinamis dari model Certification, mencakup nama penerbit (issuer), rentang masa berlaku, deskripsi, serta tautan pratinjau sertifikat. Dilengkapi form tambah, ubah, dan hapus data sesuai hak akses, fitur star, serta endpoint JSON di `/api/certifications/`.

## Tech Stack
- Django: Berfungsi sebagai backend server yang mengelola routing URL, logika *view*, koneksi ke basis data melalui Django ORM, serta rendering *template* dinamis menggunakan Django Template Language.
- Django Authentication System: Menyediakan sistem autentikasi bawaan (`UserCreationForm`, `AuthenticationForm`, `login()`, `logout()`) beserta model `User` dan `Group` untuk mengelola akun pengguna dan peran (superuser, editor, pengguna biasa).
- SQLite (lokal) / PostgreSQL (PWS): Basis data yang menyimpan seluruh data model (Experience, Education, Skill, Achievement, Certification) beserta relasi many-to-many `starred_by` ke model `User`, memungkinkan konten ditambah, diubah, atau dihapus melalui Django Admin maupun form pada halaman web sesuai hak akses.
- HTML5: Mengatur hirarki dan struktur dokumen menggunakan elemen semantik (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`), serta Django Template Language untuk menampilkan data dinamis (`{% for %}`, `{% if %}`, `{% url %}`).
- CSS3 Murni: Mengelola tata letak dan estetika visual secara responsif menggunakan CSS Grid, Flexbox, Custom Properties, serta Media Queries.
- JavaScript (Vanilla): Menangani interaksi AJAX untuk proses hapus data secara asinkronus tanpa reload halaman, termasuk pembaruan tampilan secara langsung dan konfirmasi ganda sebelum penghapusan data.
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

## Tugas 4
## Pertanyaan Reflektif
Minggu ini dihilangkan

## AI Disclosure
Tools yang digunakan: Claude

#### Peran AI dalam Pengembangan:
Penggunaan AI terutama mencakup:
1. Memberikan contoh dan arahan dalam mengimplementasikan sistem autentikasi bawaan Django (register, login, logout), penggunaan session dan cookie (`last_login`), serta mekanisme CSRF, mengikuti pola dari Tutorial 04.
2. Memberikan arahan dalam menerapkan sistem role-based authorization dengan empat peran (pengunjung, pengguna biasa, editor, superuser) menggunakan `@login_required`, `is_superuser`, dan `Django Group` untuk peran editor, mencakup implementasi pada bagian Education, Experience, Skill, Achievement, dan Certification.
3. Memberikan contoh implementasi fitur star (`ManyToManyField` ke model `User`) beserta view `toggle_star` untuk tiap bagian portofolio.
4. Membantu debugging error seperti `ImportError` akibat fungsi yang hilang saat pengeditan `views.py`, serta `TemplateSyntaxError` akibat tag Django yang tidak seimbang.
5. Memberikan saran styling CSS untuk kesejajaran tombol aksi (star, edit, delete) pada berbagai ukuran layar.

#### Bagian yang Dikerjakan Manual:
1. Pemilihan bagian Education sebagai implementasi wajib Tugas 4, serta penerapan pola yang sama secara mandiri pada bagian Experience, Skill, Achievement, dan Certification sebagai pengembangan tambahan di luar instruksi minimum.
2. Pembuatan Group "Editor" melalui Django Admin serta penetapan akun pengguna ke dalam grup tersebut, baik di lingkungan lokal maupun PWS.
3. Implementasi kode ke dalam proyek, penyesuaian struktur template agar kontrol aksi (create, edit, delete) tampil sesuai peran pengguna yang sedang login.
4. Pengujian manual seluruh alur autentikasi dan otorisasi (pengunjung, pengguna biasa, editor, superuser) melalui browser untuk memastikan setiap peran hanya dapat melakukan tindakan yang diizinkan.
5. Penambahan fitur konfirmasi ganda (modal kustom dan `confirm()` bawaan browser) sebelum data dihapus, sebagai lapisan pencegahan kesalahan pengguna di luar instruksi tutorial.

#### Refleksi Kritis terhadap Penggunaan AI:
AI membantu mempercepat penerapan pola autentikasi dan otorisasi yang berulang di lima bagian portofolio, terutama dalam menyusun kombinasi dekorator `@login_required` dengan pemeriksaan `is_superuser` dan keanggotaan grup Editor. Namun, saya menemukan bahwa AI tidak selalu memprediksi kondisi aktual proyek saya, misalnya saat fungsi `delete_experience` sempat hilang akibat proses penyuntingan manual yang tidak sengaja menimpa kode sebelumnya; masalah ini baru terdeteksi melalui `ImportError` saat server dijalankan, bukan dari analisis AI sebelumnya. Saya juga secara sadar memilih untuk memperluas penerapan sistem role-based ke seluruh bagian portofolio (bukan hanya Education), meskipun ini di luar cakupan minimum tugas, untuk menjaga konsistensi arsitektur dan menghindari dua mekanisme proteksi berbeda (secret key dan autentikasi Django) berjalan bersamaan dalam satu proyek. Pengalaman ini menegaskan bahwa AI efektif digunakan sebagai referensi pola implementasi, tetapi verifikasi terhadap kondisi kode yang sebenarnya tetap sepenuhnya menjadi tanggung jawab saya sebagai pengembang.