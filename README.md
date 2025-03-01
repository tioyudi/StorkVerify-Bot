# Stork API Checker

## 🚀 About
Stork API Checker is a Python-based tool designed to validate access tokens, retrieve signed prices, and validate them using the Stork Oracle Network API.

## 🔧 Features
- Automatic token validation
- Token refresh support
- Signed price retrieval
- Proxy support (optional)
- Auto retry on failures

## 📦 Requirements
Ensure you have **Python 3.x** installed. Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## 🛠 Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/tioyudi/StorkVerify-Bot.git
   cd StorkVerify-Bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Prepare your tokens:
   - Add your **access tokens** to `token.txt` (one per line).
   - Add your **refresh tokens** to `refresh.txt` (one per line).
   - (Optional) Add proxies to `proxy.txt` (one per line) if you want to use proxy mode.

## 🚀 Usage
Run the script:
```bash
python main.py
```
You will be prompted:
- `Do you want to use proxy? (y/n):` Select `y` if you want to use proxies, or `n` to proceed without them.

## 📜 Output Example
```plaintext
[INFO] 🚀 Starting process...
[INFO] ✅ Valid Token - Email: example@gmail.com | Valid: 102 | Invalid: 0
[INFO] 📜 Signed Price Retrieved: 0x78be3ae3a48ff811b639deaff1a3f9e5b0b15163fda3ac1719878cfc304cda9d
[INFO] ✅ Validation successful!
```


## 🤝 Contributing
Feel free to fork this repo and submit pull requests to improve the project.

