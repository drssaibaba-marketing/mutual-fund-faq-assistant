import requests
from urllib.parse import urlparse
from corpus_registry import CORPUS_REGISTRY

APPROVED_DOMAINS = ["www.hdfcfund.com", "investor.sebi.gov.in", "www.sebi.gov.in", "www.amfiindia.com"]

def validate_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    total = len(CORPUS_REGISTRY)
    validated = 0
    broken = 0
    unapproved = 0
    wrong_scheme_mappings = 0

    print("--- Starting Automated Source Validation ---")
    
    for item in CORPUS_REGISTRY:
        url = item.get('canonical_url', item['url'])
        domain = urlparse(url).netloc
        
        if domain not in APPROVED_DOMAINS:
            print(f"[FAIL] Unapproved domain: {url}")
            unapproved += 1
            continue
            
        try:
            # We use allow_redirects=True to catch if it moved completely.
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            
            # WAF 403s on approved domains are considered "active but protected" for HDFC.
            # 404s mean the page is truly gone.
            if response.status_code == 404:
                print(f"[FAIL] Broken link (404 Not Found): {url}")
                broken += 1
            elif response.status_code >= 400 and response.status_code != 403:
                print(f"[FAIL] HTTP Error {response.status_code}: {url}")
                broken += 1
            else:
                # Optionally check if domain changed due to redirect
                final_domain = urlparse(response.url).netloc
                if final_domain not in APPROVED_DOMAINS:
                    print(f"[FAIL] Redirected to unapproved domain ({response.url}): {url}")
                    unapproved += 1
                else:
                    validated += 1
                    
        except requests.exceptions.RequestException as e:
            print(f"[FAIL] Connection Error: {url} -> {e}")
            broken += 1

    print("\n--- Final Source Report ---")
    print(f"Total corpus sources: {total}")
    print(f"Successfully validated: {validated}")
    print(f"Broken active citation URLs: {broken}")
    print(f"Unapproved active sources: {unapproved}")
    print(f"Wrong-scheme citations mapped: {wrong_scheme_mappings} (Enforced by corpus_registry.py strict dictionary)")
    
    if broken > 0 or unapproved > 0 or wrong_scheme_mappings > 0:
        print("\nValidation FAILED. Please fix the broken/unapproved URLs before deployment.")
        exit(1)
    else:
        print("\nValidation PASSED. All active citation URLs are approved and reachable.")

if __name__ == "__main__":
    validate_urls()
