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

## Tugas 5
## Pertanyaan Reflektif
1. **Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**
   Debouncing adalah teknik pemrograman yang menunda eksekusi sebuah fungsi sampai jeda waktu tertentu berlalu sejak pemanggilan fungsi tersebut yang terakhir. Pada fitur pencarian berbasis AJAX, sebuah *request* ke server biasanya terpicu setiap kali pengguna mengetik karakter baru (misalnya event `keyup` atau `input`). Tanpa debouncing, mengetik kata "django" akan memicu 6 request terpisah secara berurutan dalam waktu yang sangat singkat. Hal ini dapat membebani server, menyia-nyiakan *bandwidth*, dan menyebabkan *race condition* pada hasil pencarian. Dengan menerapkan debouncing, request hanya akan dikirim setelah pengguna berhenti atau menjeda ketikannya selama waktu tertentu (misalnya 300ms). Teknik ini sangat penting karena secara signifikan mengurangi jumlah *request* ke server, sehingga meningkatkan performa dan efisiensi aplikasi.

2. **Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?**
   Fungsi `fetch()` berjalan secara asinkronus (asynchronous) dan mengembalikan sebuah *Promise*. Kata kunci `await` berfungsi untuk memberitahu JavaScript agar "menunggu" dan menunda eksekusi kode di baris selanjutnya sampai *Promise* dari `fetch()` tersebut berstatus *resolved* (berhasil menyelesaikan *request* jaringan dan mengembalikan HTTP Response).
   **Jika kita tidak menggunakan `await`:** Kode di bawahnya akan langsung dieksekusi tanpa menunggu balasan dari server. Variabel yang menampung hasil `fetch()` hanya akan berisi objek *Promise* yang masih berstatus *pending*, bukan berisi balasan data sebenarnya. Akibatnya, saat kita mencoba mengolah data tersebut (seperti menjalankan `.json()`), program akan mengalami error karena data yang dibutuhkan dari *response* belum benar-benar ada.

3. **Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**
   Serangan XSS (Cross-Site Scripting) adalah celah keamanan situs web di mana penyerang menyusupkan kode atau skrip berbahaya (biasanya JavaScript) ke dalam data situs, yang kemudian akan tanpa sengaja dieksekusi oleh browser pengguna lain yang melihat data tersebut. Ini bisa berakibat pencurian *cookie*, *session*, atau data sensitif pengguna.
   **Mengapa AJAX/JavaScript lebih rentan?** Saat kita me-render data langsung menggunakan template HTML Django (misalnya `{{ nama }}`), Django memiliki fitur *auto-escaping* bawaan. Fitur ini secara otomatis mengubah karakter berbahaya seperti `<` dan `>` menjadi entitas aman HTML (`&lt;` dan `&gt;`), sehingga tag berbahaya tidak bisa dieksekusi oleh browser. Namun, ketika kita mengambil data dalam bentuk JSON mentah melalui AJAX lalu menampilkannya secara dinamis ke halaman menggunakan JavaScript (contohnya mengatur nilai properti `.innerHTML`), JavaScript tidak akan melakukan *auto-escaping* secara otomatis. Jika tidak ada mekanisme pencegahan tambahan (seperti fungsi `escapeHtml` manual di JavaScript atau sanitasi `strip_tags` pada *backend*), string HTML berbahaya dari JSON tersebut akan disisipkan dan dieksekusi begitu saja, membuat aplikasi sangat rentan terhadap serangan XSS.

## AI Disclosure
Tools yang digunakan: Gemini

#### Peran AI dalam Pengembangan
1. Memberikan contoh dan arahan terkait penerapan AJAX pada halaman Skills, Achievements, dan Certifications, termasuk pola penggunaan `get_json`, pembuatan view `create_ajax`, dan penambahan endpoint `add-ajax/`. Implementasi dan penyesuaian kode dilakukan secara mandiri sesuai struktur proyek.
2. Memberikan saran terkait struktur halaman HTML untuk mendukung AJAX, seperti loading state, error state, empty state, debounced search, modal form untuk superuser, serta rendering data secara dinamis menggunakan `escapeHtml`. Struktur akhir dan penyesuaian dengan kebutuhan masing-masing halaman dilakukan secara manual.
3. Memberikan referensi mengenai penggunaan Popover API dalam pembuatan komponen modal seperti `skill_form_modal.html`, kemudian diimplementasikan dan disesuaikan secara manual dengan struktur proyek.
4. Memberikan arahan mengenai sanitasi input menggunakan metode `clean_...` pada form dan `strip_tags` sebagai salah satu lapisan mitigasi terhadap penyisipan HTML atau script berbahaya. Implementasi metode tersebut dilakukan secara manual pada form yang diperlukan.

#### Bagian yang Dikerjakan Manual
1. Pemilihan bagian Skills, Achievements, dan Certifications sebagai target implementasi AJAX sebagai pengembangan tambahan di luar tutorial dasar yang hanya menargetkan satu bagian.
2. Implementasi dan penyesuaian kode AJAX pada masing-masing halaman, termasuk pengaturan endpoint, pengolahan response JSON, rendering data, pencarian dengan debouncing, loading/error/empty state, dan integrasi dengan struktur template yang sudah ada.
3. Pembuatan dan penyesuaian komponen modal serta form sesuai kebutuhan masing-masing halaman, termasuk pengaturan hak akses superuser.
4. Verifikasi pola inline delete agar sesuai dengan kebutuhan setiap halaman serta memastikan proses penghapusan tetap menggunakan dua tahap konfirmasi, yaitu modal kustom dan `confirm()` bawaan browser.
5. Implementasi sanitasi input pada form yang diperlukan serta penyesuaian `escapeHtml` pada proses rendering data secara dinamis.
6. Pengujian manual alur CRUD melalui AJAX, pencarian dengan debouncing, serta pengujian terhadap input yang mengandung HTML/script pada seluruh form yang diubah.

#### Refleksi Kritis terhadap Penggunaan AI:
AI membantu mempercepat penerapan pola autentikasi dan otorisasi yang berulang di lima bagian portofolio, terutama dalam menyusun kombinasi dekorator `@login_required` dengan pemeriksaan `is_superuser` dan keanggotaan grup Editor. Namun, saya menemukan bahwa AI tidak selalu memprediksi kondisi aktual proyek saya, misalnya saat fungsi `delete_experience` sempat hilang akibat proses penyuntingan manual yang tidak sengaja menimpa kode sebelumnya; masalah ini baru terdeteksi melalui `ImportError` saat server dijalankan, bukan dari analisis AI sebelumnya. Saya juga secara sadar memilih untuk memperluas penerapan sistem role-based ke seluruh bagian portofolio (bukan hanya Education), meskipun ini di luar cakupan minimum tugas, untuk menjaga konsistensi arsitektur dan menghindari dua mekanisme proteksi berbeda (secret key dan autentikasi Django) berjalan bersamaan dalam satu proyek. Pengalaman ini menegaskan bahwa AI efektif digunakan sebagai referensi pola implementasi, tetapi verifikasi terhadap kondisi kode yang sebenarnya tetap sepenuhnya menjadi tanggung jawab saya sebagai pengembang.

#### Refleksi Kritis terhadap Penggunaan AI
Secara keseluruhan, AI sangat membantu mempercepat penerapan pola-pola berulang, seperti autentikasi role-based di berbagai bagian portofolio dan pemahaman tentang AJAX, debouncing, serta sanitasi input. Namun, saya menemukan bahwa AI tidak selalu dapat memprediksi kondisi aktual atau arsitektur spesifik proyek saya. Misalnya, masalah kode yang tidak sengaja tertimpa (seperti hilangnya `delete_experience`) baru terdeteksi melalui error saat runtime, bukan dari analisis AI. Selain itu, setiap kode dari AI untuk implementasi AJAX dan DOM manipulation tidak bisa langsung di-copy-paste, melainkan harus disesuaikan dengan struktur template dan kebutuhan keamanan (seperti mencegah XSS). Pengalaman ini menegaskan bahwa AI efektif digunakan sebagai referensi pola implementasi dan alat bantu pemahaman, tetapi verifikasi dan pengujian terhadap kondisi kode yang sebenarnya tetap sepenuhnya menjadi tanggung jawab saya sebagai pengembang.