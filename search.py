import requests
import time
import re
import csv
from urllib.parse import quote

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
GOOGLE_CSE_ID = "YOUR_CSE_ID"

QUERIES = [
    'inurl:/wp-content/ site:.ru',
    'inurl:/wp-includes/ site:.ru',
    'inurl:/wp-login.php site:.ru',
    'intitle:"Welcome to WordPress" site:.ru',
    'intext:"powered by WordPress" site:.ru',
    'inurl:/xmlrpc.php site:.ru',
    'inurl:/wp-json/ site:.ru',
    'inurl:/wp-admin/ site:.ru',
    'inurl:/wp-comments-post.php site:.ru',
    'inurl:/wp-cron.php site:.ru'
]

OUTPUT_FILE = 'wp_sites_info.csv'

def google_search(query, api_key, cse_id, start=1):
    """Perform a Google Custom Search query."""
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'start': start
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[!] Google error {resp.status_code}: {resp.text}")
            return {}
        return resp.json()
    except requests.RequestException as e:
        print(f"[!] Connection error to Google API: {e}")
        return {}

def collect_domains():
    """Collect domains from Google search results."""
    all_sites = set()
    for query in QUERIES:
        print(f"\n🔍 Searching: {query}")
        for start in range(1, 91, 10):
            print(f'[+] Fetching results {start}–{start+9}...')
            data = google_search(query, GOOGLE_API_KEY, GOOGLE_CSE_ID, start)
            items = data.get('items', [])
            if not items:
                print("[!] No data or search limit reached.")
                break
            for item in items:
                link = item.get('link')
                if link:
                    try:
                        domain = link.split('/')[2]
                        all_sites.add(domain)
                    except IndexError:
                        continue
            time.sleep(1.2)
    return all_sites

def get_wp_version(domain):
    """Try to detect the WordPress version from the site."""
    try:
        for protocol in ['http', 'https']:
            url = f"{protocol}://{domain}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                match = re.search(r'<meta name="generator" content="WordPress (\d+\.\d+\.\d+)"', resp.text)
                if match:
                    return match.group(1)
                version_url = f"{url}/wp-includes/version.php"
                resp_version = requests.get(version_url, timeout=5)
                if resp_version.status_code == 200:
                    version_match = re.search(r'\$wp_version\s*=\s*[\'"]([\d.]+)[\'"]', resp_version.text)
                    if version_match:
                        return version_match.group(1)
    except Exception as e:
        print(f"[!] Error checking version for {domain}: {e}")
    return None

def get_plugins(domain):
    """Extract plugin names and versions from site source."""
    try:
        for protocol in ['http', 'https']:
            url = f"{protocol}://{domain}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                scripts = re.findall(r'<script[^>]+src="[^"]*/wp-content/plugins/([^/]+)/[^"]*\?ver=([^"]+)"', resp.text)
                links = re.findall(r'<link[^>]+href="[^"]*/wp-content/plugins/([^/]+)/[^"]*\?ver=([^"]+)"', resp.text)
                plugins = {}
                for plugin, version in scripts + links:
                    plugins[plugin] = version
                return plugins
    except Exception as e:
        print(f"[!] Error checking plugins for {domain}: {e}")
    return {}

def main():
    domains = collect_domains()
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Domain', 'WordPress Version', 'Plugins'])
        for domain in sorted(domains):
            version = get_wp_version(domain)
            if version:
                plugins = get_plugins(domain)
                plugins_str = '; '.join([f"{p}:{v}" for p, v in plugins.items()]) if plugins else 'No detected plugins'
                writer.writerow([domain, version, plugins_str])
                print(f"[+] Found WP site: {domain} (v{version}) with plugins: {plugins_str}")
            else:
                print(f"[-] {domain} is not a WP site or version not detected.")
    print(f"\n[✓] Results saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
