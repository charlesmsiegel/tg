# Authentication through cache failures (#1594, #1546)

Use Django cached_db sessions so Redis accelerates reads while the database retains
sessions. Fail closed for login, signup and password reset whenever counting fails;
keep existing sessions usable and log cache failures through the configured tg logger.
Trust forwarded addresses only from explicitly configured proxy IPs/CIDRs, walking
right to left until the first untrusted hop. None means unconfigured (deploy warning);
an explicit empty list means a direct deployment using REMOTE_ADDR.

1. Pin the failure with tests: production session/cache logging settings; session
   create/read/update with Redis-like suppressed failures; all three auth forms return
   429 on None/exception; retry an expired counter once and refuse repeated failures.
2. Replace fixed-window reset with a two-bucket weighted counter: current attempts plus
   previous attempts multiplied by the remaining fraction of the window. Keep atomic
   add/incr, retain buckets for two windows, count rejected attempts and document that
   this is an approximation, not an exact timestamp log. Test boundary bursts and expiry.
3. Add client_address(request), explicit AUTH_THROTTLE_TRUSTED_PROXIES configuration,
   IPv4/IPv6 and multi-hop/spoof tests, and deploy checks for absent/invalid proxy config.
4. Update auth/settings/deployment/logging docs and .env.example. Record that switching
   cache-only to cached_db sessions requires one login after rollout; no schema change.
5. Run focused tests with normal settings, the full suite with the established temporary
   Windows runner, changed-file hooks and repository Ruff. Review independently, commit,
   push and open a draft PR linking both issues.

Boundary: no fallback that permits uncounted auth attempts, no trust of arbitrary
X-Forwarded-For, no new cache backend or custom session implementation. New auth forms
reuse the existing mixin and all workers must share the default cache.

Review ruling: the installer enables Daphne proxy-header parsing while nginx appends
untrusted client XFF. Replace XFF with the socket client address for this single-proxy
setup and pin it with a regression. Otherwise Daphne rewrites REMOTE_ADDR before the
application can apply its trust list. Existing nginx installations need the same change.
