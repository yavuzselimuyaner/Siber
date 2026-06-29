# Web Security and Penetration Testing Cheat Sheet

## 1. Path Traversal
Path Traversal is a vulnerability that allows an attacker to read arbitrary files on the server running an application by manipulating file reading operations.

* **Critical Parameter (`../` or `..\`):** Represents the command to "step up one level in the directory structure." Even if the application uses a fixed base directory, these sequences can be used consecutively to navigate up to the filesystem root.
* **Unix / Linux Target:** `/etc/passwd` (Standard file containing registered user details)
* **Windows Target:** `\windows\win.ini` (Standard Windows file example)

### Lab Solution: Simple Path Traversal
* **Goal:** Retrieve the contents of the `/etc/passwd` file using a vulnerable product image parameter.
* **Method:** Intercepted the product image request using Burp Suite. Modified the `filename` parameter to `../../../../../../etc/passwd` to step up to the root directory and successfully read the file contents. (`GET /image?filename=../../../../../../etc/passwd HTTP/2`)

---

## 2. Access Control Vulnerabilities
Access control failures allow users to access data or functionality that falls outside their intended permissions.

### 2.1. Vertical Privilege Escalation
Occurs when a regular user gains access to functionality they are not permitted to use (e.g., a non-admin user accessing an admin panel to delete users).

### 2.2. Unprotected Functionality
Arises when sensitive pages are not protected by backend authentication/authorization checks. The application relies solely on hiding the link from the UI.

**Discovery Methods:**
1.  **Direct Browsing:** Guessing the URL and entering it directly into the browser's address bar.
2.  **Brute-force:** Scanning directories using wordlists.
3.  **Information Disclosure:** The application leaking sensitive directories (e.g., via the `robots.txt` file).

### Lab Solution: Unprotected Admin Panel (robots.txt)
* **Goal:** Find the unprotected admin panel and delete the user `carlos`.
* **Method:** Inspected the `robots.txt` file at the web root. Discovered a hidden directory (`/administrator-panel`) marked with a `Disallow:` rule intended to hide it from search engines. Navigated directly to this URL to access the unauthenticated panel and deleted the user.

### 2.3. Horizontal Privilege Escalation & IDOR
Occurs when a user is able to gain access to resources belonging to another user with the same privilege level (e.g., an employee accessing another employee's private records). 

* **IDOR (Insecure Direct Object Reference):** This vulnerability arises when an application uses user-controlled parameter values (like `?id=123`) to access resources directly without checking if the current user is authorized to access that specific resource.
* **Unpredictable IDs (GUIDs) vs. Information Disclosure:** Some applications try to prevent IDOR by using unguessable Globally Unique Identifiers (GUIDs) instead of sequential numbers. However, this is ineffective if the application leaks these GUIDs elsewhere (e.g., in user reviews, messages, or blog author profiles).

### Lab Solution: Horizontal Privilege Escalation via GUID Leak
* **Goal:** Access the account page of user `carlos` and retrieve his API key.
* **Method:** 1. Browsed the public-facing application and found a blog post authored by `carlos`.
    2. Clicked on the author's name and inspected the URL to extract his unique user ID (GUID).
    3. Logged in using standard user credentials (`wiener:peter`).
    4. Navigated to the "My Account" page (`/my-account?id=[wiener's GUID]`).
    5. Replaced `wiener`'s GUID in the URL parameter with `carlos`'s GUID. 
    6. Successfully accessed Carlos's account page and retrieved the API key.

### 2.4. Chaining Vulnerabilities: Horizontal to Vertical Privilege Escalation
A horizontal privilege escalation attack can often be weaponized into a vertical privilege escalation by targeting a more privileged user.

* **Mechanism:** An attacker uses parameter tampering (IDOR) to access another user's account page. If the attacker targets an administrator's ID, they gain access to the administrative account page.
* **Impact:** This page might disclose the administrator's password, provide a way to change it, or grant direct access to privileged functionality, thereby elevating the attacker's rights to an administrative level.

### Lab Solution: User ID Controlled by Request Parameter with Password Disclosure
* **Goal:** Retrieve the administrator's password via IDOR and use it to delete the user `carlos`.
* **Method:** 1. Logged in using standard user credentials (`wiener:peter`) and accessed the user account page.
    2. Modified the `id` parameter in the URL from `wiener` to `administrator` (`/my-account?id=administrator`).
    3. Intercepted the response using Burp Suite (or inspected the page source) and found the administrator's password populated within a masked input field.
    4. Logged out, then logged back in using the newly acquired administrator credentials.
    5. Accessed the admin panel and deleted the user `carlos`.

---

## 3. The "Security by Obscurity" Fallacy
Attempting to secure sensitive functionality by giving it an unpredictable, random, or complex URL (e.g., `/administrator-panel-yb556` instead of `/admin`). This fails because without server-side access controls, anyone who discovers the URL can access the panel.

### Client-Side Disclosure
Developers often use JavaScript to dynamically construct menus and might inadvertently leak sensitive URLs to the client. Controls like `if (isAdmin)` only prevent the button from being rendered on the screen. However, the script itself is downloaded to the browser, meaning the URL can be easily found by inspecting the Page Source (View Source).

### Lab Solution: Unpredictable Admin Panel (View Source)
* **Goal:** Find the unpredictable admin panel URL leaked in the application and delete the user `carlos`.
* **Method:** Inspected the page's source code (View Source). Found the complex admin panel URL inside a `<script>` tag, which was intended only for admins but was visible to all users. Accessed the leaked URL and successfully deleted the user.

---

## 4. Parameter-Based Access Control (User-Controllable Locations)
Some applications determine the user's access rights or role at login, and then store this information in a location that the user can control. 

**Common Storage Locations:**
* A hidden HTML field.
* A cookie (e.g., `Cookie: admin=false`).
* A preset query string parameter (e.g., `?role=1`).

**The Vulnerability:**
The application makes critical access control decisions based solely on the submitted value without proper server-side cryptographic validation. Since these locations are user-controllable, an attacker can simply modify the value (e.g., changing `admin=false` to `admin=true` or changing a role ID) to elevate their privileges and access unauthorized administrative functions.

### Lab Solution: Privilege Escalation via Forgeable Cookie
* **Goal:** Access the `/admin` panel and delete the user `carlos`.
* **Method:** Logged in using standard user credentials (`wiener:peter`). Inspected the HTTP requests (using Burp Suite or browser DevTools) and identified a session cookie explicitly defining the user's role: `Admin=false`. Modified the cookie's value to `Admin=true`. Navigated to the `/admin` endpoint, successfully bypassing the access control, and deleted the target user.
