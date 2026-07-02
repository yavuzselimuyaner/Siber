# Port Scanner

This folder contains a simple TCP port scanner written in Python.

## Purpose
- Identify open ports on a target host
- Serve as a lightweight scanning utility for basic network assessment

## Usage
```bash
python port_scanner.py --host 127.0.0.1 --start 1 --end 100
```

## Notes
- The script writes results to `results.json` by default.
- It can later be extended with threading or more advanced scanning logic.
