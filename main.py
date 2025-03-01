import requests
import json
import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_access_token(refresh_token):
    print("Getting access token...")
    url = "https://stork-prod-apps.auth.ap-northeast-1.amazoncognito.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "5msns4n49hmg3dftp2tp1t2iuh",
        "refresh_token": refresh_token
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    print("Access Token Response Status:", response.status_code)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def check_token_validity(token):
    print("Checking token validity...")
    url = "https://app-api.jp.stork-oracle.network/v1/me"
    headers = {
        "Authorization": f"Bearer {token}",
        "Origin": "chrome-extension://knnliglhgkmlblppdejchidfihjnockl",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print("Token Validity Response Status:", response.status_code)
    print("ME Response:", response.json())
    return response.status_code == 200

def get_signed_price(token):
    print("Fetching signed price...")
    url = "https://app-api.jp.stork-oracle.network/v1/stork_signed_prices"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Signed Price Response Status:", response.status_code)
    if response.status_code == 200:
        data = response.json()
        print("Signed Price Response:", data)
        if "data" in data:
            for key, value in data["data"].items():
                if "timestamped_signature" in value and "msg_hash" in value["timestamped_signature"]:
                    print("Extracted msg_hash:", value["timestamped_signature"]["msg_hash"])
                    return value["timestamped_signature"]["msg_hash"]
    return None

def validate_signed_price(token, msg_hash):
    print("Validating signed price...")
    url = "https://app-api.jp.stork-oracle.network/v1/stork_signed_prices/validations"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"msg_hash": msg_hash, "valid": True}
    response = requests.post(url, headers=headers, json=data)
    print("Validation Response Status:", response.status_code)
    print("Validation Response:", response.json())

def main():
    while True:
        clear_console()
        print("Starting process...")
        with open("token.txt", "r") as token_file, open("refresh.txt", "r") as refresh_file:
            tokens = token_file.read().splitlines()
            refresh_tokens = refresh_file.read().splitlines()
        
        updated_tokens = []
        for i, token in enumerate(tokens):
            print(f"Processing token {i+1}...")
            if not check_token_validity(token):
                print(f"Token {i+1} invalid, refreshing...")
                new_token = get_access_token(refresh_tokens[i])
                if new_token:
                    token = new_token
                else:
                    print(f"Failed to refresh token {i+1}")
                    continue
            updated_tokens.append(token)
            msg_hash = get_signed_price(token)
            if msg_hash:
                validate_signed_price(token, msg_hash)
        
        with open("token.txt", "w") as token_file:
            token_file.write("\n".join(updated_tokens))
        print("Process completed. Waiting 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    main()
