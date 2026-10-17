# Toolkit session authentication — initial #198 increment

Base: d39ff18. Execute inline; no publishing or subagents. Approved design:
`/workspace/work/native-auth-design.md`. Existing native HTML login stays unchanged.

1. Write and observe failing real-CSRF tests for public JSON discovery, native-login
   subclass form POST, generic denials, quota sharing, session/CSRF rotation, expiry,
   logout, safe profile projection and route/method policies.
2. Add a thin facade over CustomLoginView/LogoutView with inherited protections,
   explicit form/content-type validation and shared login throttle. Add read-only
   discovery and safe authenticated session metadata; no JWT or credential logging.
3. Verify all API/native auth/policy/action/import guards, format/lint, document
   contract and limitations. Run full suite with authorized external browser exclusion.
4. Obtain controller-coordinated review, resolve findings with regressions, commit
   cleanly and report. Native Rust login/keyring/UI remain a separate increment.
