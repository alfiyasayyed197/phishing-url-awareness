"""Local, text-only phishing URL awareness checker."""

import ipaddress
from urllib.parse import urlparse


INFO_PREFIXES = (
    "No URL entered.",
    "Could not identify a hostname.",
    "This text is not a valid URL format.",
    "No listed warning signs found.",
)


def inspect_url(raw_url: str) -> list[str]:
    """Return visible warning signs for URL text without contacting a website."""
    url = raw_url.strip()
    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url
    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
        # Accessing .port validates malformed port syntax too.
        _ = parsed.port
    except ValueError:
        return ["This text is not a valid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    findings: list[str] = []
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        findings.append("Uses an IP address instead of a familiar domain.")

    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")
    return findings


def has_warnings(findings: list[str]) -> bool:
    """Distinguish warning results from informational or invalid-input results."""
    return not findings[0].startswith(INFO_PREFIXES)


def main() -> None:
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")
    while True:
        try:
            raw_url = input("\nEnter a sample URL (or type q to quit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Stay alert online.")
            break
        if raw_url.strip().lower() in {"q", "quit", "exit"}:
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)
        print("\nResult:")
        for item in findings:
            print("- " + item)
        if has_warnings(findings):
            print(f"\nREVIEW CAREFULLY: {len(findings)} warning sign(s) found.")
        print("Never enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
