from urllib.parse import urlparse
import argparse
import time
import csv
import os
import warnings
import json
from branch import Branch

# Metadata
NAME = 'Branch'
VERSION = '1.0.0'
AUTHOR = 'Hesam Aghajani'
CONTACT = 'hesamz3090@gmail.com'
URL = 'https://github.com/heasmz3090/branch'
DESCRIPTIONS = 'A subdomain enumeration and validation tool.'

# Suppress unnecessary warnings
warnings.filterwarnings("ignore")


def banner():
    print(rf"""
  ___                  _    
 | _ )_ _ __ _ _ _  __| |_  
 | _ \ '_/ _` | ' \/ _| ' \ 
 |___/_| \__,_|_||_\__|_||_|
    v{VERSION}
    
Author : {AUTHOR}
Contact: {CONTACT}
Description: {DESCRIPTIONS}
""")


def main():
    parser = argparse.ArgumentParser(description='Branch Subdomain Enumerator')
    parser.add_argument('url', help='Target base URL (e.g. example.com or https://example.com)')
    parser.add_argument('--timeout', type=int, default=5, help='Request timeout in seconds (default=5)')
    parser.add_argument('--live', action='store_true', default=False,
                        help='Only show live subdomains (default: False)')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--output', type=str, help='Output directory path (default: current directory)')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')

    args = parser.parse_args()
    banner()

    if not args.url.startswith(('http://', 'https://')):
        print("[!] Error: URL must start with http:// or https://")
        exit(1)

    start_time = time.time()

    # Create an instance of Branch and run enumeration
    branch = Branch(args.url, timeout=args.timeout, live=args.live)
    result = branch.run()

    end_time = time.time()
    duration = end_time - start_time

    print(f"\n[*] Enumeration finished. Total subdomains found: {len(result)}")
    print(f"Time taken: {duration:.2f} seconds\n")

    # Prepare output file paths
    base_name = f'branch_result_{urlparse(args.url).hostname}'
    output_dir = args.output or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    # Write output in CSV format
    if args.format == 'csv':
        csv_path = os.path.join(output_dir, base_name + '.csv')
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in result:
                writer.writerow([item])
        print(f"[✓] CSV saved to: {csv_path}")

    # Write output in JSON format
    elif args.format == 'json':
        json_path = os.path.join(output_dir, base_name + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[✓] JSON saved to: {json_path}")


if __name__ == '__main__':
    main()
