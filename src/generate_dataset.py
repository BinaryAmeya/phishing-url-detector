# src/generate_dataset.py
"""
Generate a synthetic phishing vs legitimate URL dataset and save as:
data/phishing_dataset.csv

CSV columns: url,label
label: 0 = legitimate, 1 = phishing

Usage (from project root):
    python src\generate_dataset.py

You can change TOTAL_COUNT, RATIO_PHISH below.
"""
import csv
import random
import os
from urllib.parse import urljoin

random.seed(42)

# Config: total rows and fraction phishing
TOTAL_COUNT = 5000
RATIO_PHISH = 0.5   # fraction that are phishing (0..1)

# Lists of known legitimate domains (common popular domains)
LEGIT_DOMAINS = [
    "google.com", "facebook.com", "youtube.com", "amazon.com", "wikipedia.org",
    "twitter.com", "linkedin.com", "github.com", "microsoft.com", "apple.com",
    "reddit.com", "stackoverflow.com", "instagram.com", "dropbox.com", "netflix.com",
    "paypal.com", "quora.com", "bing.com", "stackoverflow.com", "live.com"
]

# Common TLDs to pick from
TLDs = ["com", "net", "org", "io", "co", "info", "biz"]

# Suspicious words frequently used in phishing URLs
PHISH_KEYWORDS = ["login", "verify", "secure", "update", "account", "signin", "confirm", "bank", "ebank"]

# Path fragments for legitimate-looking pages
LEGIT_PATHS = ["", "/", "/home", "/about", "/contact", "/products", "/search?q=test", "/user/profile"]

# Typosquatting helper: insert, remove, swap, double chars
def typosquat(domain):
    # domain like 'google.com' -> operate on left label
    if not domain:
        return domain
    name, _, tld = domain.partition(".")
    ops = [
        lambda s: s + random.choice("abcdefghijklmnopqrstuvwxyz"),          # append char
        lambda s: s[:-1] if len(s) > 1 else s,                              # drop last
        lambda s: s.replace("o", "0"),                                      # homoglyph simple
        lambda s: s + "-" + random.choice(["secure","login"]),              # add suffix
        lambda s: s.replace("i", "1"),                                      # i->1
        lambda s: s[:1] + s[1:].replace(s[1], s[1]*2) if len(s)>1 else s,   # double second char
    ]
    fn = random.choice(ops)
    new = fn(name)
    return f"{new}.{tld}"


def random_subdomain(domain):
    subs = ["", "www", "secure", "login", "mail", "account", "update"]
    sub = random.choice(subs)
    if sub == "" or sub == "www":
        return domain
    return f"{sub}.{domain}"


def random_port_and_ip_style():
    # sometimes phishing uses ip addresses
    if random.random() < 0.05:
        # create IPv4 like 192.0.2.1:8080
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        if random.random() < 0.5:
            return f"http://{ip}"
        else:
            return f"http://{ip}:{random.randint(8000, 50000)}"
    return None


def make_legit_url():
    domain = random.choice(LEGIT_DOMAINS)
    # occasionally randomize tld
    if random.random() < 0.05:
        name = domain.split(".")[0]
        domain = name + "." + random.choice(TLDs)
    domain = random_subdomain(domain)
    path = random.choice(LEGIT_PATHS)
    scheme = "https" if random.random() < 0.95 else "http"
    url = f"{scheme}://{domain}{path}"
    return url


def make_phish_url():
    # Choose a phishing pattern
    pattern = random.random()
    # Pattern A: typosquatted domain
    if pattern < 0.35:
        base = random.choice(LEGIT_DOMAINS)
        d = typosquat(base)
        d = random_subdomain(d)
        path = "/" + random.choice(PHISH_KEYWORDS) + "/" + random.choice(["", "login", "user", "auth"])
        scheme = random.choice(["http", "https"])
        return f"{scheme}://{d}{path}"
    # Pattern B: legit domain in path (e.g., example.com/amazon.com/login)
    if pattern < 0.60:
        host = random.choice(["secure-login.com", "auth-update.net", "confirm-pay.info", "verify-account.co"])
        embed = random.choice(LEGIT_DOMAINS)
        path = "/" + embed + "/" + random.choice(["login", "signin", "verify"])
        scheme = random.choice(["http", "https"])
        return f"{scheme}://{host}{path}"
    # Pattern C: IP address hosting
    if pattern < 0.75:
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        path = "/" + random.choice(PHISH_KEYWORDS) + ".php"
        return f"http://{ip}{path}"
    # Pattern D: subdomain that looks like legit (paypal.example.com.attacker.com)
    if pattern < 0.9:
        legit = random.choice(LEGIT_DOMAINS).split(".")[0]
        attacker = random.choice(["secure-login", "account-update", "verify-page", "auth"])
        tld = random.choice(TLDs)
        # create domain like legit.attacker.com
        domain = f"{legit}.{attacker}.{tld}"
        path = "/" + random.choice(PHISH_KEYWORDS) + "/" + random.choice(["", "login"])
        scheme = random.choice(["http", "https"])
        return f"{scheme}://{domain}{path}"
    # Pattern E: long query parameters with suspicious keywords
    host = random.choice(["login-check.com", "account-verify.net", "securepay.info", "update-bank.co"])
    q = "?token=" + "".join(random.choice("abcdef0123456789") for _ in range(20))
    q += "&ref=" + random.choice(["email", "sms", "notification"])
    path = "/" + random.choice(PHISH_KEYWORDS)
    return f"https://{host}{path}{q}"


def generate_dataset(total=TOTAL_COUNT, ratio_phish=RATIO_PHISH):
    os.makedirs("data", exist_ok=True)
    phish_count = int(total * ratio_phish)
    legit_count = total - phish_count

    rows = []
    # generate legitimate URLs
    for _ in range(legit_count):
        url = make_legit_url()
        rows.append((url, 0))

    # generate phishing URLs
    for _ in range(phish_count):
        url = make_phish_url()
        rows.append((url, 1))

    random.shuffle(rows)
    out_path = os.path.join("data", "phishing_dataset.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "label"])
        for u, l in rows:
            writer.writerow([u, l])

    print(f"Wrote {len(rows)} rows to {out_path}")
    return out_path


if __name__ == "__main__":
    # Optionally adjust numbers here
    generate_dataset(total=TOTAL_COUNT, ratio_phish=RATIO_PHISH)
