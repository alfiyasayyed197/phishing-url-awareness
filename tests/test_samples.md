# Test Results

Python version used: 3.12.14 | Operating system: Windows | Date: 2026-10-29

All inputs below are the reserved sample strings specified in the workbook. The checker only inspects text and makes no network requests.

| # | Input | Expected result | Actual result | Pass/Fail |
|---|-------|-----------------|---------------|-----------|
| 1 | `https://www.example.com/login` | No listed warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | `http://192.0.2.10/account` | IP address + HTTP | Uses an IP address instead of a familiar domain; Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | `http://example.com@sample.invalid/login` | @ symbol + HTTP | Contains an @ symbol; inspect carefully; Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Many hostname segments | Contains many hostname segments/subdomains. | PASS |
| 5 | `https://xn--example.invalid/` | Punycode-style hostname | Contains a punycode-style hostname. | PASS |

## Additional checks

| Input | Actual result | Result |
|-------|---------------|--------|
| Empty input | No URL entered. | PASS |
| `http://[bad` | This text is not a valid URL format. | PASS |
| `http://example.invalid/` followed by a path longer than 100 characters | Long URL warning and HTTP warning. | PASS |

## Notes

The hostname is the part that identifies the server, so the checker parses it before applying hostname checks. I learned that these warning signs are clues only: a URL with no listed signs may still be dangerous. The malformed IPv6 example also showed why parsing errors should be handled instead of crashing the program.
