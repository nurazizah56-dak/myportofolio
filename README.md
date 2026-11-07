Nama : Nur Azizah
NPM : 2506547935
Kelas : PBP A

# Portofolio Pribadi (Tugas 6 - Django REST Framework)

## Deskripsi Proyek
Website ini merupakan aplikasi portofolio pribadi "About Me" berbasis web yang mengintegrasikan Django dengan **Django REST Framework (DRF)**. Seluruh modul portofolio (Education, Skills, Experience, Achievements, dan Certifications) telah diimplementasikan sebagai **RESTful API** di bawah rute `/api/v1/` dengan dukungan penuh operasi HTTP (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`). 

Sistem menerapkan kontrol akses berbasis peran (*role-based authorization*) yang ketat di sisi server melalui *permission class* kustom `IsPortfolioOwnerOrEditorOrReadOnly` dan `IsAuthenticated`, mencakup 4 tingkatan peran:
1. **Unauthenticated Visitor (Pengunjung)**: Hanya memiliki izin baca (`GET`, `HEAD`) pada daftar dan detail setiap entitas portofolio.
2. **Authenticated User (Pengguna Terdaftar)**: Memiliki izin baca serta dapat memberikan atau mencabut bintang (*star/unstar*) pada entitas portofolio.
3. **Editor**: Pengguna dalam grup `Editor` yang memiliki izin baca, star, serta memperbarui/mengedit data yang ada secara parsial (`PATCH`) maupun penuh (`PUT`).
4. **Superuser / Owner (Pemilik Portofolio)**: Memiliki hak akses penuh untuk membuat data baru (`POST`), memperbarui (`PUT`/`PATCH`), serta menghapus data (`DELETE`).

Di sisi antarmuka, aplikasi memanfaatkan komunikasi asinkronus (AJAX) menggunakan JavaScript murni (Vanilla JS) yang berinteraksi langsung dengan endpoint DRF. Seluruh proses pengambilan data, pencarian interaktif dengan teknik *debouncing*, penambahan data via modal, pengeditan data via modal edit, pergantian status bintang, hingga penghapusan data berjalan dinamis tanpa memuat ulang (*reload*) halaman, dilengkapi sistem notifikasi umpan balik (*toast*) dan sanitasi input terhadap ancaman Cross-Site Scripting (XSS). Rangkaian pengujian otomatis menyeluruh dibangun menggunakan `APITestCase` (102 tes) yang memvalidasi seluruh peran, validasi serializer, dan penegakan CSRF pada `SessionAuthentication`.

### Fitur-Fitur Utama Portofolio (RESTful API & AJAX Frontend):
1. **Fitur Section Profile**: Menyediakan informasi profil diri, riwayat singkat, minat, bio, tautan sosial, serta menampilkan waktu login terakhir (`last_login`) pengguna berbasis cookie.
2. **Fitur Autentikasi**: Menyediakan alur registrasi (`/register/`), login (`/login/`), dan logout (`/logout/`) yang terintegrasi dengan `SessionAuthentication` Django dan DRF.
3. **Fitur Education (`/education/` & `/api/v1/education/`)**: Menampilkan riwayat pendidikan dinamis dengan dukungan pencarian langsung, modal tambah, modal edit untuk Editor/Superuser, fitur star, dan hapus data.
4. **Fitur Skills (`/skills/` & `/api/v1/skills/`)**: Menampilkan daftar keahlian teknis (*hard skills*) dan non-teknis (*soft skills*) dengan visualisasi persentase tingkat kemahiran (*progress bar*), filter/search, modal tambah, modal edit, star, dan hapus data.
5. **Fitur Experience (`/experience/` & `/api/v1/experience/`)**: Menampilkan linimasa pengalaman organisasi, kepanitiaan, dan pekerjaan (dengan status *ongoing* atau selesai), filter pencarian ber-debounce, modal tambah, modal edit, star, dan hapus data.
6. **Fitur Achievements (`/achievements/` & `/api/v1/achievements/`)**: Menampilkan prestasi akademik dan non-akademik, pratinjau sertifikat dalam bentuk *carousel* horizontal, live search, modal tambah, modal edit, star, dan hapus data.
7. **Fitur Certifications (`/certifications/` & `/api/v1/certifications/`)**: Menampilkan lisensi dan sertifikasi profesional beserta nama penerbit (*issuer*) dan rentang validitas, pencarian instan, modal tambah, modal edit, star, dan hapus data.

## Tech Stack
- **Django**: Backend framework yang menangani routing URL, manajemen basis data melalui Django ORM, manajemen sesi, dan rendering template antarmuka dasar.
- **Django REST Framework (DRF)**: Framework REST API yang mengelola serialisasi data (`ModelSerializer`), validasi input, sanitasi XSS (`strip_tags`), penanganan metode HTTP (`@api_view`), autentikasi sesi (`SessionAuthentication`), serta otorisasi berbasis peran via *permission classes* kustom (`IsPortfolioOwnerOrEditorOrReadOnly`, `IsAuthenticated`).
- **Django Authentication System**: Sistem autentikasi bawaan (`User`, `Group`) untuk membagi peran pengguna (Visitor, Authenticated User, Editor, Superuser/Owner).
- **SQLite (Lokal) / PostgreSQL (PWS)**: Basis data relasional yang menyimpan data entitas portofolio dan relasi many-to-many `starred_by` dengan integritas referensial UUID.
- **HTML5 & CSS3 Murni**: Struktur semantik modern dengan CSS kustom tanpa framework eksternal, memanfaatkan CSS Grid, Flexbox, CSS Variables, dan Popover API untuk dialog modal.
- **JavaScript (Vanilla)**: Mengelola logika AJAX asinkronus menggunakan `fetch()`, integrasi endpoint REST DRF, penanganan token CSRF (`X-CSRFToken`), live search dengan teknik *debouncing*, manipulasi DOM dinamis, perlindungan XSS (`escapeHtml`), dan notifikasi *toast*.
- **PWS (Pacil Web Service)**: Platform deployment hosting aplikasi berbasis cloud dari Fasilkom UI menggunakan Gunicorn dan WhiteNoise.

## Cara Menjalankan Proyek
1. Clone repository ini
```bash
git clone https://github.com/nurazizah56-dak/myportofolio
cd myportofolio
```

2. Aktifkan virtual environment
```bash
# Windows
env\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Jalankan migrasi dan test suite
```bash
python manage.py migrate
python manage.py test
```

5. Jalankan server lokal
```bash
python manage.py runserver
```
Buka browser ke `http://127.0.0.1:8000/`.

---

### Tugas 6
1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan `PUT` dan `PATCH` beserta contoh kapan masing-masing sebaiknya digunakan!**
   - **REST (Representational State Transfer)** adalah gaya arsitektur perangkat lunak yang dirumuskan oleh Roy Fielding untuk merancang sistem hipermedia terdistribusi yang terhubung melalui jaringan. Arsitektur REST menetapkan serangkaian batasan (*architectural constraints*), di antaranya pemisahan *Client-Server*, *Statelessness* (server tidak menyimpan state klien antar-permintaan), *Cacheability*, *Layered System*, dan *Uniform Interface* (identifikasi *resource* berbasis URI unik, manipulasi data melalui representasi standar, serta pesan yang *self-descriptive*).
   - **Mengapa mengembalikan JSON saja belum cukup?** JSON hanyalah salah satu format serialisasi data (representasi pesan). Sebuah endpoint dapat mengembalikan format JSON (misalnya gaya RPC seperti `POST /getSkillList` atau `POST /updateData`), namun tetap **tidak** memenuhi kaidah RESTful jika melanggar prinsip-prinsip dasarnya. Suatu API baru layak disebut RESTful apabila:
     1. Berorientasi pada *resource* (menggunakan kata benda jamak pada URI seperti `/api/v1/skills/`, bukan kata kerja tindakan).
     2. Memanfaatkan HTTP verbs secara semantik (`GET` untuk membaca, `POST` untuk membuat data baru, `PUT`/`PATCH` untuk memperbarui, dan `DELETE` untuk menghapus).
     3. Menggunakan kode status HTTP standar secara tepat (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `403 Forbidden`, `404 Not Found`).
     4. Bersifat *stateless*, di mana setiap request membawa seluruh konteks informasi yang diperlukan untuk diproses oleh server secara independen.
   - **Perbedaan `PUT` dan `PATCH` beserta contoh penggunaannya:**
     - `PUT` (*Full Replacement*): Bersifat idempoten dan digunakan untuk mengganti **seluruh** representasi dari suatu *resource* dengan representasi data baru yang dikirimkan. Jika ada atribut yang tidak disertakan dalam payload permintaan, atribut tersebut dianggap dihapus atau direset ke nilai bawaan.
       *Contoh*: Pembaruan total data sertifikasi melalui form edit lengkap yang mengirimkan seluruh field (judul, penerbit, rentang waktu, deskripsi, ikon, gambar) menggunakan `PUT /api/v1/certifications/<id>/`.
     - `PATCH` (*Partial Update*): Digunakan untuk melakukan modifikasi **sebagian** (parsial) terhadap atribut tertentu dari suatu *resource* tanpa mengubah atribut lain yang tidak dikirimkan.
       *Contoh*: Pengguna dengan peran Editor yang hanya memiliki izin untuk memperbarui deskripsi atau tahun pencapaian tanpa mengubah judulnya, atau aksi spesifik memperbarui satu status menggunakan `PATCH /api/v1/achievements/<id>/` dengan payload `{"description": "Deskripsi terbarui"}`.

2. **Jelaskan peran *serializer* pada Django REST Framework! Apa keuntungannya dibandingkan merakit *dictionary* secara manual dengan `JsonResponse` seperti pada Tutorial 05?**
   - **Peran Serializer:**
     Serializer bertindak sebagai jembatan dua arah (*two-way transformer*) di dalam DRF:
     1. *Serialization*: Mengubah struktur data kompleks Django (objek model, instance, atau queryset) menjadi tipe data asli Python (*dict*, *list*, primitif) yang dapat dirender dengan mudah menjadi format JSON atau XML.
     2. *Deserialization & Validation*: Mengambil payload data mentah dari permintaan klien (JSON), memvalidasi tipe data dan batasan bisnisnya, serta mengonversinya kembali menjadi instance objek model yang siap disimpan ke basis data.
   - **Keuntungan Serializer dibanding merakit manual dengan `JsonResponse`:**
     1. **Validasi Kuat dan Otomatis**: Serializer secara otomatis membaca tipe data, panjang maksimal, dan batasan field dari model Django, serta mendukung validasi kustom melalui fungsi `validate_<field_name>()` dan `validate()`. Pada pendekatan manual `JsonResponse`, setiap validasi harus ditulis baris per baris menggunakan percabangan `if-else` yang rentan kesalahan dan sulit dirawat.
     2. **Sanitasi Terpusat**: Logika pencegahan celah keamanan (seperti `strip_tags` untuk sanitasi XSS) dapat disatukan langsung di dalam serializer sebelum data menyentuh basis data atau logika view.
     3. **Standarisasi Format Error**: Jika validasi gagal, serializer secara konsisten mengembalikan struktur pesan error yang terpetakan rapi per field beserta status kode HTTP yang sesuai (`400 Bad Request`), memudahkan antarmuka frontend mengonsumsinya.
     4. **Dukungan Operasi Parsial (`partial=True`)**: Serializer mendukung pembaruan parsial (`PATCH`) secara otomatis tanpa perlu logika kondisional manual untuk mengecek apakah suatu field hadir di dalam request body.
     5. **Kemudahan Menangani Relasi & Field Kalkulasi**: Melalui `SerializerMethodField` atau nested serializer, data turunan seperti jumlah star (`star_count`), status apakah user sedang login sudah memberi star (`is_starred`), dan nama-nama pemberi star (`starred_by_names`) dapat dikomputasi secara elegan dan konsisten.

3. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan *permission class* di server, bukan hanya dengan menyembunyikan tombol di *template*?**
   - **Perbedaan Autentikasi vs Otorisasi:**
     - **Autentikasi (Authentication)** adalah mekanisme untuk membuktikan dan memverifikasi **identitas** pengguna — menjawab pertanyaan *"Siapakah Anda?"*. Di DRF, autentikasi (seperti `SessionAuthentication`) membaca kredensial (cookie sesi, token header) untuk mengidentifikasi pengguna dan mengaitkannya ke `request.user` atau menetapkannya sebagai `AnonymousUser`.
     - **Otorisasi (Authorization)** adalah mekanisme untuk memeriksa dan menegakkan **hak akses / izin** — menjawab pertanyaan *"Apakah pengguna ini berhak melakukan aksi ini pada resource ini?"*. Di DRF, otorisasi diatur melalui *permission classes* (seperti `IsPortfolioOwnerOrEditorOrReadOnly` atau `IsAuthenticated`) yang mengevaluasi apakah pengguna memiliki hak untuk memanggil metode HTTP tertentu (`GET`, `POST`, `PATCH`, `DELETE`) terhadap suatu endpoint atau instance objek.
   - **Mengapa hak akses HARUS diperiksa di server melalui *permission class*?**
     - Menyembunyikan tombol aksi (seperti tombol Add, Edit, Delete) di template HTML hanyalah pengelolaan antarmuka (*UI convenience*) untuk kenyamanan visual pengguna biasa, **bukan mekanisme pengamanan sistem**.
     - Pengguna dengan niat jahat dapat dengan mudah memeriksa struktur kode JavaScript di browser, melihat rute API di tab *Network Developer Tools*, lalu mengirimkan permintaan HTTP secara langsung menggunakan alat seperti `fetch()`, `curl`, atau Postman ke endpoint server tanpa pernah menyentuh tombol di template.
     - Tanpa *permission class* di sisi server, server akan memproses permintaan tersebut secara membabi buta, menyebabkan celah keamanan fatal (*Broken Access Control*). Oleh karena itu, server harus selalu menjadi otoritas tunggal (*single source of truth*) yang memvalidasi setiap hak akses dan menolak aksi ilegal dengan status `403 Forbidden` atau `401 Unauthorized`.

**4. Mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai `SessionAuthentication`? Mengapa test yang memakai `force_authenticate` tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**
- **Mengapa permintaan pengubah data memerlukan token CSRF pada `SessionAuthentication`?**
  - `SessionAuthentication` memanfaatkan cookie sesi bawaan browser (`sessionid`) untuk mengenali pengguna yang sudah login.
  - Kerentanan CSRF (*Cross-Site Request Forgery*) terjadi karena browser dapat secara otomatis menyertakan cookie yang tersimpan untuk domain tujuan pada HTTP request, termasuk request yang dipicu dari situs lain.
  - Jika API menerima permintaan pengubah data seperti `POST`, `PUT`, `PATCH`, dan `DELETE` hanya berdasarkan cookie sesi tanpa memverifikasi token CSRF, penyerang dapat mencoba mengirimkan permintaan berbahaya atas nama pengguna yang sedang login.
  - Oleh karena itu, DRF mewajibkan token CSRF untuk setiap metode yang termasuk *unsafe methods* pada `SessionAuthentication`. Token ini dikirimkan melalui header `X-CSRFToken` untuk memastikan bahwa permintaan berasal dari konteks frontend yang memiliki token CSRF yang valid.
- **Mengapa `force_authenticate` tidak cukup untuk menguji perlindungan CSRF?**
  - Metode `force_authenticate(user=...)` pada pengujian DRF secara langsung menetapkan pengguna yang digunakan dalam request sehingga melewati proses autentikasi normal pada authentication class. Akibatnya, mekanisme pemeriksaan CSRF yang dilakukan oleh `SessionAuthentication` tidak dijalankan.
  - Dengan demikian, pengujian menggunakan `force_authenticate` tidak dapat membuktikan bahwa perlindungan CSRF berjalan dengan benar karena request tidak melalui mekanisme autentikasi sesi yang melakukan pemeriksaan CSRF.
  - Untuk menguji perlindungan CSRF, pengujian perlu menggunakan `APIClient(enforce_csrf_checks=True)` dengan autentikasi berbasis sesi melalui `client.login()`. Selanjutnya, permintaan pengubah data tanpa token CSRF yang valid seharusnya ditolak oleh server dengan status kode `403 Forbidden`.
---

## AI Disclosure
Tools yang digunakan: Claude

### Bagian yang Dibantu AI dan Kontribusi Saya
| Bagian | Peran AI | Yang saya lakukan |
|---|---|---|
| Perancangan REST API | Memberikan referensi dan alternatif pendekatan implementasi Django REST Framework. | Menentukan kebutuhan API berdasarkan fitur dan struktur model yang sudah dikembangkan pada proyek portofolio. |
| Serializer dan Validasi | Memberikan contoh implementasi serializer, validasi input, sanitasi data, dan pengelolaan relasi. | Menyesuaikan kebutuhan field dan validasi dengan karakteristik data pada setiap section portofolio. |
| Autentikasi dan Otorisasi | Membantu mengeksplorasi penerapan autentikasi dan pembagian hak akses menggunakan permission class. | Menentukan skenario hak akses untuk pengunjung, pengguna terdaftar, editor, dan pemilik portofolio. |
| API dan Integrasi Frontend | Memberikan referensi implementasi endpoint serta penggunaan Fetch API untuk menghubungkan frontend dengan backend. | Menyesuaikan integrasi dengan template dan JavaScript yang sudah ada, termasuk perubahan struktur respons JSON. |
| Pengujian dan Keamanan | Membantu mengeksplorasi skenario pengujian API, validasi data, dan perlindungan CSRF. | Menjalankan pengujian, mengevaluasi hasilnya, serta melakukan penyesuaian ketika ditemukan ketidaksesuaian. |
| Version Control | Memberikan rekomendasi pengelompokan fitur dan urutan pengerjaan. | Mengatur branch, melakukan commit bertahap, mengelola Pull Request, dan melakukan merge ke branch utama. |

### Keterbatasan AI yang saya temui dan perbaikan manual
- **Asumsi struktur proyek yang kurang tepat.** AI sempat menganggap `Experience` sebagai padanan `Project`. Saya mengoreksi asumsi tersebut dengan menjelaskan struktur lima section pada portofolio sehingga pendekatan implementasi dapat disesuaikan.
- **Masalah lingkungan pengembangan lokal.** Terjadi penguncian berkas pada direktori `.git` akibat sinkronisasi OneDrive di Windows. Kendala tersebut perlu diidentifikasi dan ditangani melalui terminal secara manual.
- **Penyesuaian pengujian CSRF.** Saran awal AI mengenai pengujian CSRF pada DRF perlu diperiksa kembali. Penggunaan `force_authenticate` tidak cukup untuk membuktikan mekanisme perlindungan CSRF pada `SessionAuthentication`, sehingga pengujian disesuaikan menggunakan `APIClient(enforce_csrf_checks=True)` dan autentikasi sesi.
- **Perubahan struktur respons API.** Peralihan dari struktur data view Django sebelumnya ke format respons serializer DRF memerlukan penyesuaian pada JavaScript dan template HTML agar proses manipulasi DOM, sorting, serta modal edit tetap berjalan.
- **Penyesuaian konfigurasi dan debugging.** Beberapa saran AI tidak selalu langsung sesuai dengan lingkungan lokal dan kebutuhan proyek. Oleh karena itu, implementasi perlu diperiksa kembali melalui pengujian dan penyesuaian manual sebelum digunakan.

### Refleksi Kritis terhadap Penggunaan AI
Penggunaan AI membantu mempercepat proses pengembangan proyek, terutama dalam memahami konsep, menyusun struktur implementasi, menghasilkan kode yang repetitif, dan mengeksplorasi alternatif penyelesaian masalah. Namun, hasil yang diberikan AI tidak selalu langsung sesuai dengan kondisi proyek.
Selama proses pengerjaan, saya menemukan bahwa AI dapat menghasilkan asumsi yang kurang tepat terhadap struktur proyek, memberikan saran konfigurasi yang perlu disesuaikan, serta menghasilkan implementasi yang masih membutuhkan pemeriksaan melalui pengujian. Hal tersebut membuat saya perlu memahami alur kerja kode, memeriksa kesesuaian implementasi, dan melakukan debugging terhadap kendala yang ditemukan.
Dari pengalaman tersebut, saya memahami bahwa AI merupakan alat bantu dalam proses pengembangan, bukan pengganti pemahaman dan tanggung jawab pengembang. Keputusan implementasi, pemeriksaan hasil, pengujian, serta perbaikan akhir tetap menjadi tanggung jawab saya.