# Request Smuggling - CL-TE

## Summary
A mismatch between Content-Length (CL) and Transfer-Encoding (TE) headers can confuse the server-side parser and lead to request smuggling.

## Core Logic
- CL tells the server where one request body ends.
- TE may instruct the server to interpret a chunked body differently.
- When two components interpret the request differently, a subsequent request can be processed in an unintended way.

## Notes
- Header correctness must be validated carefully.
- A single malformed request structure can trigger smuggling in a lab environment.
- Comparing behavior across different servers or intermediaries is often necessary.
