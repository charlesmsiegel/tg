# Security policy

## Supported versions

Tellurium Games is deployed from the `main` branch. Security fixes are made on `main`; there
are no separately maintained release lines.

## Reporting a vulnerability

Please report security problems privately, not in a public issue or pull request:

- Use GitHub's private vulnerability reporting for this repository
  ([Security → Report a vulnerability](https://github.com/charlesmsiegel/tg/security/advisories/new)),
  or
- contact the maintainer, [@charlesmsiegel](https://github.com/charlesmsiegel), through GitHub
  and ask for a private channel.

Include what you found, how to reproduce it (the URL, the account role you used, and the
request), and what an attacker could do with it. Do not access other people's data beyond
what is needed to show the problem, and do not run tests that degrade the service.

You should get an acknowledgement within a week. Once a fix is released, the report can be
credited if you wish.

## Scope

In scope: the application code in this repository, including access control (route policies,
object permissions, visibility of chronicles, scenes and characters), authentication and
sessions, cached pages, uploads, and the WebSocket scene chat.

Out of scope: problems that need a compromised administrator or server account,
denial-of-service by volume, and vulnerabilities in third-party dependencies that are already
public (report those upstream; the pinning policy is in
[`requirements.txt`](requirements.txt)).

## For operators

How the application is secured in production (settings, cookies, headers, sessions,
authorization, uploads) is described in
[`docs/operations/security.md`](docs/operations/security.md).
