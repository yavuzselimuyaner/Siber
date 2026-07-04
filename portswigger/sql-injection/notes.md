# PortSwigger - Server-Side Vulnerabilities Notes

## Overview
This note summarizes the PortSwigger learning path for server-side vulnerabilities, with a focus on SQL injection and related web security topics.

## 1. Path Traversal
Path traversal (also known as directory traversal) allows an attacker to access arbitrary files on the server. If the vulnerability also allows writing, attackers may modify application files or data and potentially gain full control.

### Key ideas
- Read sensitive files such as configuration and source files
- Abuse URL parameters or file-handling inputs
- Use traversal sequences such as `../` to navigate outside the intended directory
- In some cases, combine traversal with file upload or web shell deployment for deeper impact

### Common examples
- `/image?filename=../../../../../etc/passwd`
- `/download?file=../../app/config.php`
- `/view?path=..%2f..%2f..%2fvar/www/html/config.php`

### Practical impact
- Steal credentials, API keys, and application secrets
- Read source code to identify logic flaws
- Abuse write access to plant a web shell or modify content

### Learning path
- What is path traversal?
- Reading arbitrary files via path traversal
- Lab: File path traversal, simple case

## 2. Access Control
Access control is the mechanism that ensures users can only interact with resources and features they are authorized to use.

### Key ideas
- Broken access control can expose sensitive functionality or data
- Common types include vertical and horizontal privilege escalation
- Attackers may exploit weak checks in URLs, parameters, or session-based logic
- Insecure direct object references (IDOR) are a common pattern

### Common examples
- Changing a request parameter from `userId=2` to `userId=1`
- Accessing `/admin` when the application should require elevated privilege
- Bypassing client-side checks that only hide the UI

### Practical impact
- Read or modify someone else’s data
- Escalate from normal user to admin
- Expose hidden functionality or administrative interfaces

### Learning path
- What is access control?
- Vertical privilege escalation
- Unprotected functionality
- Lab: Unprotected admin functionality
- Unprotected functionality - Continued
- Lab: Unprotected admin functionality with unpredictable URL
- Parameter-based access control methods
- Lab: User role controlled by request parameter
- Horizontal privilege escalation
- Lab: User ID controlled by request parameter, with unpredictable user IDs
- Horizontal to vertical privilege escalation
- Lab: User ID controlled by request parameter with password disclosure

## 3. Authentication
Authentication verifies that a user is really who they claim to be.

### Key ideas
- Weak authentication can be bypassed through brute-force or enumeration
- Two-factor authentication can be bypassed if the implementation is flawed
- Attackers often rely on response differences and predictable logic
- Poor password reset flows and session handling often create additional weaknesses

### Common examples
- Username enumeration by observing different error messages
- Password spraying or brute-force with wordlists
- Bypassing 2FA via session manipulation or logic flaws

### Practical impact
- Account takeover
- Access to private data and admin functionality
- Further pivoting into internal systems or business logic abuse

### Learning path
- Authentication vulnerabilities
- Difference between authentication and authorization
- Brute-force attacks
- Brute-forcing usernames
- Brute-forcing passwords
- Brute-forcing passwords - Continued
- Username enumeration
- Lab: Username enumeration via different responses
- Bypassing two-factor authentication
- Lab: 2FA simple bypass

## 4. Server-Side Request Forgery (SSRF)
SSRF vulnerabilities let an attacker cause the server to make requests to unintended internal URLs.

### Key ideas
- The server acts as a trusted client to other systems
- Attackers may access internal services or metadata endpoints
- SSRF is especially dangerous in internal networks
- Some applications allow interaction with localhost, private IP ranges, or cloud metadata endpoints

### Common examples
- `http://127.0.0.1/admin`
- `http://169.254.169.254/latest/meta-data/`
- `http://internal-service:8080/health`

### Practical impact
- Read internal resources and APIs
- Enumerate internal services
- Abuse trusted server access to pivot deeper into the infrastructure

### Learning path
- What is SSRF?
- SSRF attacks against the server
- SSRF attacks against the server - Continued
- Lab: Basic SSRF against the local server
- SSRF attacks against other back-end systems
- Lab: Basic SSRF against another back-end system

## 5. File Upload Vulnerabilities
File upload features are dangerous if they do not enforce strict validation.

### Key ideas
- Attackers may upload malicious scripts or web shells
- File type validation can be bypassed with content tricks
- A successful upload may lead to remote code execution
- Web shells are often written in PHP, JSP, ASPX, or similar server-side languages

### Common examples
- Uploading a PHP file such as `shell.php` containing `<?php system($_GET['cmd']); ?>`
- Changing the file extension or content type to bypass checks
- Uploading a file that is later executed by the web server

### Practical impact
- Remote code execution
- Full compromise of the application host
- Persistence, data theft, and lateral movement

### Learning path
- What are file upload vulnerabilities?
- How do file upload vulnerabilities arise?
- Exploiting unrestricted file uploads to deploy a web shell
- Lab: Remote code execution via web shell upload
- Exploiting flawed validation of file uploads
- Flawed file type validation
- Flawed file type validation - Continued
- Lab: Web shell upload via Content-Type restriction bypass

## 6. OS Command Injection
Command injection allows an attacker to execute operating system commands on the server.

### Key ideas
- The application passes attacker input into shell commands
- Attackers may chain commands or inject separators
- Success can lead to full server compromise
- Common payloads use shell metacharacters like `&&`, `;`, `|`, or backticks

### Common examples
- `127.0.0.1; whoami`
- `127.0.0.1 && cat /etc/passwd`
- `127.0.0.1 | ls`
- `127.0.0.1$(whoami)`

### Practical impact
- Read files, enumerate users, and steal secrets
- Execute arbitrary commands and install persistence
- Combine with file upload or web shell deployment for deeper access

### Learning path
- What is OS command injection?
- Useful commands
- Injecting OS commands
- Injecting OS commands - Continued
- Lab: OS command injection, simple case

## 7. SQL Injection
SQL injection is a classic vulnerability where attacker input changes the SQL query executed by a database.

### Core concepts
- User-controlled input is embedded directly into SQL queries
- Weak input validation and poor escaping enable exploitation
- Common payloads include UNION-based, boolean-based, and error-based injection
- Different database engines need different syntax, such as MySQL, PostgreSQL, MSSQL, and Oracle

### Common examples
- `OR 1=1--`
- `' UNION SELECT username, password FROM users-- -`
- `admin'--`
- `1' AND 1=1--`

### Practical impact
- Read hidden data from arbitrary tables
- Bypass login logic and authentication checks
- Exfiltrate sensitive information or modify records when write access exists

### Useful notes
- Simple bypasses such as `or 1=1` can be useful during early testing
- Different responses may reveal hidden data or database structure
- Identifying the database type helps choose the right payloads
- In PHP applications, SQLi often appears alongside weak input handling and poor prepared statements

### Learning path
- What is SQL injection (SQLi)?
- How to detect SQL injection vulnerabilities
- Retrieving hidden data
- Retrieving hidden data - Continued
- Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
- Subverting application logic
- Lab: SQL injection vulnerability allowing login bypass

## Useful tools
- Burp Suite
- Burp Intruder for brute-force and automation
- Burp Scanner for vulnerability discovery
- Browser developer tools for inspecting requests and responses

## General study tips
- Always test for both read and write impact
- Check whether a vulnerability can be chained with another issue
- Think about how a bug can lead to privilege escalation, code execution, or data exposure
- Practice the same concept across multiple languages and stacks, including PHP, Java, ASP.NET, and Node.js

## References
- PortSwigger Web Security Academy
- Burp Suite documentation and release notes
