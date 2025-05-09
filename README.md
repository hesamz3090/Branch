```
    ___                  _    
    | _ )_ _ __ _ _ _  __| |_  
    | _ \ '_/ _` | ' \/ _| ' \ 
    |___/_| \__,_|_||_\__|_||_|
    v1.0.0
    
    Author : Hesam Aghajani
    Contact: hesamz3090@gmail.com
    Description:  A subdomain enumeration and validation tool
```

# Branch Subdomain Finder
**Branch** is a modular and automated subdomain enumeration tool designed for reconnaissance and domain footprinting. It integrates several powerful subdomain discovery tools, generates permutations with dnsgen, and validates results using massdns. Branch helps you build a comprehensive subdomain list for a given domain—quickly and efficiently.

## Features
- Multi-tool Enumeration: Integrates tools like amass, subfinder, assetfinder, findomain, subscraper
- DNS Permutation: Uses dnsgen to generate realistic subdomain variations
- DNS Resolution: Leverages massdns for fast and accurate DNS resolution
- Live Detection: Optionally sends HTTP requests to detect which subdomains are alive
- Temporary File Management: All temp files are auto-removed after execution
- Progress Reporting: Displays status at each stage of the process (tools, dnsgen, massdns, filtering)
- Custom Timeout & Live Settings: Tune requests and performance as needed
- Fast & Clean: Designed to run quickly and cleanly on any system with the required tools installed
---

## Requirements

- Python 3.6+
- See `requirements.txt` for dependencies

---
## Installation

### Clone the repository:
```bash
git clone https://github.com/hesamz3090/branch.git
cd branch
pip install -r requirements.txt
```
Or install directly using pip (after packaging):

### Installation on Linux:
```bash
pip install .
```

## Usage

| Argument        | Type      | Default     | Description                                                                      |
|-----------------|-----------|-------------|----------------------------------------------------------------------------------|
| url             | str       | Required    | The base URL to start crawling from. Must start with http:// or https://.        |
| --timeout       | int       | 5           | Timeout in seconds for each HTTP request.                                        |
| --live          | flag      | True        | If enabled, prints real-time logs during crawling.                               |
| --format        | str       | csv         | Output format: either 'csv' or 'json'.                                           |
| --output        | str       | current dir | Directory path to save the output. If not provided, saves in the current folder. |
| -v              | flag      | —           | Displays the current version of the tool.                                        |

### Examples

```bash
moss "http://example.com"
moss python moss.py https://example.com --format json --output ./results
```
**Or**

```python
from branch import Branch
obj = Branch("http://example.com")
response_list = obj.run()
```

## Example Output

```json
[
  "https://test.example.com",
  "https://demo.example.com",
  ".."
]
```
Or
```csv
https://test.example.com
https://demo.example.com
"..."
```

---
## License

Moss is licensed under the MIT License. See the [LICENSE](https://github.com/hesamz3090/branch/blob/main/LICENSE) for more information.
