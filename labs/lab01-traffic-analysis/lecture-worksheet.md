# L15 worksheet — DNS and email security

These are fictional summaries, not live DNS or mail validation outputs.

1. A validating resolver receives an A RRset and RRSIG; DNSKEY and parent DS are available. Explain how the trust anchor and parent DS establish trust in the child key, what is authenticated, and whether DNSSEC encrypts queries. A tampered RRset fails signature validation: should it be treated as authenticated?
2. A message has From: alice@lab.test, envelope sender bounce@other.test, SPF pass for other.test, DKIM pass for lab.test. Under strict alignment, which mechanism can satisfy DMARC? Repeat when DKIM fails. Explain why SPF pass alone is not enough in the latter case.
3. Compare STARTTLS hop protection with S/MIME message protection. Explain what DANE adds to TLS server authentication and why validated DNSSEC matters.
