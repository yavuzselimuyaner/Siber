# Request Smuggling - TE-CL

## Summary
TE-CL occurs when one component uses Transfer-Encoding while another uses Content-Length, resulting in inconsistent request parsing.

## Main Idea
- A proxy or server may prioritize TE while another component follows CL.
- This mismatch can cause the next request to be interpreted incorrectly.

## Important Considerations
- Header order and duplicated values should be inspected carefully.
- A broken chunked body structure can alter the request boundary.
- Comparing both sides of the request flow is essential.
