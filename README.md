# 🔍 WordPress Finder

A Python script that automatically searches for **WordPress** sites in the `.ru` zone via **Google Custom Search API**,  
collects a list of domains, checks their **WordPress version**, detects installed **plugins** (if possible),  
and saves everything to a **CSV file**.

---

## 📌 Features

- 🔎 Searches for WordPress sites using **Google Dorks** via **Custom Search API**  
- 📂 Collects **unique domains**  
- 🆚 Detects **WordPress version** (from meta tag or `version.php`)  
- 🔌 Lists detected **plugins** and their versions  
- 💾 Saves results to a **CSV file** (`wp_sites_info.csv`)  

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/wp-finder.git
cd wp-finder
pip install -r requirements.txt
```

## 🔑 Configuration

Before running, you must set your Google Custom Search API credentials.
Without them, the search will not work.

In the script, replace:
- GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
- GOOGLE_CSE_ID = "YOUR_CSE_ID"
  
And:
- DOMAIN_ZONE = ".com"
If you want a different domain

### 1️⃣ Get GOOGLE_API_KEY

- Go to Google Cloud Console
- Create a new project (or select an existing one)
- Enable Custom Search API in APIs & Services → Library
- Go to APIs & Services → Credentials
- Create an API key
- Copy it and paste it in the script

### 2️⃣ Get GOOGLE_CSE_ID
- Go to Google Custom Search Engine
- Create a new search engine (set site:.ru or * to search everywhere)
- Open Search Engine settings
- Copy the Search engine ID
- Paste it in the script

## 📄 Example Output

CSV file format:
```
Domain,WordPress Version,Plugins
example1.com,6.3.1,contact-form-7:5.7.3; elementor:3.11.5
example2.com,5.9.3,No detected plugins
```
