# Vendored browser libraries

Served as ordinary static files; there is no npm, bundler or build step.
The version is part of each path. To upgrade, vendor the new version beside
the old one, update the table and `core/templates/core/includes/interactive_scripts.html`,
and delete the old directory. `core.tests.test_htmx` recomputes each
file's SRI hash and fails if the include or this table drifts from the bytes.

| Library | File | Source (npm tarball) | npm `dist.integrity` (tarball, verified when vendored) | SRI of the file | License |
|---|---|---|---|---|---|
| htmx 2.0.11 | `htmx/2.0.11/htmx.min.js` | `htmx.org@2.0.11` `dist/htmx.min.js` | `sha512-Thx/WtpeOQqSrqBCw/A1cwGJGg4UrVa3+sW0GmrM3p4gJgO89ecH4qtbnyzDDWFvBTqjnIMCgELTNt636dtamA==` | `sha384-2OatzQy1H+Zd/IIrjr1TcuDGqLXeHhbooAyJY1KdQMKnr4LZ22k31GBLdYKHmVjg` | 0BSD (`htmx/2.0.11/LICENSE`) |
| Alpine.js CSP build 3.17.4 | `alpinejs-csp/3.17.4/cdn.min.js` | `@alpinejs/csp@3.17.4` `dist/cdn.min.js` | `sha512-SlRXmqO6kYhnxlg+99etmuzJtE9Lk4QbKjBHqerXzaMflJqoJXdz/SI3IvHJGZ/vRVyC3bR0SSBz40oY7goBeg==` | `sha384-DQd2BgbtOQrdt/JbxcM+wSb8poOHwsG5W2jbbXskj85r7SWPwqpBFgGGR1devM/D` | MIT (`alpinejs-csp/3.17.4/LICENSE`) |
| htmx `ws` extension 2.0.4 | `htmx-ext-ws/2.0.4/ws.min.js` | `htmx-ext-ws@2.0.4` `dist/ws.min.js` | `sha512-LnOpFRL/2hInhdKl/9N0OJsb4GYQ5/teUdTHNZYY9ytYdxYEqjfLEe0MWgF3ODjfwGJRb4E95igAbU66te48ZA==` | `sha384-1RwI/nvUSrMRuNj7hX1+27J8XDdCoSLf0EjEyF69nacuWyiJYoQ/j39RT1mSnd2G` | 0BSD (`htmx-ext-ws/2.0.4/LICENSE`) |

No file contains a `sourceMappingURL` comment, so Django's
`ManifestStaticFilesStorage` copies them byte-for-byte and the SRI hashes stay
valid on hashed URLs.

Why the Alpine **CSP** build: it evaluates directive expressions with its own
parser instead of `new Function`, so it needs no `'unsafe-eval'`. All components
are registered with `Alpine.data()` in static files.

The `ws` extension (scene chat, Step 11) must load after htmx; both are
`defer`, so document order is enough. Pages opt in with
`{% include "core/includes/interactive_scripts.html" with ws=True %}`.
