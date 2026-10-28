"""flawpath skills 34-50: confirm, harden and document phases."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "clean-state-reproduction",
        "title": "Clean-State Reproduction",
        "summary": "Reproduce an observation from a fresh record and an empty cache, so a reviewer can replay it without inheriting the state your earlier probes created",
        "use_when": "an observation must be handed to an owner or reviewer who will replay it elsewhere",
        "avoid_when": "the behaviour is deterministic and cannot depend on prior state, which a repeat already proved",
        "tags": ["confirm", "reproduction", "method"],
        "steps": [
            "Identify every store that could remember your earlier requests: record state, caches, rate limiters and idempotency keys.",
            "State which must be empty before step one and how a reader clears or avoids each.",
            "Use a fresh synthetic record and a fresh key for each run so no run inherits another's state.",
            "Write the request sequence in order, including waits, so it can be replayed without interpretation.",
            "Record the status and the observable outcome for each step so a reader can tell a match from a divergence.",
            "Package the recipe with the observation and mark any step that cannot be replayed outside your session.",
        ],
        "signals": [
            "The reproduction succeeds on your machine but fails for a reviewer with a warm cache",
            "The first request of a session behaves differently from every later one",
            "A step has no recorded outcome, leaving the state at that point ambiguous",
            "The recipe depends on a record or key created by an earlier probe",
        ],
        "patterns": [
            (
                "Recipe block",
                "precondition: cache empty, fresh record R1\n1. POST create key K1 -> record status\n2. PATCH unknown field -> record status\n3. GET R1 -> record full field set\nrecord every outcome",
            ),
            (
                "Fresh-key rule",
                "each run uses a new record and a new idempotency key, suffixed with the run number, so no run inherits another's state",
            ),
            (
                "Assumption list",
                "if a step cannot be replayed outside your session, write it as an environment assumption rather than presenting it as deterministic",
            ),
        ],
        "pitfalls": [
            "Writing a reproduction that silently relies on state your earlier probe created",
            "Omitting the empty-store precondition, so a reviewer sees a different result and reports a false negative",
            "Presenting an environment-dependent sequence as though it were deterministic",
        ],
        "done_when": [
            "A numbered recipe lists every request with its outcome and the stores that must be empty first",
            "The recipe reproduces in a fresh context without relying on state from earlier runs",
        ],
        "refs": [
            "[PortSwigger - Writing reproducible reports](https://portswigger.net/web-security)",
            "[NIST - Evidence handling guidance](https://csrc.nist.gov/publications/detail/sp/800-86/final)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "single-input-attribution",
        "title": "Single-Input Attribution",
        "summary": "Prove that exactly one input caused the observed outcome by replaying with only that input changed, because a multi-field request cannot support a causal claim",
        "use_when": "a probe changed several inputs at once and the report needs to say which one mattered",
        "avoid_when": "the original probe already varied exactly one input",
        "tags": ["confirm", "attribution", "method"],
        "steps": [
            "List every input the original request changed relative to its baseline.",
            "Replay with all inputs at baseline except one candidate, which is the only value you vary.",
            "Record whether the outcome reproduces; if not, move to the next candidate.",
            "Continue until one input alone reproduces the outcome or none does.",
            "When none alone reproduces it, record that the effect is combinatorial rather than picking a single cause.",
            "Write the attribution as one input with its replay result, or as a combination with the members named.",
        ],
        "signals": [
            "A request changed three fields and the report attributes the effect to one of them without a replay",
            "No single input reproduces the effect when tested alone",
            "The attribution rests on which field seemed most plausible",
            "A baseline replay was never performed against the original request",
        ],
        "patterns": [
            (
                "Attribution replay",
                "original: {a:1, b:2, c:3} -> outcome\nreplay: {a:1, base, base} -> outcome reproduced -> a is the cause",
            ),
            (
                "Combinatorial case",
                "no single input reproduces it -> record the combination, name its members, and say the effect requires them together",
            ),
            (
                "Baseline-first rule",
                "always replay the baseline first to confirm the outcome was not incidental to the environment",
            ),
        ],
        "pitfalls": [
            "Naming a cause because it looks most plausible rather than because it reproduces the effect",
            "Stopping at the first input that correlates instead of testing each in isolation",
            "Never replaying the baseline, so an environmental change could explain the outcome",
        ],
        "done_when": [
            "Exactly one input, or a named combination, is recorded with the replay that isolates it",
            "A baseline replay confirms the outcome was not environmental",
        ],
        "refs": [
            "[NIST - Evidence-based assessment practice](https://csrc.nist.gov/publications/detail/sp/800-86/final)",
            "[OWASP - Testing methodology](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "response-differential-comparison",
        "title": "Response Differential Comparison",
        "summary": "Compare the full response against a baseline capture field by field, so the reported difference is the one that exists rather than the one that caught your eye",
        "use_when": "a probe produced a response and the report needs an exact statement of what differs",
        "avoid_when": "the response is a simple status with no body structure to compare",
        "tags": ["confirm", "comparison", "evidence"],
        "steps": [
            "Capture a baseline response with every input at its normal value, including headers and timing.",
            "Capture the probe response under identical conditions except for the single varied input.",
            "Diff both captures field by field across status, headers and every body field.",
            "Record every difference found, not only the one you were looking for.",
            "Attribute each difference to the varied input, or mark it as unattributed and re-test it.",
            "Store both captures so a reviewer can repeat the comparison themselves.",
        ],
        "signals": [
            "Only the expected difference was reported while a second one went unrecorded",
            "The baseline and the probe capture came from different sessions or environments",
            "Headers were not compared even though a header changed",
            "An unattributed difference was dropped rather than re-tested",
        ],
        "patterns": [
            (
                "Diff record",
                "baseline: status 200, field set {a,b,c}, header x-1\nprobe:    status 200, field set {a,b,d}, header x-2\ndifferences: c removed, d added, x changed",
            ),
            (
                "Full-field rule",
                "report every difference the diff finds; an unremarked second difference is often the more interesting one",
            ),
            (
                "Re-test loop",
                "any difference you cannot attribute to the varied input gets its own single-input replay rather than being discarded",
            ),
        ],
        "pitfalls": [
            "Reporting only the expected difference and letting a second one pass unnoticed",
            "Comparing captures taken under different conditions, which introduces noise into the claim",
            "Discarding an unattributed difference instead of testing it separately",
        ],
        "done_when": [
            "Baseline and probe captures are diffed field by field with every difference recorded",
            "Each difference is attributed to an input or re-tested on its own",
        ],
        "refs": [
            "[NIST - Evidence handling guidance](https://csrc.nist.gov/publications/detail/sp/800-86/final)",
            "[OWASP - Testing methodology](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "precondition-and-effect-statement",
        "title": "Precondition and Effect Statement",
        "summary": "State what an attacker would already need and what changes once they have it, because a defect that requires an existing privilege is a different finding from one that needs none",
        "use_when": "a confirmed observation is ready to be written up and its severity has not been argued",
        "avoid_when": "the observation is a configuration note with no behavioural consequence",
        "tags": ["confirm", "impact", "severity"],
        "steps": [
            "List the precondition: authentication, a role, a valid identifier, or nothing at all.",
            "State the effect in terms of what changes in the system, not in adjectives.",
            "State what remains impossible even with the behaviour, so the reader sees the claim's boundary.",
            "Separate defects with different preconditions into different statements rather than merging them.",
            "Rank against a recognized class such as mass assignment, resource exhaustion or information disclosure, with a reason.",
            "Write the paragraph a reviewer would accept: precondition, effect, boundary, class, nothing beyond it.",
        ],
        "signals": [
            "The impact statement is an adjective list with no precondition named",
            "Severity is stated without saying what an attacker must already possess",
            "The statement does not say what the behaviour cannot achieve",
            "Two defects with different preconditions are merged into one claim",
        ],
        "patterns": [
            (
                "Impact skeleton",
                "precondition: <what the caller must already have>\neffect: <what changes in the system>\nboundary: <what remains impossible>\nclass: <mass assignment | resource exhaustion | disclosure | workflow>",
            ),
            (
                "Worked example",
                "precondition: authenticated member with an update grant; effect: an undeclared field is stored and read back by later queries; boundary: no cross-tenant read is possible; class: mass assignment",
            ),
            (
                "Split rule",
                "if two observations have different preconditions, write two statements; merging them hides the difference a triager needs",
            ),
        ],
        "pitfalls": [
            "Claiming critical severity for behaviour that already requires an existing grant",
            "Omitting the boundary, which makes a reviewer trust the claim less rather than more",
            "Blending an information disclosure into a state-change finding so neither can be triaged",
        ],
        "done_when": [
            "The statement names precondition, effect, boundary and class in that order",
            "Observations with different preconditions appear as separate claims",
        ],
        "refs": [
            "[OWASP - Risk rating methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)",
            "[CVSS - Qualitative severity mapping](https://www.first.org/cvss/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "environment-transferability-check",
        "title": "Environment Transferability Check",
        "summary": "Re-read the environment delta and mark each finding as transferable or not, so a defect that only exists behind a staging flag never reaches production as a claim",
        "use_when": "findings were established in one environment and are about to be reported against another",
        "avoid_when": "one environment serves all traffic and configuration is identical by construction",
        "tags": ["confirm", "environment", "reporting"],
        "steps": [
            "Re-read the environment delta table, since configuration may have changed since the assessment began.",
            "For each finding, identify which settings it depends on, if any.",
            "Mark the finding transferable, not transferable, or unknown, with the setting responsible.",
            "For unknown, state what would settle it: a reading, a test in the other environment, or an owner's answer.",
            "Re-check any finding that depended on a debug flag or a validation mode, since those differ most often.",
            "Place the transferability column beside each finding rather than in an appendix.",
        ],
        "signals": [
            "A finding's transferability was never assessed against the delta",
            "A debug-flag-dependent error shape is reported as a production behaviour",
            "Transferability is discussed once in general terms rather than per finding",
            "The delta has not been re-read since the assessment started",
        ],
        "patterns": [
            (
                "Transfer column",
                "finding | depends on setting | tested env | production | transferable\nF-01 | validation strictness | off | on | no\nF-02 | nothing | - | - | yes",
            ),
            (
                "Unknown handling",
                "unknown -> state what settles it: a config reading, a test in that environment, or an owner's written answer",
            ),
            (
                "Placement rule",
                "the column sits beside the finding so a reader meets it before acting, never in an appendix",
            ),
        ],
        "pitfalls": [
            "Assuming transferability for all findings with one sentence at the top of the report",
            "Reporting a debug-only shape as a production defect",
            "Marking a finding transferable without naming the setting it depends on",
        ],
        "done_when": [
            "Every finding has a transferability verdict with the setting responsible or a stated none",
            "Unknown verdicts state what would settle them, and the column sits beside the findings",
        ],
        "refs": [
            "[OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)",
            "[NIST SP 800-53 - Configuration settings controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "ruling-out-alternative-cause",
        "title": "Ruling Out Alternative Cause",
        "summary": "Name the other explanations for what you saw and test each one, because a finding that survives every alternative is the only kind that survives review",
        "use_when": "an observation is confirmed and at least one other cause could plausibly explain it",
        "avoid_when": "the single-input replay already rules out every plausible alternative by construction",
        "tags": ["confirm", "method", "rigour"],
        "steps": [
            "List the alternative causes: client-side caching, an environment setting, a concurrent writer, a gateway rewrite or your own tooling.",
            "For each alternative, design the one observation that would distinguish it from the finding you intend to report.",
            "Run those distinguishing observations and record the result for each.",
            "Mark each alternative ruled out with its evidence, or ruled in, which changes the finding entirely.",
            "Where an alternative cannot be ruled out with the access you have, say so plainly in the report.",
            "Keep the alternatives list with the finding, since a reviewer will ask the same questions.",
        ],
        "signals": [
            "A plausible alternative was never tested before the claim was written",
            "Your own tooling could explain the observation and was not checked",
            "An alternative was dismissed in prose rather than by an observation",
            "An untestable alternative is absent from the report as though it did not exist",
        ],
        "patterns": [
            (
                "Alternative table",
                "alternative | distinguishing test | result | verdict\nclient cache | bypass client cache | same outcome | ruled out\nstaging flag | read setting | differs from prod | ruled in, finding transferable: no",
            ),
            (
                "Unsettleable case",
                "alternative that cannot be tested with your access -> written as an open alternative in the report, not omitted",
            ),
            (
                "Own-tooling check",
                "first alternative to test is your own client, since it is both the most likely and the cheapest to rule out",
            ),
        ],
        "pitfalls": [
            "Asserting an alternative is impossible without an observation that shows it",
            "Forgetting that your own tooling may add caching, headers or retries",
            "Omitting an untestable alternative, which makes the claim look stronger than it is",
        ],
        "done_when": [
            "Every plausible alternative has a distinguishing test with a recorded result",
            "Any alternative that cannot be ruled out is stated in the report as an open one",
        ],
        "refs": [
            "[NIST - Evidence-based assessment practice](https://csrc.nist.gov/publications/detail/sp/800-86/final)",
            "[OWASP - Testing methodology](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "confirm"},
    },
    {
        "slug": "server-side-field-allowlist",
        "title": "Server-Side Field Allowlist",
        "summary": "Build the accepted field set on the server from an explicit allow-list, so a field nobody declared can never reach an assignment no matter how the parser behaves",
        "use_when": "the parser passes unknown keys through or a probe showed an undeclared field was stored",
        "avoid_when": "an explicit allow-list already governs assignment and a probe confirms rejection",
        "tags": ["harden", "mass-assignment", "validation"],
        "steps": [
            "Declare the accepted field set per endpoint explicitly, in code or schema, rather than deriving it from a model.",
            "Apply the allow-list at the assignment boundary, after parsing and before any write to state.",
            "Reject or strip anything not on the list, and record which of the two you chose and why.",
            "Include nested paths in the declaration so a dotted or bracketed key cannot reach an undeclared field.",
            "Re-run the unknown-field, privileged-field and nested-key probes against the change.",
            "Record the change location and the retest results beside it.",
        ],
        "signals": [
            "The accepted set is derived from the model, which by construction includes every persisted field",
            "Stripping is applied only in some code paths while others assign directly",
            "Nested paths are not declared, so a dotted key bypasses the flat allow-list",
            "The retest after the change was never run",
        ],
        "patterns": [
            (
                "Declaration",
                "endpoint: PATCH /orders/{id} -> allowed: [status, note, shipping_address.street, shipping_address.city]",
            ),
            (
                "Placement",
                "parse -> allow-list -> assign -> persist; an allow-list applied before parsing is bypassed by whatever the parser produces",
            ),
            (
                "Retest set",
                "re-run unknown-field, privileged-field and nested-key probes; all three must now be rejected with the same response",
            ),
        ],
        "pitfalls": [
            "Deriving the allow-list from the model, which is the defect restated as a fix",
            "Declaring only flat fields while nested paths remain writable",
            "Declaring the change without re-running the probes that found the problem",
        ],
        "done_when": [
            "An explicit field declaration exists per endpoint and is applied at the assignment boundary",
            "The three original probes are re-run and their results recorded",
        ],
        "refs": [
            "[OWASP - Mass assignment guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "strict-dto-and-validation-boundary",
        "title": "Strict DTO and Validation Boundary",
        "summary": "Give every write path a strict request object that rejects unknown, mistyped and out-of-range input before construction, so the handler only ever sees declared shape",
        "use_when": "validation is loose, applied after construction, or varies by content type",
        "avoid_when": "a strict request object already governs every write path and a test confirms rejection",
        "tags": ["harden", "validation", "schema"],
        "steps": [
            "Define a request object per endpoint with declared fields, types, ranges and enumerations.",
            "Configure it to reject unknown fields rather than discard them, so a client error is visible instead of silent.",
            "Run it before object construction, so nothing unvalidated is ever built.",
            "Apply the same object regardless of which parser produced the request, since parser choice must not change policy.",
            "Return one uniform rejection for all validation failures with a correlation id.",
            "Re-run the coercion, range, duplicate-key and content-type probes against the change.",
        ],
        "signals": [
            "Validation runs after an object is constructed from the parsed body",
            "Unknown fields are silently discarded rather than rejected",
            "Different parsers yield different validation behaviour for the same bytes",
            "Validation failures return several distinct error shapes",
        ],
        "patterns": [
            (
                "Target order",
                "parse -> validate (strict, reject unknown) -> construct -> handle; the validator runs before anything is built",
            ),
            (
                "Reject-not-strip",
                "rejection tells the caller their request was wrong; silent stripping hides a client bug and makes support harder",
            ),
            (
                "Retest set",
                "re-run coercion, range, duplicate-key and content-type probes; each must now produce the same uniform rejection",
            ),
        ],
        "pitfalls": [
            "Adding validation after construction, which still allows transient invalid state",
            "Stripping unknown fields quietly, which fixes the exposure while hiding the client error",
            "Validating only the default parser path while a second content type reaches the handler unvalidated",
        ],
        "done_when": [
            "Each write path has a strict request object that rejects unknown input before construction",
            "The four original probes are re-run with results recorded",
        ],
        "refs": [
            "[OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)",
            "[CWE-20 - Improper input validation](https://cwe.mitre.org/data/definitions/20.html)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "uniform-error-response-and-correlation",
        "title": "Uniform Error Response and Correlation",
        "summary": "Return one response shape for each error class with a correlation id, so a caller cannot map your internals by trying different malformed inputs",
        "use_when": "the error surface map shows differing shapes, disclosed field names or stack detail",
        "avoid_when": "one formatter already handles every error and a probe confirms uniform output",
        "tags": ["harden", "errors", "disclosure"],
        "steps": [
            "Group the mapped errors into classes: validation, authorization, not found, conflict and internal.",
            "Give each class one status and one body shape, with no per-condition detail beyond a stable code.",
            "Move the specific reason into the server log and put a correlation id in the response.",
            "Confirm the formatter runs for every path, including errors raised before the handler and in middleware.",
            "Re-run every controlled error trigger and confirm each now returns the uniform shape for its class.",
            "Record the before and after shapes so the reduction in disclosed detail is provable.",
        ],
        "signals": [
            "Different conditions within one class return different messages or codes",
            "An error raised in middleware returns a framework default rather than the uniform shape",
            "A response body contains a field name, a query fragment or a stack frame",
            "The correlation id is absent, leaving operators unable to diagnose a real failure",
        ],
        "patterns": [
            (
                "Class table",
                "class | status | body | reason location\nvalidation | 400 | {code, correlation_id} | server log\nauthorization | 403 | {code, correlation_id} | server log\ninternal | 500 | {code, correlation_id} | server log",
            ),
            (
                "Coverage check",
                "test an error raised in middleware and one before the handler runs, since both usually bypass an application-level formatter",
            ),
            (
                "Retest sweep",
                "re-run every trigger from the leak table; all must return their class's single shape byte for byte",
            ),
        ],
        "pitfalls": [
            "Unifying the body while statuses still differ per condition, which leaks through the code",
            "Fixing only errors raised inside handlers while middleware keeps returning framework defaults",
            "Removing the correlation id, which leaves operators unable to diagnose",
        ],
        "done_when": [
            "Every error class has one status and one body shape with a correlation id",
            "Pre-handler and middleware error paths return the same uniform shape, with the retest sweep recorded",
        ],
        "refs": [
            "[CWE-209 - Generation of error message containing sensitive information](https://cwe.mitre.org/data/definitions/209.html)",
            "[OWASP - Error handling guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "debug-surface-disabled-in-shared-environments",
        "title": "Debug Surface Disabled in Shared Environments",
        "summary": "Turn off debug, introspection and verbose error paths in any environment more than one person can reach, and verify by request rather than by configuration reading",
        "use_when": "a debug or introspection route is reachable or verbose errors are enabled outside a local environment",
        "avoid_when": "every debug surface is disabled in shared environments and a request confirms it",
        "tags": ["harden", "debug", "configuration"],
        "steps": [
            "List every debug, introspection, metrics-detail and verbose-error surface found during probing.",
            "Disable each in shared environments, or place it behind authentication if it must remain available.",
            "Prefer removing the route over flagging it, since a flag can be flipped back by a later deploy.",
            "Verify by issuing the same requests that found the exposure and confirming rejection or absence.",
            "Confirm the environment delta now records the setting as disabled in every shared environment.",
            "Re-run the debug-endpoint probe and record the result beside the change.",
        ],
        "signals": [
            "A debug route is gated by a flag that a later deploy could re-enable",
            "The fix is a configuration change with no verification request recorded",
            "One shared environment still answers a debug path after others were closed",
            "The environment delta still lists the debug setting as enabled",
        ],
        "patterns": [
            (
                "Closure record",
                "surface | action | verification request | result\n/debug/routes | removed | GET -> 404 | confirmed absent\nverbose errors | flag off | trigger -> uniform body | confirmed",
            ),
            (
                "Remove-over-flag",
                "removal survives a deploy; a flag flipped by a later change does not, so prefer deletion where the route has no legitimate use",
            ),
            (
                "Delta update",
                "the environment delta row is updated in the same change, so the record and the reality stay aligned",
            ),
        ],
        "pitfalls": [
            "Closing a debug route in one environment while another shared environment keeps it",
            "Recording a configuration edit as the fix without a request proving the surface is gone",
            "Leaving the setting enabled in the delta, which makes the next assessment repeat the work",
        ],
        "done_when": [
            "Each debug surface has an action and a verification request with a recorded result",
            "The environment delta reflects the disabled state in every shared environment",
        ],
        "refs": [
            "[CWE-489 - Active debug code](https://cwe.mitre.org/data/definitions/489.html)",
            "[OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "concurrency-guard-and-idempotent-write",
        "title": "Concurrency Guard and Idempotent Write",
        "summary": "Add a version guard so concurrent updates conflict visibly, and enforce the idempotency key so a retried create cannot produce a second object",
        "use_when": "a lost update or a duplicate create was observed during probing",
        "avoid_when": "a version guard and an enforced idempotency key already exist and probes confirm both",
        "tags": ["harden", "concurrency", "idempotency"],
        "steps": [
            "Add a version or updated-at field to each mutable object and require it on every update.",
            "Return a conflict status when the supplied version does not match, rather than silently last-write-wins.",
            "Enforce the idempotency key by storing it with its first response and returning that response on replay.",
            "Key the stored response on the request identity so a changed body with a reused key is rejected.",
            "Re-run the interleaving and idempotency probes against the change and record the outcomes.",
            "State what happens to concurrent requests that arrive together, since a guard moves the failure rather than removing it.",
        ],
        "signals": [
            "Two concurrent updates result in one silently overwriting the other",
            "A replayed create key produces a second object",
            "A reused key with a changed body is processed instead of rejected",
            "A conflict is returned as a generic error with no indication of the version mismatch",
        ],
        "patterns": [
            (
                "Guard record",
                "field: version | required on: update | mismatch: 409 with correlation id | last-write-wins: disabled",
            ),
            (
                "Idempotency record",
                "key storage: keyed to request identity, retained for <window> | replay: original response returned | changed body with same key: 409 rejected",
            ),
            (
                "Retest expectation",
                "re-run concurrent-write-interleaving and idempotency-key-handling; both must now show the guard working rather than the effect repeating",
            ),
        ],
        "pitfalls": [
            "Adding a version field but leaving the handler to overwrite on mismatch anyway",
            "Storing the idempotency key without binding it to the body, so a changed request returns a stale response",
            "Treating a conflict response as a fix without re-running the concurrent probe",
        ],
        "done_when": [
            "Updates require a version and return a conflict on mismatch, with a recorded retest",
            "Idempotency keys are enforced and bound to request identity, with the replay retest recorded",
        ],
        "refs": [
            "[CWE-362 - Concurrent execution with improper synchronization](https://cwe.mitre.org/data/definitions/362.html)",
            "[CWE-841 - Improper enforcement of behavioral workflow](https://cwe.mitre.org/data/definitions/841.html)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "regression-probe-suite",
        "title": "Regression Probe Suite",
        "summary": "Turn every probe that found something into a repeatable check that runs on every change, so the fix is protected rather than merely applied",
        "use_when": "findings have been fixed and nothing currently prevents them returning",
        "avoid_when": "a suite already covers each finding and runs in the pipeline with fixture proof",
        "tags": ["harden", "regression", "pipeline"],
        "steps": [
            "For each finding, write the probe as a check with an explicit expected rejection or expected state.",
            "Run the checks against the fix to prove they fail before it and pass after, which is what makes them meaningful.",
            "Place them in the pipeline that runs on every change rather than in a scheduled job nobody reads.",
            "Make the assertion about the specific behaviour, not only a status code, so a coincidental 400 does not pass.",
            "Record which findings have a check and which do not, since the unchecked list is the remaining risk.",
            "Assign an owner to the suite, because an unowned check stops being maintained within a quarter.",
        ],
        "signals": [
            "A check asserts only a status code, so any rejection passes it",
            "The check was never observed failing before the fix was applied",
            "Some findings have no check and the report does not say which",
            "No owner is assigned to maintaining the suite",
        ],
        "patterns": [
            (
                "Check record",
                "finding F-01 | probe: send unknown field | assert: field absent on read-back, not merely status 400 | owner: team-api",
            ),
            (
                "Fail-then-pass",
                "run the check against the pre-fix build and the post-fix build; both results recorded, since a check that never failed proves nothing",
            ),
            (
                "Coverage list",
                "findings with checks and without checks are both listed; the without list is what remains unprotected",
            ),
        ],
        "pitfalls": [
            "Asserting only a status code, so a different rejection satisfies the check",
            "Never observing the check fail, which means its strength is unknown",
            "Leaving the suite unowned so it decays as the code around it changes",
        ],
        "done_when": [
            "Every finding has a named check with a behavioural assertion and an owner",
            "Each check is recorded as failing before the fix and passing after it",
        ],
        "refs": [
            "[OWASP - Security regression testing](https://owasp.org/www-project-application-security-verification-standard/)",
            "[NIST SP 800-53 - Configuration change control](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "implementation-finding-evidence-pack",
        "title": "Implementation Finding Evidence Pack",
        "summary": "Assemble a report where every implementation claim carries its request pair, response diff, attribution and boundary version, so a reader can check the claim rather than trust it",
        "use_when": "a confirmed backend observation is ready to be written up for the owning team",
        "avoid_when": "the finding has already been reported and only a closing note remains",
        "tags": ["document", "evidence", "reporting"],
        "steps": [
            "State the defect in one sentence naming endpoint, input and outcome, without adjectives.",
            "Attach the baseline and probe captures so the difference is visible rather than described.",
            "Include the single-input attribution replay that establishes which input caused the effect.",
            "Record the request shapes for both captures, including which field you varied.",
            "Give the reproduction recipe and the boundary version that permitted each request.",
            "State impact as precondition, effect, boundary and class, and stop there.",
        ],
        "signals": [
            "A report claims an implementation defect without the request pair that revealed it",
            "The attribution replay is missing, so the causal claim rests on an assumption",
            "Statuses are given without the response diff that distinguishes the cases",
            "Impact is stated without naming the precondition an attacker would already need",
        ],
        "patterns": [
            (
                "Claim skeleton",
                "claim: <endpoint> stores <undeclared input> because <allow-list> is absent\nbaseline vs probe: <the diff>\nattribution: <input> alone reproduces it\nimpact: precondition / effect / boundary / class",
            ),
            (
                "Evidence block",
                "E-011 | PATCH /orders/{id} | body: {status, extra_field} | resp 200 | read-back: extra_field present | boundary v3",
            ),
            (
                "Boundary note",
                "attach the boundary version and mark each request as permitted by it, so the test itself can be audited",
            ),
        ],
        "pitfalls": [
            "Presenting a narrative claim when the reader needs the raw request pair to judge it",
            "Leaving out the attribution replay, which is what makes it a causal claim rather than a correlation",
            "Inflating impact beyond what the recorded requests demonstrate",
        ],
        "done_when": [
            "Every claim is followed by a baseline and probe pair with the attribution replay",
            "The reproduction recipe and boundary version are attached to the pack",
        ],
        "refs": [
            "[OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)",
            "[NIST SP 800-61 - Incident handling guidance](https://csrc.nist.gov/pubs/sp/800/61/r2/final)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "reproduction-steps-in-client-terms",
        "title": "Reproduction Steps in Client Terms",
        "summary": "Write the reproduction so someone else can run it with their own client and fixtures, using plain requests rather than the tooling only you had set up",
        "use_when": "an owner must independently reproduce a finding before acting on it",
        "avoid_when": "the owner has already reproduced the observation themselves",
        "tags": ["document", "reproduction", "handover"],
        "steps": [
            "Rewrite the sequence as plain requests: method, path, headers and body, with placeholders for the reader's own identifiers.",
            "State the preconditions: an account, a role, a record to create, and the environment.",
            "Give expected output per step, so the reader can tell a match from a divergence.",
            "List the environmental assumptions, such as a feature flag or a configuration value, that the result depends on.",
            "Run the published version yourself from a clean state and confirm the expected output still appears.",
            "Mark which findings depend on this recipe for reproduction and which reproduce from the evidence alone.",
        ],
        "signals": [
            "The owner replies that the observation does not reproduce on their side",
            "The recipe contains steps that only work with state your session created",
            "Expected output is described in prose rather than as values to match",
            "Environmental assumptions such as a flag or a mode are unstated",
        ],
        "patterns": [
            (
                "Published recipe",
                "precondition: account with member role, empty cache\n1. POST /orders (key K1) -> expect 201, id R1\n2. PATCH /orders/R1 {status, undeclared: true} -> expect 200\n3. GET /orders/R1 -> expect undeclared absent",
            ),
            (
                "Assumption list",
                "assumes: strict validation off in this environment, no feature flag routing elsewhere; listed so a divergence has an explanation",
            ),
            (
                "Dependency note",
                "findings F-01 and F-03 require this recipe; F-02 reproduces from the evidence block alone",
            ),
        ],
        "pitfalls": [
            "Publishing a recipe that depends on an idempotency key or record from an earlier probe",
            "Omitting an environment flag, then reading a configuration difference as a failed reproduction",
            "Never re-running the published version, so a later change invalidates it unnoticed",
        ],
        "done_when": [
            "The published recipe runs from a clean state and produces the stated expected output",
            "Environmental assumptions and dependent findings are listed beside it",
        ],
        "refs": [
            "[PortSwigger - Writing reproducible reports](https://portswigger.net/web-security)",
            "[OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "fix-worded-in-framework-terms",
        "title": "Fix Worded in Framework Terms",
        "summary": "Describe each remediation in the vocabulary of the framework and layer that owns it, so the implementer can act without reverse-engineering your finding first",
        "use_when": "a backend finding is ready to include remediation across handler, middleware and configuration layers",
        "avoid_when": "the fix is one configuration value with an obvious verification step",
        "tags": ["document", "remediation", "communication"],
        "steps": [
            "Name the layer for each step: request schema, handler, middleware, framework configuration or gateway.",
            "Write the step in the framework's own terms, naming the object or setting the implementer will change.",
            "State the expected effect so a reader can verify the change rather than assume it.",
            "Include a retest instruction using the exact request from the probe that revealed the defect.",
            "Mark steps needing a partner action or a scheduled window, since those need coordination rather than a merge request.",
            "List what you deliberately did not change and why, so nothing appears silently out of scope.",
        ],
        "signals": [
            "A remediation step says add validation without naming the object or setting to change",
            "A step requiring a migration or a window appears with no owner or date",
            "No retest instruction is given, so closure cannot be verified",
            "The report does not say which related items were left unchanged",
        ],
        "patterns": [
            (
                "Step line",
                "layer: request schema | change: declare strict request object rejecting unknown fields | effect: probe now returns uniform 400 | retest: replay evidence E-011",
            ),
            (
                "Framework vocabulary",
                "reference the actual object the implementer changes: the schema class, the middleware registration, the setting name, not a general principle",
            ),
            (
                "Not-changed list",
                "unchanged: gateway timeout, because it belongs to the platform team; recorded so it is not reported as an outstanding item on our side",
            ),
        ],
        "pitfalls": [
            "Writing generic advice the implementer already knows while omitting the specifics of this stack",
            "Hiding a partner-dependent step inside our own task list so it never gets scheduled",
            "Omitting retest instructions, which makes an owner's closure claim unverifiable",
        ],
        "done_when": [
            "Every step names its layer, its effect in framework terms and a retest instruction",
            "Partner-dependent steps carry an owner and a date, and unchanged items are listed with reasons",
        ],
        "refs": [
            "[OWASP - Remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[NIST SP 800-40 - Patch and configuration management](https://csrc.nist.gov/pubs/sp/800/40/r4/final)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "coordinated-retest-and-closure",
        "title": "Coordinated Retest and Closure",
        "summary": "Agree the retest point in writing, re-run the original probe after the fix lands, and close only on the observed result rather than on the promise that it was done",
        "use_when": "a finding has been fixed and is about to be reported as closed",
        "avoid_when": "the fix is still in progress and closure is not yet being considered",
        "tags": ["document", "verification", "closure"],
        "steps": [
            "Agree the retest point, the target date and the person who will run it, in writing, before the fix lands.",
            "Re-run the exact probe from the evidence pack against the same class of record in the same environment.",
            "Record the new status, body and read-back result beside the original evidence entry.",
            "Re-run the regression check if one exists, since a check that passes independently is stronger evidence.",
            "Close only when the observed result matches the expectation, and record the date and the person who confirmed it.",
            "List anything still open with its blocker and owner, since an unfixable finding needs a decision rather than a status.",
        ],
        "signals": [
            "Closure was announced without the original probe being re-run",
            "The retest used a different request than the one that found the defect",
            "A regression check exists but was not run during closure",
            "Items remain open with no owner and no date attached",
        ],
        "patterns": [
            (
                "Closure record",
                "F-01 | retest 2026-10-28 by <owner> | probe replayed: field absent on read-back | regression check: pass | closed",
            ),
            (
                "Same-request rule",
                "re-run the identical request that found the defect; a different request answers a different question",
            ),
            (
                "Open-items list",
                "open item | blocker | owner | needed decision; listed so it is escalated rather than left in a backlog",
            ),
        ],
        "pitfalls": [
            "Closing on a merge request hash instead of on the observed result",
            "Retesting with a different request than the original and calling the difference a pass",
            "Leaving a blocked finding in the list without naming who can unblock it",
        ],
        "done_when": [
            "Each closed finding has a retest record with date, observer and the replayed probe result",
            "Open items name their blocker and the person who can unblock them",
        ],
        "refs": [
            "[NIST SP 800-53 - Assessment and monitoring records](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Verification methodology](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "document"},
    },
]