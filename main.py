import requests
import json
import time
import os
import subprocess

def clear_console():
    """ Membersihkan layar terminal dengan cara yang lebih kompatibel di berbagai OS. """
    try:
        if os.name == "nt":  # Windows
            subprocess.run("cls", shell=True)
        else:  # Linux & Mac
            subprocess.run("clear", shell=True)
    except Exception:
        print("\n" * 100)  # Alternatif jika perintah tidak berfungsi

def load_proxies():
    """ Memuat proxy dari file jika pengguna memilih untuk menggunakannya. """
    use_proxy = input("🔌 Apakah ingin menggunakan proxy? (y/n): ").strip().lower()
    if use_proxy == 'y':
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.read().splitlines()
                if proxies:
                    print(f"✅ {len(proxies)} proxy berhasil dimuat.\n")
                    return proxies
                else:
                    print("❌ File proxy.txt kosong! Lanjut tanpa proxy...\n")
        except FileNotFoundError:
            print("❌ File proxy.txt tidak ditemukan! Lanjut tanpa proxy...\n")
    return None

def get_access_token(refresh_token, proxy=None):
    """ Mendapatkan access token baru dari refresh token. """
    print("🔄 Refreshing access token...")
    url = "https://stork-prod-apps.auth.ap-northeast-1.amazoncognito.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "5msns4n49hmg3dftp2tp1t2iuh",
        "refresh_token": refresh_token
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers, proxies=proxy)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ Gagal refresh token!")
        return None

def check_token_validity(token, proxy=None):
    """ Mengecek apakah token masih valid dan menampilkan email + valid count. """
    url = "https://app-api.jp.stork-oracle.network/v1/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, proxies=proxy)
    
    if response.status_code == 200:
        data = response.json().get("data", {})
        email = data.get("email", "N/A")
        valid_count = data.get("stats", {}).get("stork_signed_prices_valid_count", 0)
        print(f"✅ Token valid | Email: {email} | Valid Count: {valid_count}")
        return True
    print("❌ Token invalid!")
    return False

def get_signed_price(token, proxy=None):
    """ Mengambil signed price dari API. """
    url = "https://app-api.jp.stork-oracle.network/v1/stork_signed_prices"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, proxies=proxy)
    
    if response.status_code == 200:
        data = response.json().get("data", {})
        for value in data.values():
            if "timestamped_signature" in value and "msg_hash" in value["timestamped_signature"]:
                msg_hash = value["timestamped_signature"]["msg_hash"]
                print(f"📜 Extracted msg_hash: {msg_hash}")
                return msg_hash
    print("❌ Gagal mendapatkan signed price!")
    return None

def validate_signed_price(token, msg_hash, proxy=None):
    """ Mengirim validasi signed price ke API. """
    url = "https://app-api.jp.stork-oracle.network/v1/stork_signed_prices/validations"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"msg_hash": msg_hash, "valid": True}
    response = requests.post(url, headers=headers, json=data, proxies=proxy)

    if response.status_code == 200:
        print("✅ Validation successful!")
    else:
        print("❌ Validation failed!")

def main():
    clear_console()
    print("🚀 Starting process...")
    print("""
    #################################################
    #                                               #
    #   🚀 Welcome to the #AidropID Stork Checker! 🚀  #
    #                                               #
    #################################################
    """)
    
    proxies = load_proxies()  # Tanya pengguna apakah ingin menggunakan proxy
    
    while True:
        clear_console()  # Membersihkan layar sebelum iterasi baru
        print("🔄 Memulai ulang proses...\n")

        try:
            with open("token.txt", "r") as token_file, open("refresh.txt", "r") as refresh_file:
                tokens = token_file.read().splitlines()
                refresh_tokens = refresh_file.read().splitlines()
            
            updated_tokens = []
            for i in range(len(tokens)):
                print(f"\n🔹 Processing token {i+1}...")

                # Pilih proxy secara bergantian jika tersedia
                proxy = {"http": proxies[i % len(proxies)], "https": proxies[i % len(proxies)]} if proxies else None
                
                token = tokens[i]
                refresh_token = refresh_tokens[i]

                if not check_token_validity(token, proxy):
                    print("🔄 Token tidak valid, mencoba refresh...")
                    token = get_access_token(refresh_token, proxy)
                    if not token:
                        print("❌ Gagal mendapatkan token baru. Melewati token ini...")
                        continue
                
                updated_tokens.append(token)
                msg_hash = get_signed_price(token, proxy)
                if msg_hash:
                    validate_signed_price(token, msg_hash, proxy)
            
            # Perbarui token yang berhasil diperbarui
            with open("token.txt", "w") as token_file:
                token_file.write("\n".join(updated_tokens))
            
            print("\n⏳ Process completed. Menunggu 60 detik sebelum loop berikutnya...")
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Terjadi kesalahan: {e}")
            time.sleep(10)  # Jika ada error, tunggu 10 detik lalu coba lagi

if __name__ == "__main__":
    main()
