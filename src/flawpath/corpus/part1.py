"""flawpath skills 1-15: scope and map phases."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "api-assessment-boundary",
        "title": "API Assessment Boundary",
        "summary": "Write down which paths, methods, roles and write operations the backend assessment may exercise, before the first request leaves the workstation",
        "use_when": "a backend API assessment is about to start and no written list states permitted paths, methods or write operations",
        "avoid_when": "the program publishes a machine-readable endpoint list with permitted methods and a stated rate ceiling",
        "tags": ["scope", "authorization", "rules-of-engagement"],
        "steps": [
            "Collect the signed rules of engagement, the published API documentation and any internal endpoint list, noting versions used.",
            "List every permitted path, method and environment exactly as written, without normalizing or guessing wildcards.",
            "Record which write operations are permitted, which are forbidden, and what rollback exists for the permitted ones.",
            "Capture the numeric rate ceiling per endpoint and the total request budget for the session.",
            "Confirm whether destructive verbs such as delete or purge are permitted at all, since that single answer shapes the whole plan.",
            "Save the boundary beside the evidence so a reviewer can prove every recorded request fell inside the permitted set.",
        ],
        "signals": [
            "Rules list hosts but say nothing about which methods may be sent",
            "No rate ceiling exists as a number anywhere in the document",
            "Destructive verbs are neither explicitly allowed nor explicitly banned",
            "A previous session recorded requests against a path you cannot find in writing",
        ],
        "patterns": [
            (
                "Boundary record",
                "scope:\n  paths: [/api/v1/orders/**, /api/v1/users/me]\n  methods: [GET, POST, PATCH]\n  forbidden: [DELETE, PUT]\n  rate_rps: 2\n  writes: create + update allowed, rollback documented\n  environments: staging only",
            ),
            (
                "Pre-flight echo",
                "Before session start, restate paths, methods, write permissions, rate ceiling and the ban list. Any element you cannot quote is a gap to resolve, not a permission to assume.",
            ),
            (
                "Evidence binding",
                "Store boundary.md beside evidence/ so each recorded request line carries a document version it can be checked against during review.",
            ),
        ],
        "pitfalls": [
            "Reading a wildcard path as permission for every method on it",
            "Assuming staging and production share a method list",
            "Treating an old approval as current after the API changed version",
        ],
        "done_when": [
            "A written boundary table names paths, methods, write permissions, rate ceiling and the ban list",
            "Every later evidence entry carries the document version that justified the request",
        ],
        "refs": [
            "[OWASP - API security testing guidance](https://owasp.org/API-Security/)",
            "[PortSwigger - Web service testing](https://portswigger.net/web-security)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "handler-and-route-inventory",
        "title": "Handler and Route Inventory",
        "summary": "Enumerate every route and its handler, including internal and versioned ones, because an unlisted handler is where a check you assumed exists turns out not to",
        "use_when": "a backend is in scope and no maintained list of routes with their handlers exists",
        "avoid_when": "framework-generated documentation lists every route with handler and middleware already confirmed current",
        "tags": ["scope", "inventory", "routes"],
        "steps": [
            "Extract routes from the framework registry or router table rather than from prose documentation that may be stale.",
            "Record for each route its method, handler function, middleware chain and the roles permitted to reach it.",
            "Flag routes that exist but are undocumented, since these are usually the ones with the oldest checks.",
            "Note versioned duplicates where one version kept a check the newer one dropped.",
            "Separate public, authenticated and internal-only routes into three lists so coverage is visible per class.",
            "Carry undocumented and internal routes into the map phase as explicit questions rather than dropping them.",
        ],
        "signals": [
            "The router table contains paths absent from the published documentation",
            "Two API versions expose the same operation with different middleware",
            "An internal-only route shares a prefix with public routes",
            "A handler is registered dynamically, so a static route list misses it",
        ],
        "patterns": [
            (
                "Inventory row",
                "path | method | handler | middleware | roles | documented\n/api/v1/orders | GET | list_orders | auth, rate | member | yes\n/internal/reindex | POST | reindex | none | internal | no",
            ),
            (
                "Class split",
                "public | authenticated | internal; each list is reviewed separately so an internal route with no middleware is visible rather than averaged away",
            ),
            (
                "Dynamic-route note",
                "when a route is registered at runtime, record where registration happens so the inventory can be regenerated from that source",
            ),
        ],
        "pitfalls": [
            "Building the inventory from documentation, which is exactly what has drifted",
            "Skipping versioned duplicates, where a dropped check is most likely to be found",
            "Assuming internal routes are unreachable because a gateway usually fronts them",
        ],
        "done_when": [
            "Every route has a row with method, handler, middleware, permitted roles and documentation status",
            "Undocumented and internal routes are listed as explicit questions for the map phase",
        ],
        "refs": [
            "[OWASP - API documentation and discovery](https://owasp.org/API-Security/)",
            "[CWE-778 - Insufficient logging](https://cwe.mitre.org/data/definitions/778.html)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "write-surface-and-state-map",
        "title": "Write Surface and State Map",
        "summary": "Establish which objects are writable and which transitions each write can trigger, because a state change you did not expect is the real effect of a mass-assignment defect",
        "use_when": "the API mutates domain objects and the reachable transitions have not been enumerated",
        "avoid_when": "the API is read-only, or a documented state model covers every writable object",
        "tags": ["scope", "state", "inventory"],
        "steps": [
            "List every domain object the API can create, update or delete, with the endpoint that performs each operation.",
            "For each object, list the states it can be in and the transitions the endpoints can cause.",
            "Mark which transitions are intended for which role, since that is the expectation a defect would break.",
            "Note transitions reachable through an update endpoint rather than a dedicated one, which is where unexpected paths appear.",
            "Record what rollback or compensation exists for each permitted write, so testing can be undone.",
            "Carry the map into the probe phase as the set of intended transitions to compare against observed ones.",
        ],
        "signals": [
            "An update endpoint can set a field that a dedicated transition endpoint also controls",
            "No documented state model exists for an object with several visible states",
            "A transition appears reachable that the role matrix says belongs to another role",
            "No rollback path exists for a write the boundary permits",
        ],
        "patterns": [
            (
                "Transition row",
                "object: order | transition: draft -> paid | intended role: billing service | reachable via: PATCH /orders/{id} (status field)",
            ),
            (
                "Unexpected-path flag",
                "a transition reachable through a generic update endpoint rather than its dedicated operation is flagged, since that is the usual defect shape",
            ),
            (
                "Rollback column",
                "each permitted write carries a rollback: undo endpoint, compensating call, or none; none means the write must be avoided or carefully bounded",
            ),
        ],
        "pitfalls": [
            "Testing only the dedicated transition endpoint while the generic update reaches the same state",
            "Assuming a transition is impossible because no endpoint is documented for it",
            "Performing a permitted write with no rollback when the boundary required one",
        ],
        "done_when": [
            "Every writable object has a row with intended transitions, roles and rollback status",
            "Transitions reachable through generic update endpoints are flagged explicitly",
        ],
        "refs": [
            "[OWASP - Broken object level authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)",
            "[CWE-284 - Improper access control](https://cwe.mitre.org/data/definitions/284.html)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "environment-configuration-delta",
        "title": "Environment Configuration Delta",
        "summary": "Record which settings differ between the environment you test and the one that matters, because a check passing in staging says nothing about production behaviour",
        "use_when": "the assessment runs against a non-production environment while findings will apply to production",
        "avoid_when": "one environment serves all traffic and configuration is identical by construction",
        "tags": ["scope", "configuration", "environment"],
        "steps": [
            "List the settings that govern behaviour: validation strictness, debug mode, authentication enforcement, rate limits and feature flags.",
            "Read each value in the tested environment and record it verbatim beside the documented production value.",
            "Flag any setting where the tested environment is more permissive than production, or the reverse.",
            "Note feature flags that change which code path runs, since a flag difference makes a finding inapplicable.",
            "State in the report which findings depend on a setting that differs between environments.",
            "Keep the delta current, since configuration changes while an assessment runs.",
        ],
        "signals": [
            "Debug mode or verbose errors are enabled in the environment you are testing",
            "Validation strictness differs between the tested and production settings",
            "A feature flag routes one environment to a different handler",
            "The delta has never been read, so findings are assumed transferable",
        ],
        "patterns": [
            (
                "Delta row",
                "setting | tested env | production | effect on findings\ndebug | on | off | error-shape findings not transferable\nstrict validation | off | on | coercion findings may not apply",
            ),
            (
                "Transfer statement",
                "for each finding, one line saying whether it depends on a differing setting, so a reader knows which to re-verify in production",
            ),
            (
                "Flag note",
                "feature flags that change routing are recorded with their state, because a flag-off path was never exercised",
            ),
        ],
        "pitfalls": [
            "Reporting a debug-only error shape as a production defect",
            "Assuming staging is stricter than production when the opposite is true",
            "Noting a flag difference but never stating which findings it invalidates",
        ],
        "done_when": [
            "A delta table lists each behavioural setting in both environments with its effect on findings",
            "Findings that depend on a differing setting are marked transferable or not",
        ],
        "refs": [
            "[OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)",
            "[NIST SP 800-53 - Configuration settings controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "synthetic-record-only-policy",
        "title": "Synthetic Record Only Policy",
        "summary": "Create and mutate only records you own, so a write-surface assessment never leaves real customer data changed or a real workflow triggered",
        "use_when": "the assessment will create or update records through the API",
        "avoid_when": "the environment runs entirely on fixtures that no real record can reach",
        "tags": ["scope", "data-handling", "safety"],
        "steps": [
            "Create a synthetic record set under an account you control, with invented identifiers and values.",
            "Mark those records with a recognizable marker so a later cleanup can find them without a query you have to trust.",
            "Check every write you plan against the boundary: permitted method, permitted path, rollback available.",
            "Avoid any write that triggers an external effect, such as a notification or a charge, unless the boundary explicitly permits it.",
            "Record the identifiers of every record you created so cleanup is mechanical rather than archaeological.",
            "Clean up at the end and record what was removed and what could not be.",
        ],
        "signals": [
            "A test write would trigger a notification or a charge to someone",
            "No marker distinguishes records you created from records that already existed",
            "Created records are never cleaned up, so they accumulate in the environment",
            "A write targets an existing record rather than one you created",
        ],
        "patterns": [
            (
                "Synthetic marker",
                "owner: tester@example.test | note: authorized assessment fixture | created: 2026-10-28 | cleanup: scheduled",
            ),
            (
                "Write check",
                "before each write: method permitted? path permitted? rollback exists? external effect avoided? all four yes before sending",
            ),
            (
                "Cleanup list",
                "identifiers created, removed at <time>, exceptions recorded; stored beside the boundary so the session leaves nothing behind",
            ),
        ],
        "pitfalls": [
            "Updating a record you did not create because it was convenient to test against",
            "Triggering a real notification to prove a field reaches a template",
            "Leaving fixture records behind because cleanup was planned but never scheduled",
        ],
        "done_when": [
            "Every write targets a marked record you created, with the four-part write check recorded",
            "A cleanup list exists with what was removed and any exceptions",
        ],
        "refs": [
            "[OWASP - Sensitive data exposure](https://owasp.org/www-project-top-ten/)",
            "[NIST SP 800-53 - Information handling controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "mutation-budget-and-rollback",
        "title": "Mutation Budget and Rollback",
        "summary": "Agree a numeric cap on write operations and a rollback step for each, so a probe that mutates state cannot quietly become the incident being investigated",
        "use_when": "the plan includes write operations and no numeric cap or rollback sequence has been agreed",
        "avoid_when": "the boundary already states a mutation ceiling and provides a documented rollback",
        "tags": ["scope", "rate-limit", "operations"],
        "steps": [
            "Record a numeric ceiling: mutations per endpoint and a total for the session, with a pause between probe families.",
            "Write the rollback step for each class of mutation before performing any of them, not afterwards.",
            "Set a stop condition tied to observed behaviour, such as a queue depth or an error rate, rather than to a planned step count.",
            "Check whether the API applies rate limits itself, since hitting them changes what your results mean.",
            "Log actual mutations beside the plan so the owner can see the session stayed inside the budget.",
            "Perform the rollbacks at the end and record their results alongside the creations.",
        ],
        "signals": [
            "The plan mutates state with no stated ceiling anywhere",
            "A rollback step was never written and cannot be recalled under time pressure",
            "An error rate rose during the session without a stop condition to catch it",
            "The API's own rate limit began returning responses partway through",
        ],
        "patterns": [
            (
                "Budget record",
                "per_endpoint: 10 | session_total: 150 | pause: 5s | stop: any 5xx increase or queue depth > threshold | actual: 62",
            ),
            (
                "Rollback first",
                "write the rollback before the first mutation: rollback step, expected result, and what to do if it fails",
            ),
            (
                "Rate-limit note",
                "when the API's own limit returns 429, record it: it marks both your ceiling and a real behavioural observation",
            ),
        ],
        "pitfalls": [
            "Discovering the rollback procedure after a write did something unexpected",
            "Treating a 429 as a bug to report when it is the system working as designed",
            "Ending a session without the rollbacks having run",
        ],
        "done_when": [
            "A numeric mutation ceiling and per-class rollback steps exist before the first write",
            "Actual mutations and rollback results are recorded beside the plan",
        ],
        "refs": [
            "[NIST SP 800-53 - Configuration and change controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - API rate limiting guidance](https://owasp.org/API-Security/)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "observability-and-ownership-record",
        "title": "Observability and Ownership Record",
        "summary": "Establish who owns the logs and what you are allowed to read in them, because a finding that cannot be traced to its own trace line will not survive review",
        "use_when": "the assessment will correlate API requests with server-side logs or traces",
        "avoid_when": "the owner supplies read access to the relevant logs with a stated retention and scope",
        "tags": ["scope", "observability", "logs"],
        "steps": [
            "Confirm what log and trace access the boundary permits, including which environments and which time window.",
            "Identify the correlation identifier the API returns or records, since that is what joins your request to server-side state.",
            "Record who owns each log source, so a question during review has a person to reach.",
            "Note retention, because a finding traced to a log older than retention cannot be re-checked.",
            "Confirm that reading logs will not expose other users' records beyond what the boundary allows.",
            "Write the access, correlation method and ownership into the boundary document before the first request.",
        ],
        "signals": [
            "The boundary says nothing about reading server-side logs",
            "No correlation identifier joins a request to its server-side trace",
            "Log retention is shorter than the assessment window",
            "No one can say who owns the error log for the endpoint under test",
        ],
        "patterns": [
            (
                "Access record",
                "source: application logs | window: staging, assessment dates | correlation: x-request-id header | owner: platform | retention: 14 days",
            ),
            (
                "Correlation rule",
                "every evidence entry records the correlation id, so a reviewer can find the matching server-side line without re-issuing the request",
            ),
            (
                "Ownership column",
                "each log source has an owner named; a source with no owner is escalated before it is relied upon",
            ),
        ],
        "pitfalls": [
            "Trusting a client-side response as proof of server-side behaviour without a correlated log line",
            "Reading logs beyond the permitted window or environment",
            "Relying on a log source whose retention ends before review happens",
        ],
        "done_when": [
            "Log access, correlation method, owners and retention are recorded in the boundary",
            "Every later evidence entry carries the correlation id that ties it to server-side state",
        ],
        "refs": [
            "[OWASP - Logging cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)",
            "[CWE-778 - Insufficient logging](https://cwe.mitre.org/data/definitions/778.html)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "route-verb-matrix",
        "title": "Route Verb Matrix",
        "summary": "Build the path-by-method matrix from the router itself, because an undocumented method on a documented path is usually where the newest and least-reviewed handler lives",
        "use_when": "a route inventory exists but has not been expanded into a full path-by-method matrix",
        "avoid_when": "framework-generated documentation already lists every path with every method and its handler",
        "tags": ["map", "routes", "methods"],
        "steps": [
            "Read the router table and expand it into one row per path and method combination actually registered.",
            "Mark each cell as documented or undocumented, and as having middleware or none.",
            "Probe for a method the matrix does not list on a path you expect to answer, such as an override or a fallback.",
            "Note framework defaults, such as an automatically registered index or an options handler.",
            "Check for method override handling where a body or header field changes the effective verb.",
            "Carry undocumented cells into the probe phase as the highest-value handlers to examine.",
        ],
        "signals": [
            "A path answers a method the matrix does not list",
            "A method override field or header changes which handler runs",
            "An automatically registered fallback handler exists with no middleware",
            "One path has three methods while its neighbours have one each",
        ],
        "patterns": [
            (
                "Matrix row",
                "path | method | handler | middleware | documented\n/api/v1/orders | GET | list | auth | yes\n/api/v1/orders | PATCH | update | auth | yes\n/api/v1/orders | DELETE | destroy | none | no  <- undocumented",
            ),
            (
                "Override check",
                "send a permitted method with an override field set to a forbidden verb and observe whether the handler changes; a change means the matrix must record effective verbs",
            ),
            (
                "Fallback flag",
                "an automatically registered handler gets its own row with a flag, because nobody reviewed it when it was added",
            ),
        ],
        "pitfalls": [
            "Building the matrix from documentation, which is what drifted in the first place",
            "Recording only the documented verb and never probing for an undocumented one",
            "Missing a method override that makes the effective verb different from the sent one",
        ],
        "done_when": [
            "Every path has one row per registered method with middleware and documentation status",
            "At least one probe for an unlisted method or override has a recorded result",
        ],
        "refs": [
            "[OWASP - API9 Improper inventory management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)",
            "[CWE-778 - Insufficient logging](https://cwe.mitre.org/data/definitions/778.html)",
        ],
        "meta": {"phase": "map"},
    },
    {
        "slug": "parameter-provenance-map",
        "title": "Parameter Provenance Map",
        "summary": "Trace every field the handler reads back to where it comes from, because the field that reaches an assignment without validation is the one a defect is built from",
        "use_when": "handlers accept input from several sources and no map records which fields arrive from which",
        "avoid_when": "one schema defines every input and the source of each field is explicit",
        "tags": ["map", "parameters", "provenance"],
        "steps": [
            "For each handler, list every field read and mark its source: path, query, header, body or derived server-side.",
            "Note where a field is merged from more than one source, since precedence between them is a decision someone made silently.",
            "Mark whether each field passes through validation, coercion or sanitization before use, and which of those it gets.",
            "Identify fields read from a merged object rather than a named schema, which is where unknown keys survive.",
            "Record derived fields separately, since they are computed rather than accepted.",
            "Carry unvalidated merged fields into the probe phase as the primary candidates.",
        ],
        "signals": [
            "A handler reads a merged object rather than a named schema",
            "Two sources supply the same field with no documented precedence",
            "A field reaches an assignment with no validation step on its path",
            "A header-derived value is used where a body field was expected",
        ],
        "patterns": [
            (
                "Provenance row",
                "field | source | validated | coerced | merged | handler use\nid | path | yes | yes | no | lookup\nrole | body | no | no | yes  <- candidate | assignment\nx-tenant | header | no | no | no | routing",
            ),
            (
                "Merge flag",
                "any field arriving through a merged object is marked, because unknown keys survive a merge that a named schema would reject",
            ),
            (
                "Precedence note",
                "when two sources supply one field, record which wins and where that rule is written, or mark it as an implicit decision",
            ),
        ],
        "pitfalls": [
            "Assuming a field is validated because it appears in documentation",
            "Mapping only body fields and missing header-derived values that affect routing",
            "Recording derived fields as accepted input, which sends the probe phase after them",
        ],
        "done_when": [
            "Every field read by each handler has a source and a validation status",
            "Merged and multi-source fields are marked, with precedence recorded or flagged as implicit",
        ],
        "refs": [
            "[OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)",
            "[CWE-915 - Improperly controlled modification of dynamically-determined object attributes](https://cwe.mitre.org/data/definitions/915.html)",
        ],
        "meta": {"phase": "map"},
    },
    {
        "slug": "deserialization-and-validation-boundary",
        "title": "Deserialization and Validation Boundary",
        "summary": "Locate exactly where a request body becomes application objects and where validation runs relative to it, because everything downstream of an unvalidated parse inherits the risk",
        "use_when": "the request body is parsed into objects and the ordering of parse, validate and authorize is unconfirmed",
        "avoid_when": "a framework pipeline documents the order and the handler code confirms it",
        "tags": ["map", "parsing", "validation"],
        "steps": [
            "Find the point in the pipeline where the body is decoded and note what runs before and after it.",
            "Determine whether validation runs before object construction or after, since the two orders differ in what they permit.",
            "Check whether unknown fields are rejected, stripped or passed through by default.",
            "Note which parser is used and whether more than one can parse the same request depending on content type.",
            "Record whether authorization runs before or after the parse, since an unauthenticated parse is a resource question too.",
            "Write the order as an explicit sequence so a later reader does not have to infer it.",
        ],
        "signals": [
            "Validation runs after object construction from the parsed body",
            "Unknown fields are passed through rather than rejected",
            "Two parsers can handle the same request depending on the content type header",
            "Authorization happens after the body has already been parsed",
        ],
        "patterns": [
            (
                "Order record",
                "receive -> parse body -> construct object -> validate -> authorize -> handle\nany other order is recorded explicitly rather than assumed",
            ),
            (
                "Unknown-field policy",
                "reject | strip | pass through; record which applies by default, since pass-through is what mass assignment needs",
            ),
            (
                "Parser list",
                "content type -> parser used; a second parser for the same request is listed because it may apply a different policy",
            ),
        ],
        "pitfalls": [
            "Assuming validation precedes construction because that is how the framework is usually described",
            "Recording the documented order instead of reading the code path that runs",
            "Ignoring a second parser selected by content type",
        ],
        "done_when": [
            "The parse, validate and authorize order is written as an explicit sequence with a code location",
            "The unknown-field policy and the parsers in play are recorded",
        ],
        "refs": [
            "[OWASP - Deserialization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)",
            "[CWE-502 - Deserialization of untrusted data](https://cwe.mitre.org/data/definitions/502.html)",
        ],
        "meta": {"phase": "map"},
    },
    {
        "slug": "object-identifier-shape",
        "title": "Object Identifier Shape",
        "summary": "Characterise how object identifiers are formed and whether they are predictable, because the shape decides whether an authorization check is doing real work or just matching a guessable key",
        "use_when": "endpoints address domain objects by an identifier and its formation has not been recorded",
        "avoid_when": "identifiers are documented as opaque and confirmed non-enumerable by construction",
        "tags": ["map", "identifiers", "authorization"],
        "steps": [
            "Collect identifier examples from responses, replacing values with their structural properties only.",
            "Classify the shape: sequential integer, time-ordered, random fixed length, composite key or a hash.",
            "Record whether an identifier appears in a location a client can influence, such as a query or a header.",
            "Check whether authorization is checked against the identifier's owner, or only that the object exists.",
            "Note whether enumeration would be observable in rate limits or logs, since that bounds the practical risk.",
            "Carry the shape and its authorization treatment into the probe phase together, not separately.",
        ],
        "signals": [
            "Identifiers are sequential integers across a tenant boundary",
            "An identifier appears in a response for an object the caller does not own",
            "The check verifies existence but not ownership of the returned object",
            "No rate limit or log line would reveal an enumeration pattern",
        ],
        "patterns": [
            (
                "Shape record",
                "shape: sequential integer | exposed in: response body, path | ownership checked: yes (separate query) | enumeration observable: yes via 404 timing",
            ),
            (
                "Authorization pairing",
                "record identifier shape next to the authorization check; a guessable identifier with an existence-only check is the pairing that matters",
            ),
            (
                "Client-influence note",
                "whether a client can supply the identifier in a header or query changes who controls the lookup",
            ),
        ],
        "pitfalls": [
            "Recording the identifier shape without the authorization treatment, which is the other half of the finding",
            "Calling a random-looking identifier safe without reading the check that uses it",
            "Ignoring that an existence check still reveals whether an object exists",
        ],
        "done_when": [
            "Every identifier class has a recorded shape, exposure locations and authorization treatment",
            "Whether enumeration would be observable in rate limits or logs is stated",
        ],
        "refs": [
            "[OWASP - API1 broken object level authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)",
            "[CWE-330 - Use of insufficiently random values](https://cwe.mitre.org/data/definitions/330.html)",
        ],
        "meta": {"phase": "map"},
    },
    {
        "slug": "middleware-chain-order",
        "title": "Middleware Chain Order",
        "summary": "Read the middleware chain in the order it actually executes, because a validation step that runs after authorization changes what an unauthenticated caller can reach",
        "use_when": "middleware is applied at several layers and its real execution order has not been read from configuration",
        "avoid_when": "one documented chain applies to every route and the code confirms it",
        "tags": ["map", "middleware", "order"],
        "steps": [
            "Read the chain from the router or application setup and write the steps in execution order.",
            "Mark which steps are global, which are per-route and which apply only to a path prefix.",
            "Note where a step can be skipped, such as an optional authentication handler that passes on failure.",
            "Identify ordering dependencies: validation before use, authorization before handler, rate limiting before work.",
            "Check whether any step short-circuits the chain or falls through to the handler on error.",
            "Record deviations from the documented order as findings about configuration rather than about code.",
        ],
        "signals": [
            "Authorization is registered after a body-parsing step",
            "An authentication handler falls through to the handler when verification fails",
            "A per-route chain omits a global step rather than extending it",
            "The configured order differs from the documented order",
        ],
        "patterns": [
            (
                "Chain record",
                "1 rate-limit  2 cors  3 authenticate  4 authorize  5 parse  6 validate  7 handler\nread from configuration, not from documentation",
            ),
            (
                "Skip-path flag",
                "each step that can be skipped or that falls through on failure is marked, since a silent fallthrough is the defect shape",
            ),
            (
                "Deviation note",
                "configured vs documented order, with the file that holds the configured one, so the fix has a location",
            ),
        ],
        "pitfalls": [
            "Trusting the documented chain instead of the one the configuration builds",
            "Checking that a step exists without reading where it sits in the order",
            "Missing that a per-route chain replaces the global chain rather than extending it",
        ],
        "done_when": [
            "The chain is written in true execution order with per-route and global steps distinguished",
            "Skip and fallthrough points are marked, and any deviation from documentation is recorded",
        ],
        "refs": [
            "[OWASP - Authorization validation guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-862 - Missing authorization](https://cwe.mitre.org/data/definitions/862.html)",
        ],
        "meta": {"phase": "map"},
    },
    {
        "slug": "response-field-exposure-map",
        "title": "Response Field Exposure Map",
        "summary": "Record which fields each endpoint returns, because an extra field in a response is an exposure that no input-side check will ever catch",
        "use_when": "response bodies have not been catalogued and over-exposure is a concern for this API",
        "avoid_when": "a response schema is enforced and tested for every endpoint",
        "tags": ["map", "responses", "exposure"],
        "steps": [
            "Capture the field set each endpoint returns for a record you created, without recording the values.",
            "Compare that field set with what the endpoint's documentation says it returns.",
            "Mark fields present but undocumented, and fields that reveal internal structure such as roles or flags.",
            "Note whether fields vary by role, since a field shown only to administrators tells you its sensitivity.",
            "Check for fields derived from joined tables that were never intended to leave the service.",
            "Carry undocumented fields into the probe phase as exposure candidates with their endpoint and role noted.",
        ],
        "signals": [
            "A response contains fields absent from the documented schema",
            "An internal flag or role field appears in a response for a normal caller",
            "Fields differ between roles in a way nothing documents",
            "A joined record's fields appear nested in a response",
        ],
        "patterns": [
            (
                "Exposure row",
                "endpoint | role | undocumented fields | derived from\nGET /orders/{id} | member | internal_flag, vendor_code | joined vendor record",
            ),
            (
                "Documented-delta",
                "returned fields minus documented fields; the delta is the finding, listed by name without values",
            ),
            (
                "Role-variance note",
                "same endpoint, two roles, differing field sets: recorded with both sets so the difference is explicit",
            ),
        ],
        "pitfalls": [
            "Cataloguing values instead of field names, which puts real data in the report",
            "Comparing only against one role and missing fields visible to another",
            "Assuming an undocumented field is harmless because it looks internal",
        ],
        "done_when": [
            "Each endpoint has a field set recorded per role, compared against its documentation",
            "Undocumented and derived fields are listed by name as exposure candidates",
        ],
        "refs": [
            "[OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)",
            "[CWE-200 - Exposure of sensitive information](https://cwe.mitre.org/data/definitions/200.html)",
        ],
        "meta": {"phase": "map"},
    },
    {
        "slug": "error-surface-and-shape-map",
        "title": "Error Surface and Shape Map",
        "summary": "Catalogue which layer produces each error shape, so a later probe can tell an application rejection from a framework default from a gateway response",
        "use_when": "error responses have not been attributed to the layer that generates them",
        "avoid_when": "one error formatter handles every response and its output is documented",
        "tags": ["map", "errors", "responses"],
        "steps": [
            "Trigger a small set of controlled errors: not found, bad input, unauthorized, and one rate limit if reachable.",
            "Record the status, shape and headers of each, noting whether the body carries a stack or a code.",
            "Attribute each shape to a layer: gateway, framework, application or a debug handler.",
            "Check whether an error's shape changes when debug mode is on, which the environment delta should already record.",
            "Note whether error shapes leak field names, query structure or internal identifiers.",
            "Record the map beside the boundary so later probes can be read against it without re-deriving a baseline.",
        ],
        "signals": [
            "One error carries a stack trace while another of the same status does not",
            "Error shapes differ by layer and nobody can say which layer produced which",
            "An error body names internal fields or a query structure",
            "The shape changes between environments because of a debug setting",
        ],
        "patterns": [
            (
                "Shape map",
                "condition | status | shape | layer | leaks\nunknown id | 404 | {error} | application | no\nbad body | 400 | framework default | framework | field names\nunhandled | 500 | stack | debug handler | trace",
            ),
            (
                "Layer attribution",
                "each shape is attributed to the layer that produced it, with the evidence: headers, shape and environment setting",
            ),
            (
                "Baseline note",
                "the map is the baseline later probes compare against; without it a new error cannot be recognised as new",
            ),
        ],
        "pitfalls": [
            "Reporting an error shape produced by a debug setting as a production behaviour",
            "Comparing shapes across environments and attributing the difference to the application",
            "Recording shapes without the layer, which leaves the fix assigned to nobody",
        ],
        "done_when": [
            "Each triggered error has a recorded status, shape, producing layer and leakage assessment",
            "The map is stored as the baseline later probes compare against",
        ],
        "refs": [
            "[OWASP - Error handling guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-209 - Generation of error message containing sensitive information](https://cwe.mitre.org/data/definitions/209.html)",
        ],
        "meta": {"phase": "map"},
    },
    {
        "slug": "integration-and-async-surface-map",
        "title": "Integration and Async Surface Map",
        "summary": "Catalogue the queues, webhooks and background jobs a request can trigger, because the effect of a defect often lands off the request path where nobody is watching",
        "use_when": "a handler can enqueue work or call another service and the reachable side effects have not been listed",
        "avoid_when": "handlers are synchronous and the owner confirms no downstream work is triggered",
        "tags": ["map", "async", "integration"],
        "steps": [
            "Trace each mutating handler to the jobs, messages or outbound calls it can enqueue, reading the code rather than a diagram.",
            "Record what each downstream consumer does with the payload it receives, since that is where an unvalidated field becomes an effect.",
            "Note whether a job payload is re-validated on the consuming side or trusted as sent.",
            "Identify retry behaviour on each queue, because a retried job multiplies any unintended effect.",
            "Mark which downstream systems sit outside your testing boundary, so their behaviour is described rather than exercised.",
            "Carry the map into the probe phase with the boundary annotation attached to every out-of-boundary consumer.",
        ],
        "signals": [
            "A handler enqueues a payload that the consumer parses without re-validating",
            "A queue retries a malformed message instead of dead-lettering it",
            "A downstream consumer sits outside the testing boundary but receives data from an in-scope handler",
            "No one can say what a background job does with the fields it is given",
        ],
        "patterns": [
            (
                "Trigger row",
                "handler | job or queue | payload fields | consumer re-validates | retries | in scope\nPATCH /orders | order.sync | id, status, vendor_ref | no | 5 | vendor is out of boundary",
            ),
            (
                "Boundary flag",
                "any consumer outside the boundary is marked describe-only; its behaviour is reported from documentation and code, never exercised",
            ),
            (
                "Multiplier note",
                "retry count times one unintended effect is the real impact, so both numbers appear on the row",
            ),
        ],
        "pitfalls": [
            "Testing only the request path while the effect lands in a queue nobody is watching",
            "Describing a downstream system without noting it was never exercised",
            "Missing that the consumer trusts a payload the in-scope handler never validated",
        ],
        "done_when": [
            "Every mutating handler has a row naming its downstream consumers, payload, re-validation and retries",
            "Consumers outside the testing boundary are marked describe-only with that reason",
        ],
        "refs": [
            "[OWASP - API security guidance](https://owasp.org/API-Security/)",
            "[CWE-918 - Server-side request forgery](https://cwe.mitre.org/data/definitions/918.html)",
        ],
        "meta": {"phase": "map"},
    },
]