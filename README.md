# 🔍 Instagram Unfollowers Detector

> Find who doesn't follow you back on Instagram — fast and easy.

## 🌐 Try the Web App

**No installation needed!** Open the web app directly in your browser:

👉 **[Launch Web App](https://devandapratamaxcv.github.io/instagram-unfollowers-detector/)**

1. Download your Instagram data export (JSON format)
2. Upload `followers_1.json` and `following.json` to the web app
3. See results instantly — 100% in your browser, no server

## 💻 Command Line Version

If you prefer terminal:

```bash
git clone https://github.com/devandapratamaxcv/instagram-unfollowers-detector.git
cd instagram-unfollowers-detector
pip install -r requirements.txt
python instagram_unfollowers.py
```

### Two Modes

| Mode | Description |
|------|-------------|
| **[1] Login** | Enter Instagram credentials, data fetched live |
| **[2] Export** | Upload Instagram data export files, no login needed |

## 📁 Project Structure

```
instagram-unfollowers-detector/
├── docs/
│   └── index.html          ← 🌐 Web App (GitHub Pages)
├── instagram_unfollowers.py ← 💻 CLI Version
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## ✨ Features

- ❌ **Don't Follow Back** — You follow them, they don't follow you
- ⚠️ **You Don't Follow Back** — They follow you, you don't follow them
- ✅ **Mutual** — You follow each other
- 📊 **Summary Stats** — Total followers/following at a glance
- 🔍 **Search** — Find specific users instantly
- 💾 **Export** — JSON, TXT, CSV output
- 🔒 **Privacy** — 100% client-side, no data sent anywhere

## 📸 Preview

```
╔══════════════════════════════════════════════════════╗
║        🔍 Instagram Unfollowers Detector 🔍          ║
╚══════════════════════════════════════════════════════╝

  📊 RESULTS SUMMARY
  ───────────────────────────────
  Total Followers : 1,250
  Total Following :   890
  Mutual          :   820
  No Follow Back  :    70
  You Don't Follow:   430

  ❌ DON'T FOLLOW BACK (70 users):
    1. @someuser
    2. @anotheruser

  ⚠️  YOU DON'T FOLLOW BACK (430 users):
    1. @celeb_account
```

## 📄 License

MIT License

---

Made with ❤️ by [devandapratamaxcv](https://github.com/devandapratamaxcv)
