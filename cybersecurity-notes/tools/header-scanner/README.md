# Header Scanner

This folder contains a Python tool for scanning HTTP security headers.

## Purpose
- Review the security headers of a URL
- Detect missing headers and information leakage

## Usage
```bash
python http_header_scanner.py
```

## Notes
- The script loads a list of URLs from `urls.txt` when available.
- Results are saved in both JSON and CSV formats.
