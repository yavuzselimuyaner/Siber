# Authentication Vulnerabilities Cheat Sheet

## 1. What Authentication Means
Authentication is the process of proving that a user is really who they claim to be. It is different from authorization, which decides what that user is allowed to do after they are authenticated.

* **Authentication:** "Are you really this user?"
* **Authorization:** "What can this user access?"

A weak authentication flow can lead to account takeover, data exposure, and access to sensitive features.

---

## 2. Common Authentication Mechanisms
Web applications commonly rely on several authentication methods:

* **Password-based login**
* **Multi-factor authentication (MFA/2FA)**
* **Password reset and recovery flows**
* **Session-based authentication**

Even when the login design is simple, implementation mistakes can create major security issues.

---

## 3. Brute-Force Attacks
A brute-force attack uses repeated login attempts to guess valid credentials.

### How it works
* Attackers try many usernames and passwords, often using wordlists.
* They may also use patterns, leaked data, or common password habits.
* Password-based systems are especially risky when they lack rate limits or lockout controls.

### Why it is effective
Users often choose predictable passwords, such as:

* A base word with a number or symbol added
* A variation of a previous password
* A password that follows a simple policy pattern

This makes brute-force attacks more efficient than random guessing.

---

## 4. Username Enumeration
Username enumeration happens when the application reveals whether a username exists.

### Typical signals
* The application says "Invalid username" versus "Incorrect password"
* Registration forms reveal that a username is already taken
* Error messages or response behavior differ depending on the input

### Impact
If attackers can identify valid usernames, they can focus their password attacks on a smaller set of targets.

---

## 5. Password Attacks and Weak Password Policies
Weak password policies make credential attacks easier.

### Common issues
* Passwords are too short
* No guidance on password strength
* Users can reuse passwords across sites
* Password rotation rules encourage predictable changes

### Practical note
Attackers do not only rely on random combinations. They often exploit user behavior and common password patterns.

---

## 6. Two-Factor Authentication (2FA)
2FA adds a second verification step, usually through a code sent by email, SMS, or an authenticator app.

### Why it helps
It reduces the impact of password theft because an attacker still needs the second factor.

### Common weaknesses
* The application does not properly verify the second step
* The session or account state is trusted too early
* The verification check can be bypassed by changing the request flow

### Key takeaway
2FA is only secure when the implementation enforces the second step properly.

---

## 7. Lab Notes

### Lab: Username Enumeration via Different Responses
A vulnerable login page reveals different error messages depending on whether the username or password is wrong. This allows an attacker to discover a valid username first, then brute-force the password.

### Lab: 2FA Simple Bypass
A login flow that asks for a second authentication factor can be bypassed if the application trusts the wrong state or allows access to the account page without completing the verification step.

---

## 8. Testing Checklist
When reviewing authentication, check for:

* Different responses for valid versus invalid usernames
* Weak or missing rate limiting
* Predictable usernames or account creation behavior
* Weak password policies
* Bypass paths in MFA/2FA flows
* Session handling issues that allow account takeover

---

## 9. Key Takeaway
Authentication vulnerabilities are dangerous because they often lead directly to account compromise. Even a small flaw in the login or verification process can give an attacker access to sensitive data and privileged actions.

---

## 10. SSRF Against Internal Back-end Systems
Server-Side Request Forgery (SSRF) can allow an attacker to make the application server request internal-only services that are not directly reachable by external users. These back-end systems often sit on private, non-routable IP addresses and may expose sensitive functionality without strong authentication.

Example: if an administrative interface exists at `http://192.168.0.68/admin`, an attacker can abuse an SSRF vulnerability by submitting a request like:

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://192.168.0.68/admin
```

This causes the vulnerable server to fetch the internal admin page on the attacker's behalf, potentially exposing administrative functionality or sensitive data.

Mitigations:
- Validate and whitelist outbound URLs or hosts the application may fetch.
- Avoid allowing user-controlled input to form origin URLs for server-side requests.
- Restrict the server's network egress rules to only required destinations.
- Perform DNS resolution checks and block private or loopback IP ranges when resolving user-supplied hosts.
- Use an internal proxy with strict allowlists and logging for any required outbound requests.

Reference: SSRF risks are amplified when internal services trust the network perimeter; assume zero trust and authenticate and authorize internal endpoints.
