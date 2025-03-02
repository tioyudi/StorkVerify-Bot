# Stork Auto Validation Bot

## 📌 Deskripsi
Script ini secara otomatis memvalidasi signed price dari API Stork Oracle menggunakan akses token. Jika token tidak valid, script akan mencoba me-refresh token menggunakan refresh token.

## 🚀 Fitur
- **Auto check token validity** (menampilkan email & valid count)
- **Auto refresh token jika invalid**
- **Auto fetch signed price**
- **Auto validate signed price**
- **Support penggunaan proxy (opsional)**
- **Looping otomatis setiap 60 detik**
- **Clear console setiap iterasi untuk tampilan bersih**

---

## 🔧 Persyaratan
- Python 3.x
- Library `requests`
- File `token.txt` (daftar access token, satu per baris)
- File `refresh.txt` (daftar refresh token, satu per baris)
- (Opsional) File `proxy.txt` (daftar proxy, satu per baris)

---

## 📥 Instalasi
1. **Clone repo atau download script**
```sh
 git clone https://github.com/tioyudi/StorkVerify-Bot.git
 cd StorkVerify-Bot
```

2. **Install dependencies**
```sh
pip install requests
```

3. **Siapkan file konfigurasi**
- **token.txt** → Simpan access token di sini
- **refresh.txt** → Simpan refresh token di sini (harus sesuai urutan dengan `token.txt`)
- **proxy.txt** (Opsional) → Simpan daftar proxy jika ingin menggunakan proxy

---

## ▶️ Cara Menjalankan
1. Jalankan script dengan perintah berikut:
```sh
python main.py
```
2. Saat program berjalan, Anda akan ditanya apakah ingin menggunakan proxy:
```
🔌 Apakah ingin menggunakan proxy? (y/n): 
```
- Jika **y**, maka proxy akan digunakan dari `proxy.txt`
- Jika **n**, script akan berjalan tanpa proxy

---

## 🔄 Cara Kerja
1. Membaca token dari `token.txt`
2. Mengecek apakah token valid (menampilkan email dan valid count)
3. Jika token invalid, mencoba refresh dengan `refresh.txt`
4. Jika token valid, mengambil **signed price**
5. Mengirim validasi signed price ke API
6. Menunggu 60 detik sebelum memulai kembali

---

## 📌 Contoh Output
```
🔌 Apakah ingin menggunakan proxy? (y/n): y
Using proxy: 192.168.1.1:8080

Processing token 1...
Checking token validity...
Email: example@email.com
Valid Count: 1500
Fetching signed price...
Extracted msg_hash: 0x123abc456def
Validating signed price...
Validation successful!

Processing token 2...
Checking token validity...
Token invalid, refreshing...
New token obtained.
Fetching signed price...
Extracted msg_hash: 0x789ghi101jkl
Validating signed price...
Validation successful!

Process completed. Waiting 60 seconds...
```

---

## ❗ Catatan
- Jika token gagal diperbarui, maka akan dilewati
- Jika terjadi error, program akan menunggu 10 detik sebelum melanjutkan



