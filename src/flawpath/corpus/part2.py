"""flawpath skills 16-33: probe phase."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "unknown-field-acceptance",
        "title": "Unknown Field Acceptance",
        "summary": "Send a field the schema never declares and see whether it survives to the stored object, because acceptance is the precondition every mass-assignment defect needs",
        "use_when": "the boundary permits write requests and the parser's unknown-field policy has not been exercised",
        "avoid_when": "the parser demonstrably rejects unknown fields and a test confirms it in the current build",
        "tags": ["probe", "mass-assignment", "validation"],
        "steps": [
            "Confirm the boundary permits the write and that a rollback exists for the record you will use.",
            "Create or select a synthetic record you own and capture its state before the request.",
            "Send an update containing one field name the schema does not declare, alongside a permitted field.",
            "Read the record back and compare field set and values against the captured state.",
            "Repeat with a second unknown name to separate a name-specific rejection from a general policy.",
            "Record acceptance or rejection with the before and after state, never the sensitive value itself.",
        ],
        "signals": [
            "An undeclared field appears on the stored object after the update",
            "The response echoes the undeclared field as though it were part of the schema",
            "A second unknown name is also accepted, indicating a policy rather than an exception",
            "The field is stored but not returned, which still means it was accepted",
        ],
        "patterns": [
            (
                "Before and after",
                "before: {status: draft, owner: me}\nrequest: {status: active, internal_marker: true}\nafter: {status: active, internal_marker: true} <- unknown accepted",
            ),
            (
                "Two-name rule",
                "send two different unknown names; both accepted means the parser passes unknown keys through by policy",
            ),
            (
                "Stored-not-returned",
                "field absent from the response but present on read-back still counts as accepted; record the read-back as the evidence",
            ),
        ],
        "pitfalls": [
            "Judging acceptance from the response body alone when the field is stored but not echoed",
            "Changing two known fields at once, which makes an unknown field's effect impossible to isolate",
            "Using a record you do not own and leaving it modified",
        ],
        "done_when": [
            "Two unknown names each have a recorded before and after state",
            "Acceptance is determined from read-back rather than from the response body",
        ],
        "refs": [
            "[OWASP - Mass assignment guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "privileged-field-write-probe",
        "title": "Privileged Field Write Probe",
        "summary": "Attempt to set one field that the role matrix reserves for another role, using a single field change so the result can be attributed to exactly that field",
        "use_when": "the state map identifies fields reserved for a role you are not testing as, and the write is permitted by the boundary",
        "avoid_when": "the endpoint is documented to reject reserved fields and a test confirms it",
        "tags": ["probe", "authorization", "mass-assignment"],
        "steps": [
            "Pick one reserved field from the state map and confirm the boundary permits the write method and path.",
            "Send an update changing only that one field on a synthetic record you own.",
            "Read the record back and record whether the reserved field changed.",
            "Compare with a control update that changes only a permitted field, to prove the endpoint accepts writes at all.",
            "If the change is rejected, record the rejection's status and shape against the error map baseline.",
            "Record a one-field result with both the reserved and control attempts beside it.",
        ],
        "signals": [
            "A field reserved to another role changes after a single-field update",
            "The response returns the reserved field as though it were a normal property",
            "Rejection uses a generic validation error rather than an authorization one",
            "The control update and the reserved update behave identically, which is itself informative",
        ],
        "patterns": [
            (
                "Single-field pair",
                "control: PATCH {nickname: t1} -> 200, nickname changed\nreserved: PATCH {role: admin} -> 200, role changed <- finding",
            ),
            (
                "Attribution rule",
                "one field per request; a request changing two fields cannot attribute the outcome to either",
            ),
            (
                "Rejection class",
                "a 403 means authorization caught it, a 400 means schema validation caught it, and 200 means neither did; record which occurred",
            ),
        ],
        "pitfalls": [
            "Sending several fields at once and being unable to say which one changed the object",
            "Testing against a record you do not own, which turns a probe into an unauthorized change",
            "Reading a 400 as an authorization success when it may only be schema validation",
        ],
        "done_when": [
            "A reserved field and a permitted control each have a single-field result recorded",
            "The rejection class is recorded as authorization, validation, or neither",
        ],
        "refs": [
            "[OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)",
            "[CWE-269 - Improper privilege management](https://cwe.mitre.org/data/definitions/269.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "nested-and-dotted-key-injection",
        "title": "Nested and Dotted Key Injection",
        "summary": "Test whether a bracketed or dotted key path reaches a nested field the flat schema does not expose, since a parser that maps key paths can write where the schema never declared anything",
        "use_when": "the parser accepts a structured body and nested key paths have not been exercised",
        "avoid_when": "the parser flattens nothing and a test confirms a dotted key is rejected as unknown",
        "tags": ["probe", "mass-assignment", "parsing"],
        "steps": [
            "Confirm the boundary permits the write and identify the synthetic record you will update.",
            "Send an update using a dotted or bracketed key that targets a nested field not in the schema.",
            "Read the object back, including its nested structure, and compare against the captured state.",
            "Try one alternate notation to see whether the mapping is notation-specific or general.",
            "Record which notation reached the nested field, and the path it wrote to.",
            "Note whether the flat equivalent of the same field is rejected, since the difference is the finding.",
        ],
        "signals": [
            "A dotted key writes to a nested field while the flat equivalent is rejected",
            "Bracket notation reaches a field the schema declares nowhere",
            "The stored object gains a key containing a literal dot rather than nesting",
            "A control flat unknown key is rejected while the notated one is accepted",
        ],
        "patterns": [
            (
                "Notation pair",
                "flat: {internal.flag: true} -> rejected, stored unchanged\nbracket: {internal[flag]: true} -> stored under a nested path",
            ),
            (
                "Read-back rule",
                "read the whole object including nested keys, because a notation can either nest the value or store a literal dotted key",
            ),
            (
                "Control note",
                "the flat unknown key is the control that proves the rejection policy exists for one form but not the other",
            ),
        ],
        "pitfalls": [
            "Testing only one notation and concluding the whole class is safe",
            "Not distinguishing a stored literal dotted key from a nested field",
            "Omitting the flat control, which is what makes the difference visible",
        ],
        "done_when": [
            "At least two notations are tested with read-back results recorded for each",
            "A flat control result is recorded alongside the notated attempts",
        ],
        "refs": [
            "[CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)",
            "[OWASP - Input validation guidance](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "type-coercion-in-write-path",
        "title": "Type Coercion in Write Path",
        "summary": "Check whether a value of the wrong type is coerced rather than rejected, because a coerced boolean or number changes what a later authorization check actually tests",
        "use_when": "the write path accepts values whose types have not been exercised against the parser's coercion rules",
        "avoid_when": "the schema is strict about types and a test confirms an out-of-range type is rejected",
        "tags": ["probe", "coercion", "validation"],
        "steps": [
            "List the typed fields on the write path: booleans, numbers, enumerations and identifiers.",
            "For each, send one value of a different type on a synthetic record you own and read the object back.",
            "Record whether the value was rejected, stored as sent, or coerced into the declared type.",
            "For coercions, record the rule observed: string to number, truthy string to boolean, array to single value.",
            "Check whether the coerced value would change a downstream decision such as a feature check.",
            "Record a coercion table with one row per field and its observed behaviour.",
        ],
        "signals": [
            "A string such as a word is accepted for a boolean field and stored truthy",
            "A numeric field accepts a string and stores it without conversion",
            "An array is accepted where a scalar is declared and later truncated",
            "A coerced value changes a feature or authorization decision downstream",
        ],
        "patterns": [
            (
                "Coercion table",
                "field | type declared | value sent | result\nactive | boolean | \"no\" | stored true  <- truthy coercion\nquantity | integer | \"12\" | stored 12\nrole | enum | [\"admin\"] | stored admin",
            ),
            (
                "Downstream check",
                "after a coercion, record whether the coerced value reaches a decision; a stored-but-unused field is far lower impact",
            ),
            (
                "Rule naming",
                "write the observed coercion rule in words, since the report needs the rule rather than a single example",
            ),
        ],
        "pitfalls": [
            "Recording a coercion without checking whether anything downstream consumes the value",
            "Testing one type per class and missing the specific type that changes a decision",
            "Attributing a rejection to validation when the parser rejected it earlier in the chain",
        ],
        "done_when": [
            "A coercion table records declared type, value sent and result for each typed field",
            "At least one coercion is traced to its downstream decision, or recorded as unused",
        ],
        "refs": [
            "[CWE-704 - Incorrect type conversion](https://cwe.mitre.org/data/definitions/704.html)",
            "[OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "default-value-override-probe",
        "title": "Default Value Override Probe",
        "summary": "Attempt to set a field to the value the server assigns by default, because a default that a client can pin is a default the server never actually enforces",
        "use_when": "server-assigned defaults exist on the write path and client ability to supply them is unconfirmed",
        "avoid_when": "defaults are computed after assignment and a test confirms a client value is overwritten",
        "tags": ["probe", "defaults", "mass-assignment"],
        "steps": [
            "List the fields the server assigns by default: status, owner, timestamps and counters.",
            "Send an update supplying one of those fields with a value of your choosing on a record you own.",
            "Read the object back and record whether your value survived or was overwritten by the default.",
            "Test one field where overwriting matters, such as a status or an ownership field.",
            "Record which defaults are client-overridable and which are enforced server-side.",
            "Note whether an overridable default would change a downstream decision.",
        ],
        "signals": [
            "A client-supplied status survives where the server normally assigns one",
            "An ownership or creator field can be pinned to a value the client chose",
            "A timestamp is accepted from the client rather than generated on the server",
            "A counter or balance field accepts a client-supplied starting value",
        ],
        "patterns": [
            (
                "Override table",
                "field | default | client value sent | result\nstatus | draft | active | stored active  <- overridden\ncreated_by | server | other-user | stored other-user\nid | server | client-value | rejected",
            ),
            (
                "Enforcement split",
                "defaults split into enforced (server wins) and overridable (client wins); the split is the reportable structure",
            ),
            (
                "Decision check",
                "for each overridable default, state what downstream decision it would influence, or record it as cosmetic",
            ),
        ],
        "pitfalls": [
            "Testing only a cosmetic default while an ownership default is also overridable",
            "Reporting an overridable field that nothing consumes as though it were a state change",
            "Not comparing against the enforced defaults, which is what shows the inconsistency",
        ],
        "done_when": [
            "Each default field has a record of client value sent and the stored result",
            "The enforced and overridable split is stated, with downstream effect noted per field",
        ],
        "refs": [
            "[CWE-915 - Improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)",
            "[OWASP - Mass assignment guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "batch-write-single-record-scope",
        "title": "Batch Write Single-Record Scope",
        "summary": "Send a batch containing many entries and one that differs from the rest, because a batch that mutates as a unit can change records you never intended to touch",
        "use_when": "the API accepts an array or batch of items for a write operation",
        "avoid_when": "each batch item is processed independently and a test confirms partial failure isolates correctly",
        "tags": ["probe", "batch", "writes"],
        "steps": [
            "Confirm the boundary permits batch writes and identify the rollback for the whole batch.",
            "Send a small batch where one item is intentionally different from the others on records you own.",
            "Read back every record in the batch and record which items were applied and which were not.",
            "Check whether the response reports per-item results or only an overall status.",
            "Determine whether the batch is atomic: all applied, or none applied, or a partial state.",
            "Record the batch's atomicity, reporting granularity and any item that behaved differently.",
        ],
        "signals": [
            "A partial failure applies some items and reports only an overall success",
            "One item in the batch is processed differently from the rest with no per-item status",
            "The batch is neither atomic nor reported per item, leaving a partial state invisible",
            "An item's result cannot be determined from the response at all",
        ],
        "patterns": [
            (
                "Batch record",
                "items: 3 (2 same, 1 different) | response: overall 200 | read-back: 3 applied | per-item status: absent | atomicity: none observed",
            ),
            (
                "Partial-state rule",
                "the interesting outcome is a partial application with an overall success response; that pairing is what the report states",
            ),
            (
                "Reporting gap",
                "no per-item status means a caller cannot tell which items failed, recorded as its own finding",
            ),
        ],
        "pitfalls": [
            "Reporting an overall status as proof every item succeeded without reading each record back",
            "Making a batch too large to attribute an effect to a single item",
            "Overlooking that a partial state may persist because nothing rolls it back",
        ],
        "done_when": [
            "Every item in the test batch has a read-back result recorded",
            "Atomicity and per-item reporting are each stated explicitly",
        ],
        "refs": [
            "[OWASP - API security guidance](https://owasp.org/API-Security/)",
            "[CWE-841 - Improper enforcement of behavioral workflow](https://cwe.mitre.org/data/definitions/841.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "filter-parameter-injection",
        "title": "Filter Parameter Injection",
        "summary": "Add a filter or query parameter the endpoint does not document and observe whether it narrows or widens the result set, because an unvalidated filter changes who sees which rows",
        "use_when": "an endpoint returns a filtered list and its parameter handling has not been exercised",
        "avoid_when": "a strict allow-list of parameters is enforced and a test confirms unlisted ones are rejected",
        "tags": ["probe", "filtering", "authorization"],
        "steps": [
            "Capture a baseline list response for a record set you are allowed to read, noting the count and field set.",
            "Add one undocumented filter parameter and record whether the result set changes.",
            "Try a filter that would widen access, such as one targeting a tenant or owner field.",
            "Record the status, the count delta and whether the parameter appears in the response or an error.",
            "Check whether the filter is applied in the query rather than after fetching, since that affects scale behaviour too.",
            "Record each parameter with accepted, rejected or ignored as its verdict.",
        ],
        "signals": [
            "An undocumented filter parameter changes the returned count",
            "A filter targeting an ownership or tenant field is accepted",
            "The parameter is applied after rows are fetched rather than in the query",
            "An invalid filter value produces an error that echoes the query structure",
        ],
        "patterns": [
            (
                "Parameter verdict",
                "param | value | count before | count after | verdict\n(sort unspecified) | default | 20 | 20 | baseline\ninclude_internal | true | 20 | 27 | accepted, widened\nowner_id | other | 20 | 0 | accepted, filtered by ownership",
            ),
            (
                "Widen-versus-narrow",
                "record whether the parameter widened or narrowed the set; widening is the direction that changes who sees what",
            ),
            (
                "Application point",
                "note whether filtering happens in the query or in application code, since a post-fetch filter has a scale consequence as well",
            ),
        ],
        "pitfalls": [
            "Adding several parameters at once and losing which one changed the count",
            "Testing only narrowing filters when widening is the direction that matters",
            "Missing that a filter changed nothing because the parameter needs a different name",
        ],
        "done_when": [
            "Each undocumented parameter has an accepted, rejected or ignored verdict with count delta",
            "Whether the filter widens or narrows access is stated per parameter",
        ],
        "refs": [
            "[OWASP - API4 unrestricted resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)",
            "[CWE-639 - Authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "ordering-and-pagination-boundary",
        "title": "Ordering and Pagination Boundary",
        "summary": "Push ordering and pagination to their edges, because an unbounded page or an orderable column is both a resource question and a way to read rows the default view hides",
        "use_when": "an endpoint returns a list that supports pagination or ordering parameters",
        "avoid_when": "limits are clamped server-side and a test confirms out-of-range values are refused",
        "tags": ["probe", "pagination", "resources"],
        "steps": [
            "Record the default page size and ordering the endpoint applies with no parameters.",
            "Request a page size above the maximum and record whether it is clamped, rejected or honoured.",
            "Request an offset or cursor beyond the end of the data and record the response rather than assuming one.",
            "Try ordering by a column that is not documented as orderable, including an internal or joined field.",
            "Measure the response time for an extreme page size against the baseline you already captured.",
            "Record limits, clamping and orderable columns with the timing you observed.",
        ],
        "signals": [
            "An out-of-range page size is honoured instead of clamped",
            "Ordering by an undocumented or joined column succeeds",
            "An out-of-range offset returns a different error shape than a bad parameter",
            "Response time grows sharply with page size beyond what the baseline suggests",
        ],
        "patterns": [
            (
                "Boundary table",
                "parameter | default | extreme sent | result\npage_size | 20 | 100000 | honoured, 2.4s baseline 0.2s\noffset | 0 | 999999999 | empty 200\nsort | created_at | internal_score | accepted",
            ),
            (
                "Clamp-versus-reject",
                "record which behaviour applies: clamp is usually acceptable, honour is the finding, reject is strictest",
            ),
            (
                "Timing note",
                "extreme values get a timing recorded against the baseline, since an unbounded page is partly a resource finding",
            ),
        ],
        "pitfalls": [
            "Reporting only the pagination logic while the ordering parameter exposes a joined column",
            "Testing one extreme and missing both the clamp and the reject behaviours",
            "Quoting a slow response without the baseline it was compared against",
        ],
        "done_when": [
            "Page size, offset and sort each have an extreme-value result with a recorded outcome",
            "Clamp, reject or honour is stated per parameter with timing against baseline",
        ],
        "refs": [
            "[OWASP - API4 unrestricted resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)",
            "[CWE-770 - Allocation of resources without limits](https://cwe.mitre.org/data/definitions/770.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "sort-and-search-field-reach",
        "title": "Sort and Search Field Reach",
        "summary": "Check which fields sorting and free-text search can reach, since a search over a field the list never shows returns rows the caller was never meant to select",
        "use_when": "the endpoint supports a search term or a sort field and the reachable column set is unconfirmed",
        "avoid_when": "search and sort operate over a documented field allow-list enforced server-side",
        "tags": ["probe", "search", "exposure"],
        "steps": [
            "Capture a baseline result set for a search term that matches nothing, so the empty state is known.",
            "Search for a value that exists only in a field the response never returns and record whether rows come back.",
            "Sort by an undocumented field and record whether ordering changes as evidence the field was used.",
            "Check whether an error from a malformed sort or search term leaks column or query detail.",
            "Compare the searched field set against the response field set from the exposure map.",
            "Record each searched or sorted field with reachable, rejected or ignored as its verdict.",
        ],
        "signals": [
            "Searching a hidden field returns rows, proving the field is reachable",
            "Sorting by an undocumented column changes the result order",
            "A malformed sort term produces an error naming a column or a query fragment",
            "Search reaches fields outside the response schema entirely",
        ],
        "patterns": [
            (
                "Reach verdict",
                "field | in response | searchable | sortable | evidence\nemail | no | yes | no | rows returned for known value\ninternal_score | no | no | yes | order changed",
            ),
            (
                "Baseline empty",
                "a term matching nothing gives the empty-state shape, which is what a later error or leak is compared against",
            ),
            (
                "Error check",
                "a malformed sort term that names a column in its error is recorded as disclosure in its own right",
            ),
        ],
        "pitfalls": [
            "Testing search while never checking sort, which often reaches further",
            "Recording a leak without the baseline empty response to show the error is new",
            "Assuming a field is unreachable because it is absent from the response",
        ],
        "done_when": [
            "Each searched and sorted field has a reachable, rejected or ignored verdict with evidence",
            "A baseline empty-result response exists for comparison against errors",
        ],
        "refs": [
            "[OWASP - API3 broken object property level authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)",
            "[CWE-200 - Exposure of sensitive information](https://cwe.mitre.org/data/definitions/200.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "error-triggering-for-shape-disclosure",
        "title": "Error Triggering for Shape Disclosure",
        "summary": "Trigger controlled errors and read what the shape discloses, because an error that names a field, a query or a stack is an exposure no input-side check will catch",
        "use_when": "the error map exists and the leakage question has not been examined per shape",
        "avoid_when": "every error returns one uniform shape with only a correlation id",
        "tags": ["probe", "errors", "disclosure"],
        "steps": [
            "Choose controlled triggers: unknown identifier, malformed body, unsupported method and an authorization failure.",
            "Send each at the agreed rate and capture status, body and timing against the error map baseline.",
            "Compare shapes for disclosure: field names, query structure, internal identifiers, stack frames or versions.",
            "Check whether the same condition yields different shapes in different environments, which the delta should explain.",
            "Record which disclosures are externally visible as opposed to appearing only in server logs.",
            "Record a leakage table with one row per trigger and the markers it exposes.",
        ],
        "signals": [
            "An error body names an internal field or a query fragment",
            "A stack trace or a version string appears in a response",
            "Two environments return different shapes for the same trigger",
            "Diagnostic detail intended for operators is returned to the caller",
        ],
        "patterns": [
            (
                "Leakage table",
                "trigger | status | marker | leaks | external\nunknown id | 404 | {code} | nothing | yes\nbad body | 400 | field names list | schema | yes\nunhandled | 500 | stack frames | internals | yes",
            ),
            (
                "Visibility column",
                "external marks what a caller sees; a marker only in server logs is an operator concern, not a disclosure finding",
            ),
            (
                "Baseline comparison",
                "each shape is compared against the map captured earlier, so a difference is recognisable as a difference",
            ),
        ],
        "pitfalls": [
            "Reporting operator log detail as an external leak without checking where it appeared",
            "Comparing shapes across environments and blaming the application for a debug setting",
            "Triggering errors that create load rather than choosing controlled, bounded ones",
        ],
        "done_when": [
            "Each controlled trigger has a recorded status, marker and visibility",
            "Disclosures are split into externally visible and server-log-only",
        ],
        "refs": [
            "[CWE-209 - Generation of error message containing sensitive information](https://cwe.mitre.org/data/definitions/209.html)",
            "[OWASP - Error handling guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "debug-endpoint-exposure",
        "title": "Debug Endpoint Exposure",
        "summary": "Look for framework debug, health and introspection routes reachable without the authentication the rest of the API requires",
        "use_when": "the route inventory includes debug, metrics, health or introspection paths",
        "avoid_when": "those routes are all behind authentication and a test confirms a rejection for each",
        "tags": ["probe", "debug", "routes"],
        "steps": [
            "List every debug, metrics, health, and introspection path from the route inventory.",
            "Request each without credentials and record status, body and timing against the baseline.",
            "For any that answer, record which fields the body exposes: configuration, routes, versions or environment.",
            "Check whether the environment delta explains the exposure, since debug routes often follow a debug flag.",
            "Note whether these paths are excluded from logging while others are logged.",
            "Record each path with reachable, rejected or absent as its verdict, plus what a reachable one disclosed.",
        ],
        "signals": [
            "A debug or introspection route answers without authentication",
            "A metrics endpoint reveals internal names, counts or versions",
            "An unauthenticated route returns configuration detail absent from normal responses",
            "A debug path is excluded from the access log",
        ],
        "patterns": [
            (
                "Route verdict",
                "path | auth required | status | discloses | in log\n/debug/routes | no | 200 | full route table | no\n/metrics | no | 200 | version and counts | yes\n/health | no | 200 | nothing sensitive | yes",
            ),
            (
                "Environment link",
                "tie each exposure back to the environment delta, since a debug route enabled by a flag is a configuration finding",
            ),
            (
                "Logging note",
                "record whether the path is logged; an unlogged debug route is a second finding on the same path",
            ),
        ],
        "pitfalls": [
            "Reporting a health endpoint as exposed without saying what it actually disclosed",
            "Missing that a debug route is gated by an environment flag rather than by authentication",
            "Ignoring that the route may be excluded from logs, which changes the response",
        ],
        "done_when": [
            "Every debug and introspection path has a verdict with what it disclosed if reachable",
            "Each exposure is linked to the environment delta and its logging status",
        ],
        "refs": [
            "[OWASP - Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)",
            "[CWE-489 - Active debug code](https://cwe.mitre.org/data/definitions/489.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "content-type-parser-selection",
        "title": "Content-Type Parser Selection",
        "summary": "Vary the declared content type with identical bytes, because the parser the header selects decides which validation and which unknown-field policy your request actually gets",
        "use_when": "the endpoint accepts more than one content type or falls back when the header is absent",
        "avoid_when": "one content type is accepted and others are rejected before parsing",
        "tags": ["probe", "content-type", "parsing"],
        "steps": [
            "Send the same logical body under each accepted content type and with the header omitted entirely.",
            "Capture status, body and which handler or parser the response suggests ran.",
            "Include the unknown-field probe under each parser, since policies may differ between them.",
            "Note whether an unexpected type routes to a different handler with its own validation step.",
            "Rank each case by whether a real client can produce it, since that decides practical relevance.",
            "Record a table of declared type, status, parser and validation outcome.",
        ],
        "signals": [
            "Omitting the content type falls back to a parser with weaker validation",
            "Two parsers treat the same unknown field differently",
            "An unexpected type reaches a handler that does not validate as strictly",
            "The same bytes produce different results under two declared types",
        ],
        "patterns": [
            (
                "Parser table",
                "declared type | status | parser | unknown field | validated\napplication/json | 200 | json | rejected | yes\nabsent | 200 | fallback | accepted | no  <- finding\ntext/plain | 415 | none | n/a | n/a",
            ),
            (
                "Bytes-identical rule",
                "hold body bytes constant across cases so the only variable is the header the framework reads",
            ),
            (
                "Client-reality column",
                "rank each row by whether a real client produces it; a case no client can produce is lower risk, not zero risk",
            ),
        ],
        "pitfalls": [
            "Changing the body along with the header, which destroys attribution",
            "Ranking a fallback path as critical when no client can trigger it, or as harmless when any client can",
            "Missing that the fallback parser applies a different unknown-field policy",
        ],
        "done_when": [
            "Every accepted and absent content type has a status, parser and validation outcome recorded",
            "Each row notes whether a real client can produce that case",
        ],
        "refs": [
            "[CWE-436 - Interpretation conflict](https://cwe.mitre.org/data/definitions/436.html)",
            "[IETF RFC 9110 - Content-Type semantics](https://www.rfc-editor.org/rfc/rfc9110)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "duplicate-field-key-confusion",
        "title": "Duplicate Field Key Confusion",
        "summary": "Send the same field twice with different values and see which one wins, because two parsers disagreeing on which value to take is a decision made without anyone deciding",
        "use_when": "the body can contain a repeated key and precedence has not been observed",
        "avoid_when": "a strict parser rejects duplicate keys and a test confirms it",
        "tags": ["probe", "parsing", "confusion"],
        "steps": [
            "Send a permitted update containing one field name twice with two different values on a record you own.",
            "Read the object back and record which of the two values was stored.",
            "Repeat with the two values swapped to see whether the rule is first-wins, last-wins or something else.",
            "If a gateway or proxy sits in front, note whether it may normalize the body before the application sees it.",
            "Check whether an authorization decision would depend on which value is taken.",
            "Record the precedence rule observed, with both orders tested.",
        ],
        "signals": [
            "One value wins and the application takes a different one from what a client would assume",
            "Swapping the order changes which value is stored",
            "The gateway and the application disagree about which value is present",
            "An authorization-relevant field is subject to the ambiguity",
        ],
        "patterns": [
            (
                "Precedence record",
                "field sent twice: {a: 1, a: 2} -> stored 2 (last wins)\nreversed: {a: 2, a: 1} -> stored 1; rule: last-wins, confirmed by both orders",
            ),
            (
                "Layer question",
                "if a gateway rewrites the body, record whether it preserves duplicates, because the application may never see the pair you sent",
            ),
            (
                "Decision flag",
                "mark any precedence ambiguity on a field that reaches an authorization or state decision as the higher-impact case",
            ),
        ],
        "pitfalls": [
            "Sending both values in one order and assuming a rule without the reverse test",
            "Attributing the outcome to the application when a gateway normalized the body first",
            "Reporting ambiguity on a field nothing consumes while a decision-relevant field goes untested",
        ],
        "done_when": [
            "Both orderings of a duplicate key have a recorded stored value",
            "The precedence rule is stated, and any decision-relevant field is flagged",
        ],
        "refs": [
            "[CWE-436 - Interpretation conflict](https://cwe.mitre.org/data/definitions/436.html)",
            "[OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "partial-update-omission-behavior",
        "title": "Partial Update Omission Behavior",
        "summary": "Establish what an omitted field does during a partial update, because an omission that resets to default is a mutation the caller never asked for",
        "use_when": "the API supports partial updates and the semantics of omitted fields are unconfirmed",
        "avoid_when": "omitted fields are documented as unchanged and a test confirms the stored value survives",
        "tags": ["probe", "patch", "state"],
        "steps": [
            "Capture the full state of a synthetic record you own before the update.",
            "Send a partial update touching one field while omitting several others.",
            "Read the record back and compare every field against the captured state, not only the one you sent.",
            "Identify any omitted field that changed, reset or lost precision as a side effect.",
            "Repeat once with a different subset omitted to confirm the behaviour is about omission rather than the field.",
            "Record which fields are preserved, reset or recomputed on omission.",
        ],
        "signals": [
            "An omitted field resets to a default rather than keeping its value",
            "A numeric or precision-bearing field changes when it was not mentioned",
            "A nested object is replaced wholesale when only a sibling field was updated",
            "The behaviour differs between two subsets of omitted fields",
        ],
        "patterns": [
            (
                "Diff record",
                "before: {a: 1, b: 2, c: 3}\nupdate: {b: 9}\nafter:  {a: 1, b: 9, c: 0}  <- omitted c reset",
            ),
            (
                "Full-diff rule",
                "compare every field rather than only the one you sent; the side effect is on a field you did not touch",
            ),
            (
                "Subset repeat",
                "a second omission subset separates a field-specific behaviour from a general omission rule",
            ),
        ],
        "pitfalls": [
            "Checking only the field that was sent, which is exactly how a reset goes unnoticed",
            "Attributing a reset to the update when it was caused by a server-side recompute",
            "Concluding safe behaviour from one subset and never varying it",
        ],
        "done_when": [
            "Every field on the record is diffed before and after the partial update",
            "Preserved, reset and recomputed fields are listed with a confirming second subset",
        ],
        "refs": [
            "[RFC 5789 - PATCH method for HTTP](https://www.rfc-editor.org/rfc/rfc5789)",
            "[CWE-642 - External control of critical state data](https://cwe.mitre.org/data/definitions/642.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "enum-and-range-boundary-probe",
        "title": "Enum and Range Boundary Probe",
        "summary": "Send values at and just outside each declared enumeration and range, because a boundary enforced on the documented edge but not past it is where an unexpected state enters",
        "use_when": "fields declare enumerations or numeric ranges that have not been exercised at their edges",
        "avoid_when": "the schema enforces bounds strictly and an out-of-range test confirms rejection",
        "tags": ["probe", "validation", "boundaries"],
        "steps": [
            "List enumerated and ranged fields with their documented boundaries.",
            "For each, send the maximum in-range value, the value just outside it, and one clearly invalid value.",
            "Read the object back and record accepted, rejected or coerced for each case.",
            "Check whether an out-of-range value is clamped into range, which silently changes what was requested.",
            "For enumerations, test a value that is plausible but undeclared rather than an obviously invalid string.",
            "Record a boundary table with one row per field and its three test cases.",
        ],
        "signals": [
            "A value just outside the documented range is accepted",
            "An out-of-range value is clamped rather than rejected",
            "An undeclared but plausible enumeration value is accepted",
            "The documented boundary differs from the enforced one",
        ],
        "patterns": [
            (
                "Boundary table",
                "field | declared | max in-range | just outside | invalid\nquantity | 1..100 | 100 ok | 101 stored 101 | 0 rejected\nstate | draft|active|paid | paid ok | refunded accepted | xyz rejected",
            ),
            (
                "Clamp flag",
                "a clamped value is recorded separately from an accepted one, because the caller asked for something else than what was stored",
            ),
            (
                "Plausible-enum rule",
                "test an undeclared value that looks legitimate, since a clearly invalid string is usually caught by the most basic check",
            ),
        ],
        "pitfalls": [
            "Testing only a clearly invalid value while the plausible undeclared one passes",
            "Recording a clamp as an acceptance, which hides that stored state differs from the request",
            "Not comparing the documented boundary with the enforced one",
        ],
        "done_when": [
            "Each enumerated or ranged field has three boundary cases with a result",
            "Clamped values are distinguished from accepted ones in the table",
        ],
        "refs": [
            "[CWE-1284 - Improper validation of specified quantity in input](https://cwe.mitre.org/data/definitions/1284.html)",
            "[OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "concurrent-write-interleaving",
        "title": "Concurrent Write Interleaving",
        "summary": "Issue two writes to the same record together and read the result, because an unguarded update lets the later write silently discard the earlier one",
        "use_when": "the API permits concurrent updates to one record and the interleaving behaviour is unconfirmed",
        "avoid_when": "an optimistic locking or version field is enforced and a test confirms a conflict is rejected",
        "tags": ["probe", "concurrency", "state"],
        "steps": [
            "Confirm the boundary permits concurrent requests and that a rollback exists for the record.",
            "Capture the record's state, then send two updates touching different fields at the same time.",
            "Read the record back and record whether both changes survived or one was lost.",
            "Repeat if the first attempt happened to serialize by timing, since a clean result may just be luck.",
            "Check for a version, etag or updated-at guard in the request and response.",
            "Record the observed behaviour as guarded, lost update, or serialized by timing with evidence.",
        ],
        "signals": [
            "Two updates to different fields result in only one surviving",
            "No version or etag guard appears in the request or response contract",
            "The record's updated-at is identical after two logically separate writes",
            "A repeat of the test yields a different outcome, indicating timing dependence",
        ],
        "patterns": [
            (
                "Interleaving record",
                "write A {field1} and write B {field2} sent together -> read-back: field1 unchanged, field2 applied; verdict: lost update",
            ),
            (
                "Guard check",
                "look for version, etag or updated-at in both directions; absence is recorded as no guard rather than as safe by default",
            ),
            (
                "Repeat rule",
                "a single clean run may be serialization by luck; repeat enough times to state the behaviour honestly",
            ),
        ],
        "pitfalls": [
            "Concluding safe behaviour from one run that happened to serialize",
            "Changing two fields in one request rather than issuing two requests",
            "Reporting a lost update without noting whether a guard field exists but was not supplied",
        ],
        "done_when": [
            "Two concurrent writes have a recorded read-back showing which changes survived",
            "The presence or absence of a version guard is stated, with repeats to rule out luck",
        ],
        "refs": [
            "[CWE-362 - Concurrent execution using shared resource with improper synchronization](https://cwe.mitre.org/data/definitions/362.html)",
            "[OWASP - Race condition guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "idempotency-key-handling",
        "title": "Idempotency Key Handling",
        "summary": "Replay one request with the same idempotency key and compare the effects, because a key that is recorded but not enforced produces a duplicate every retry",
        "use_when": "the API accepts an idempotency key or a client-generated identifier for a create operation",
        "avoid_when": "a test confirms a replayed key returns the original result without a second effect",
        "tags": ["probe", "idempotency", "concurrency"],
        "steps": [
            "Confirm the boundary permits the create operation and identify its rollback.",
            "Send a create with a client-generated key and record the response and the created record.",
            "Replay the identical request with the same key and record the response and any second record.",
            "Compare the two responses and the resulting object count to determine whether the effect repeated.",
            "Send a third request with the same key but a changed body to see which of the two the server honours.",
            "Record the key's behaviour: enforced, recorded but not enforced, or ignored.",
        ],
        "signals": [
            "A replay with the same key creates a second object",
            "The key is recorded in logs or responses but does not suppress the effect",
            "A changed body with a reused key is processed rather than rejected",
            "The response to a replay differs from the original with no explanation",
        ],
        "patterns": [
            (
                "Replay record",
                "request 1 key K -> 201, object A\nrequest 2 key K same body -> 201, object B  <- effect repeated\nrequest 3 key K changed body -> 201, object C",
            ),
            (
                "Three-request rule",
                "the third request with a changed body is what distinguishes a key that is ignored from one that is enforced but keyed only on the body",
            ),
            (
                "Count evidence",
                "object count after each replay is the evidence; record it beside the status codes rather than relying on status alone",
            ),
        ],
        "pitfalls": [
            "Judging enforcement from the status code when a second object was created anyway",
            "Replaying a request the boundary forbids for this operation",
            "Skipping the changed-body case, which is what separates ignored from enforced",
        ],
        "done_when": [
            "Three requests with one key have recorded responses and object counts",
            "The key is labelled enforced, recorded but not enforced, or ignored",
        ],
        "refs": [
            "[CWE-841 - Improper enforcement of behavioral workflow](https://cwe.mitre.org/data/definitions/841.html)",
            "[OWASP - Race condition guidance](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "rate-limit-enforcement-observation",
        "title": "Rate Limit Enforcement Observation",
        "summary": "Observe which requests the rate limiter counts and which it lets through, because a limit enforced on the wrong key protects nothing while still appearing configured",
        "use_when": "a rate limiter is documented or configured but its enforcement key has not been observed",
        "avoid_when": "the limiter's key and behaviour are documented and a test confirms them",
        "tags": ["probe", "rate-limit", "resources"],
        "steps": [
            "Record the documented limit, its window and the key it is said to use, before sending anything.",
            "Send requests within your own budget until a limit or a header appears, staying under the boundary ceiling.",
            "Read the limit headers to learn remaining, reset and the key the server appears to count by.",
            "Vary one dimension between requests to see whether the counter follows identity, ip, or neither.",
            "Record whether an unauthenticated request shares a counter with an authenticated one.",
            "State the enforcement key you observed alongside the documented one, and any difference.",
        ],
        "signals": [
            "The enforced key differs from the documented one",
            "Authenticated and unauthenticated requests share one counter",
            "The limiter counts only successful responses, so failed requests are unbounded",
            "No limit headers appear at all, leaving enforcement unobservable",
        ],
        "patterns": [
            (
                "Enforcement record",
                "documented: per api key, 100/min | observed: headers show counter shared across identities | verdict: enforced by ip, not by key",
            ),
            (
                "Header read",
                "remaining, reset and limit headers recorded per response; their absence is recorded too, since it means enforcement is unobservable",
            ),
            (
                "Boundary check",
                "the test stays inside your own rate budget, because proving a limit by exceeding it breaches the ceiling you agreed",
            ),
        ],
        "pitfalls": [
            "Exceeding your own rate budget to prove that a limit exists",
            "Assuming the documented key is the enforced one without varying a dimension",
            "Reporting a missing limiter when it is simply not observable from headers",
        ],
        "done_when": [
            "The documented and observed enforcement keys are both recorded with the evidence",
            "Limit headers, or their absence, are captured for each request class tested",
        ],
        "refs": [
            "[OWASP - API rate limiting guidance](https://owasp.org/API-Security/)",
            "[CWE-770 - Allocation of resources without limits](https://cwe.mitre.org/data/definitions/770.html)",
        ],
        "meta": {"phase": "probe"},
    },
    {
        "slug": "cache-and-vary-invalidation-on-write",
        "title": "Cache and Vary Invalidation on Write",
        "summary": "Check whether a write invalidates the cached reads it should, because a stale read after a mutation is a correctness defect that only appears when you look",
        "use_when": "responses can be cached and writes update the same data the cache serves",
        "avoid_when": "the owner confirms no caching layer exists between client and origin for these paths",
        "tags": ["probe", "caching", "state"],
        "steps": [
            "Capture a read of a synthetic record and note any caching headers in the response.",
            "Perform a permitted write to that record and record the write response.",
            "Repeat the read immediately and compare the returned state against the write you just made.",
            "Record whether the read came from cache, using the status headers, and how stale it was.",
            "Check whether the vary dimensions would let another client receive the stale copy.",
            "Record the invalidation behaviour as immediate, delayed with a measured window, or absent.",
        ],
        "signals": [
            "A read after a write returns the pre-write state",
            "The stale read carries a cache status showing it was served from storage",
            "No vary dimension separates clients, so the stale copy can reach another caller",
            "Invalidation happens only after a delay long enough to observe",
        ],
        "patterns": [
            (
                "Sequence record",
                "read -> cached | write -> 200 | read again -> stale, status hit, age 12s; verdict: invalidation absent",
            ),
            (
                "Window measure",
                "when invalidation is delayed, record the observed window so the report gives a number rather than a word",
            ),
            (
                "Vary note",
                "state whether vary dimensions would isolate clients, since that decides whether staleness stays yours or spreads",
            ),
        ],
        "pitfalls": [
            "Reporting staleness without confirming the second read was actually cached",
            "Attributing staleness to the application when a downstream layer holds the copy",
            "Ignoring that your own client may have cached, which is not the server's defect",
        ],
        "done_when": [
            "A read-write-read sequence has all three recorded states with cache status",
            "Invalidation is labelled immediate, delayed with a window, or absent",
        ],
        "refs": [
            "[IETF RFC 9111 - HTTP caching](https://www.rfc-editor.org/rfc/rfc9111)",
            "[OWASP - Cache-related testing](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "probe"},
    },
]