import os
import uuid
from urllib.parse import urlunparse, urlparse
from dnsgen import generate
import subprocess
import re
import requests


def normalize_url(url):
    """Normalize input URL to a consistent format"""
    parsed = urlparse(url if '://' in url else 'http://' + url)
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip('/')
    return urlunparse((parsed.scheme, netloc, path, '', '', ''))


def execute_command(command):
    """Run a shell command and return its output"""
    process = subprocess.Popen(
        [command],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    output, err = process.communicate()
    return (output + err).decode("utf-8")


def check_subdomain(string: str) -> list:
    """Extract subdomains from a string using regex"""
    sub_pattern = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(?::\d{1,5})?'
    return list(set(re.findall(sub_pattern, string)))


def is_live(url: str, timeout: int = 5) -> bool:
    """Check if a URL is live using HTTP GET request"""
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        return response.status_code < 500
    except Exception:
        return False


class Branch:
    def __init__(self, url: str, timeout=5, live=True):
        self.url = normalize_url(url)
        self.hostname = urlparse(self.url).hostname
        self.timeout = timeout
        self.live = live
        self.protocol = 'https://' if 'https' in self.url else 'http://'

    def run(self):
        print(f"[+] Starting Branch enumeration on: {self.hostname}")
        domains_path = str(uuid.uuid4()) + '.txt'
        result_path = str(uuid.uuid4()) + '.txt'
        resolver_path = 'resolvers.txt'

        # List of subdomain enumeration tools
        command_list = [
            'amass enum -d $',
            'subfinder -d $',
            'assetfinder --subs-only $',
            'subscraper -d $',
            'findomain -t $',
        ]

        temp_result_list = []
        url_list = []
        print("[*] Running subdomain enumeration tools...")
        # Run each tool and collect subdomains
        for item in command_list:
            command = item.replace("$", self.hostname)
            print(f"[+] Executing: {command}")
            command_result = execute_command(command)
            for sub in check_subdomain(command_result):
                if sub not in temp_result_list:
                    temp_result_list.append(sub)
        print(f"[✓] Total unique subdomains collected: {len(temp_result_list)}")
        print("[*] Generating permutations with dnsgen...")

        # Generate permutations using dnsgen
        for sub in temp_result_list:
            dns_gen = [item for item in generate([sub])]
            with open(domains_path, "a") as file:
                for i, domain in enumerate(dns_gen):
                    file.write(domain + '\n' if i + 1 != len(dns_gen) else domain)

        print("[✓] Permutations saved to temp file")
        print("[*] Running DNS resolution with massdns...")
        # Run massdns for DNS resolution
        mass_command = f'massdns -r \'{resolver_path}\' -t A \'{domains_path}\' -o S -w \'{result_path}\''
        execute_command(mass_command)
        print("[*] Parsing massdns results...")
        # Parse massdns output and collect valid subdomains
        with open(result_path, 'r') as file:
            domain_list = file.readlines()
            for domain in domain_list:
                domain = domain.split(' ')[0].rstrip('.')
                if self.hostname in domain:
                    temp_result_list.append(domain)

        # Cleanup temporary files
        os.remove(domains_path)
        os.remove(result_path)
        os.remove('sub_report.txt')

        print("[*] Filtering and validating subdomains...")
        # Normalize, filter, and optionally check live status
        for temp in temp_result_list:
            if self.hostname in temp:
                normalized = normalize_url(self.protocol + temp if self.protocol not in temp else temp)
                if normalized != self.url and normalized.count('.') >= 2:
                    if normalized not in url_list:
                        if not self.live or is_live(normalized, self.timeout):
                            url_list.append(normalized)

        print(f"[✓] Enumeration completed. Total valid subdomains: {len(url_list)}")
        return url_list
