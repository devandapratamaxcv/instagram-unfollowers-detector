# 🔍 Instagram Unfollowers Detector

> Find out who doesn't follow you back on Instagram — fast and easy.

## ✨ Features

- ❌ **Don't Follow Back** — You follow them, but they don't follow you
- ⚠️ **You Don't Follow Back** — They follow you, but you don't follow them
- ✅ **Mutual** — You follow each other
- 📊 **Summary** — Total followers/following at a glance
- 💾 **Export** — JSON, TXT, and CSV output

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/devandapratamaxcv/instagram-unfollowers-detector.git
cd instagram-unfollowers-detector

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python instagram_unfollowers.py
```

You'll be asked to choose a method:

### Method 1: Login via Instagram (Live Data)

- Enter your **Instagram username**
- Enter your **password** (stored locally, never sent anywhere else)
- The script fetches your followers & following automatically
- ⚠️ Instagram may ask for 2FA/email verification

### Method 2: Instagram Data Export (No Login)

1. Go to **Instagram** → **Settings** → **Privacy and Security** → **Download Your Data**
2. Choose **JSON** format
3. Wait for the email from Instagram
4. Download & extract to `~/Downloads/instagram-export/`
5. Run the script and choose **[2]**

## 📁 Output Files

All results are saved to `~/instagram-unfollowers/results/`:

| File | Description |
|------|-------------|
| `unfollowers_*.json` | Full data (structured) |
| `unfollowers_*.txt` | Human-readable report |
| `no_follow_back_*.csv` | No follow-back list with profile URLs (open in Excel) |

## 📸 Preview

```
╔══════════════════════════════════════════════════════╗
║        🔍 Instagram Unfollowers Detector 🔍          ║
╚══════════════════════════════════════════════════════╝

  📊 RESULTS SUMMARY
  ───────────────────────────────
  Total Followers : 1250
  Total Following :  890
  Mutual          :  820
  No Follow Back  :   70
  You Don't Follow:  430

  ❌ DON'T FOLLOW BACK (70 users):
    1. @someuser
    2. @anotheruser
    ...

  ⚠️  YOU DON'T FOLLOW BACK (430 users):
    1. @celeb_account
    ...
```

## ⚠️ Notes

- **Rate Limiting**: Instagram may temporarily block you if you fetch large lists quickly. The script has built-in delays (0.5s per request).
- **Session Caching**: After first login, session is saved to `~/.instaloader/` so you don't need to log in every time.
- **Security**: Your password is only sent to Instagram's servers via instaloader. It's never stored by this script.

## 🛠️ Dependencies

- [instaloader](https://github.com/instaloader/instaloader) — Instagram data extraction

## 📄 License

MIT License — use it however you want.

---

Made with ❤️ by [devandapratamaxcv](https://github.com/devandapratamaxcv)
