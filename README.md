# Book Review Database App

![CI](https://github.com/dagron27/book-review-database-app/actions/workflows/ci.yml/badge.svg)

**Course:** `CSCI 411, Database Theory and Design, Fall 2025`

**Assignment:** `csci-411-assignment2`

## Assignment Intent

Students were given a starter project (`sqlite_books_web_example`, Week 5
course material) -- a minimal Flask + SQLite book-listing app -- and asked
to extend it in two graded ways:

1. **(5 points) Search books by year.** Add a textbox and button to the
   page, a JavaScript handler, and a server-side route. **Confirmed
   implemented**: `searchBooksByYear()` in `src/static/script.js` calls
   `GET /api/books/<int:year>`, handled by `get_books_by_year()` in
   `src/app.py`.
2. **(5 points) Add a `user_account` table with a relationship to `users`,
   and update the application to display username/email and all of that
   user's reviews when the account link is clicked.** This one is worth
   spelling out precisely, because the repository's state doesn't tell a
   single simple story:
   - The **data-model half is fully intact**: `data/script.sql` defines
     `user_account` with a foreign key to `Users`, and the committed
     `data/books.db` actually has the table created and populated (one row:
     `user_account_id=1, user_id=1`). This was never touched.
   - The **application half** (the route and page that display it) was
     briefly **removed** during an earlier security-hardening pass on this
     repository, because it served that data with no authentication of any
     kind. After confirming against the actual assignment text that this
     was the graded, intended feature -- not an accidental exposure -- it
     was **restored**. The endpoint still has no login system, by design:
     the assignment never asked for one, and this is a local coursework
     demo, not a live multi-user service. See "Security Findings" below for
     why that's an accepted characteristic of the original assignment
     scope rather than an unresolved vulnerability.

The assignment also required a short screen-recorded video showing the new
code in `index.html`, `script.js`, and `src/app.py` (no source code submission
required) -- a submission-process detail this repository can't speak to on
its own. Development was iterative in practice; that process isn't visible
in this archive since no commit history was preserved.

Per the base starter project and the schema/data files described above,
this is a **SQLite-backed** application throughout -- see `data/books.db`
(the database file itself) and `data/script.sql` (the schema).

## Overview

A small Flask + SQLite web application for adding books, searching books by
year, browsing the full book list, and viewing a single demo user's account
and submitted reviews. The stack is:

- `src/app.py` — Flask application and REST-style API routes
- `data/books.db` — SQLite database file (includes sample seed data)
- `data/script.sql` — schema used to create the database tables
- `src/static/script.js` — client-side logic (fetch calls, DOM rendering)
- `src/static/styles.css` — page styling
- `src/templates/index.html` — the single page served by the app

`docs/database-design.md` has the original table/relationship design
notes from early planning.

There is no evidence this project was ever deployed anywhere; it was built
to run locally.

**This repo has been remediated** for a personal-GitHub push after a prior
security/hygiene audit. See "Known Issues" below for what was fixed, what
remains as an accepted limitation, and the history of the user-account
feature specifically (removed, then restored -- see "Assignment Intent"
above and "Security Findings" below).

## Repository Organization

The original starter project (`sqlite_books_web_example`) had `app.py` at
the repository root alongside a flat `db/` and `static/` layout. This has
been reorganized for portfolio-wide consistency: `app.py`, `templates/`,
and `static/` moved together into `src/` (Flask's template/static
auto-discovery follows `app.py`'s own file location, so moving all three
together preserves it unchanged), and `db/` was renamed to `data/`. The
app is still invoked from the repository root (`python src/app.py`), not
from inside `src/`, so `data/books.db`'s path still resolves correctly.
`.github/workflows/ci.yml` and this README were updated to match.

## Dependencies

Listed in `requirements.txt`: `blinker==1.8.2`, `click==8.1.7`,
`colorama==0.4.6`, `Flask==3.0.3`, `itsdangerous==2.2.0`, `Jinja2==3.1.4`,
`MarkupSafe==2.1.5`, `Werkzeug==3.0.4`.

`requirements.txt` was re-saved as plain UTF-8 (it was previously UTF-16LE
with CRLF line endings, which some Linux/macOS pip versions and CI parsers
choke on). **Fixed.**

## Environment Setup

1. Ensure Python 3 is installed.
2. From the project root, create/activate a virtual environment (the
   previously-committed `venv/` directory has been removed — see Known
   Issues — so create your own with `python -m venv venv`).
3. Install dependencies: `pip install -r requirements.txt`
4. The database already exists at `data/books.db`, built from
   `data/script.sql`. To recreate it from scratch, install your own copy of
   the `sqlite3` CLI (https://www.sqlite.org/download.html) and run
   `.read data/script.sql`. (The `sqlite3.exe`/`sqldiff.exe`/
   `sqlite3_analyzer.exe` binaries formerly committed under this directory
   (then named `db/`) have been removed — see Known Issues.)
5. Run the app: `python src/app.py` (run from the repository root, not from
   inside `src/`, so the `data/books.db` path resolves correctly), or
   `FLASK_APP=src/app.py flask run`. This starts the Werkzeug development
   server on `127.0.0.1:5000`. The interactive debugger is now disabled by
   default (see Known Issues below).

## Known Issues

### Dead Code and Hygiene

- **Broken, unused endpoints** — `GET /api/authors` and `GET /api/reviews`
  in `src/app.py` call `jsonify()` directly on a raw `sqlite3.Row` result
  rather than converting it to a serializable dict/list first. Both
  always raise and return a 500-style JSON error. Neither is called
  anywhere in `src/static/script.js`.
  **Status: not fixed, left as documented limitation.** Out of scope for
  this remediation pass — either remove both routes, or rewrite them to
  build dict lists the same way `get_all_books()` does, and wire up
  frontend calls if the feature is ever actually wanted.

- **Missing write endpoints for most of the schema** — `data/script.sql`
  defines `Authors`, `Users`, `Reviews`, and `book_author` tables, but
  `src/app.py` only ever writes to `Books` (via `add_book`). No routes exist
  to create authors, register users, submit reviews, or link books to
  authors, despite the schema fully supporting all of this.
  **Status: not fixed, left as documented limitation.** Treat as a
  scoping decision for any future work — either add the missing POST
  routes (with proper validation/auth) or drop the unused
  tables/relationships from the schema if this remains a books-only demo.

- **Stray root-level `script.sql`** — a one-line scratch query
  (`select title, count(title) from books group by title`), unrelated to
  the actual schema file at `data/script.sql`.
  **Fixed.** Deleted; nothing in the codebase referenced it. `data/script.sql`
  (the real schema) is untouched.

- **Unused CSS rule** — `.book-container` is defined in
  `src/static/styles.css` but no template or script ever applies that class.
  **Status: not fixed, left as documented limitation.** Low-priority
  cosmetic cleanup, out of scope for this pass.

- **Committed build artifacts** — `venv/` and `__pycache__/` were checked
  into the repo alongside a UTF-16 `requirements.txt`.
  **Fixed.** `venv/` and `__pycache__/` have been deleted from the
  working tree, `requirements.txt` was re-saved as plain UTF-8, and a
  `.gitignore` was added covering `venv/`, `__pycache__/`, `*.pyc`, and
  the (now-removed) SQLite executables so none of this can be
  accidentally re-committed.

- **`docs/Report Part 1.pdf` and `docs/Report Part 2.pdf` -- added, then
  removed as misattributed content.** During portfolio-wide report
  collection these two PDFs were added to `docs/`, found during a PII
  sweep to contain an exposure and remediated (true-redacted via
  PyMuPDF, verified via re-extracted text showing zero remaining hits).
  A closer look afterward showed both files'
  actual content was `movie-database-indexed`'s report (ER diagram,
  `new_movies.db`, Flask movie-database screenshots) -- not content
  specific to this repository at all, evidently attached to the wrong
  repo during collection. **Fixed:** both files were removed rather than
  kept as placeholders once the mismatch was confirmed; `docs/` is now
  empty. No PII exposure remains in this repository as a result (the
  redaction step above happened before the mismatch was discovered, and
  the files are gone either way).

### Security Findings

**CRITICAL — Flask debug mode enabled** (`src/app.py`, `app.run(debug=True)`).
The Werkzeug interactive debugger is a known remote-code-execution vector
if this server is ever exposed on a network reachable by untrusted
users — the debugger's PIN protection is not a reliable safeguard once an
attacker can reach the endpoint.
**Fixed.** `src/app.py` now calls `app.run(debug=False)`.

**HIGH — Stored XSS via unauthenticated "Add a Book" form.**
`src/static/script.js` rendered book titles and review text into the DOM
using `innerHTML` with unescaped template literals in four places:
`searchBooksByYear()`, `displayBooks()`, `showAllBooks()`, and (formerly)
`showUserAccountDetails()`. `src/app.py`'s `add_book()` performs no
sanitization or encoding on the `title` field before inserting it into
`Books`. Because `/api/add_book` is public and unauthenticated, any
visitor could submit a book title containing HTML/JavaScript, which was
then stored and later rendered unescaped to every viewer of the book
list.
**Fixed.** `src/static/script.js` now defines an `escapeHtml()` helper that
entity-encodes `&`, `<`, `>`, `"`, and `'`, and every interpolated
book/review field at the four `innerHTML` call sites is passed through it
before being inserted into the template string. The surrounding HTML
structure is unchanged; only the untrusted text content is now escaped.

**MEDIUM (revised from HIGH) — No authentication on the user-account
view.** `src/app.py`'s `get_user_account()` is hardcoded to
`user_account_id = 1` — there is no session, login, or user-identity
mechanism anywhere in the codebase. `GET /api/user_account` returns a
real-shaped username, email, and full review history to any caller.
**History:** this endpoint was removed entirely during an earlier
security-hardening pass on this repository, on the reasoning that
unauthenticated PII exposure should be closed by deleting the feature.
After reviewing the actual assignment text, that call was reversed: this
endpoint and its UI are the assignment's second graded requirement (see
"Assignment Intent" above) — display username, email, and all reviews for
a user when the account link is clicked — and the assignment itself never
specified or implied a login system. Deleting the feature removed evidence
of completed, graded coursework to fix a risk that doesn't really apply
here: this is a local demo with one hardcoded synthetic account, not a
live service handling real users.
**Status: restored, accepted limitation by design, not fixed further.**
The route, the "View User Account" button, and `showUserAccountDetails()`
are back in `src/app.py` / `src/templates/index.html` / `src/static/script.js`
respectively, unchanged in shape from the original assignment scope.
Severity is downgraded from the original HIGH rating specifically because
of that context (single hardcoded demo account, synthetic seed data, no
network exposure implied by the assignment) — if this code is ever
repurposed into something with real users or deployed somewhere reachable
by untrusted clients, add real authentication before that happens.

**MEDIUM — Raw exception text leaked to clients.** Every route in
`src/app.py` returned `jsonify({'error': str(e)})` on failure, which surfaced
raw SQLite error strings (schema/constraint/table details) directly to
the client.
**Fixed.** All remaining routes now log the real exception server-side
via `app.logger.error(...)` and return a generic
`{'error': 'An error occurred processing your request.'}` message with a
500 status code instead of the raw exception text.

**MEDIUM — Fully public, unauthenticated write endpoint.**
`POST /api/add_book` has no authentication, no CSRF token, and no
origin/referrer check — it is a completely open write endpoint, and was
also the actual delivery mechanism for the stored XSS finding above.
**Status: accepted limitation, not fixed.** Adding real authentication is
out of scope for this coursework demo. The stored-XSS consequence of this
endpoint being open has been mitigated (see above), but the endpoint
itself remains unauthenticated. Anyone deploying this beyond local,
single-user use should add authentication and CSRF protection first.

**LOW — Book enumeration.** `GET /api/book/<book_id>` has no
authorization check, so sequential integer IDs can be walked to
enumerate every book in the database.
**Status: accepted limitation, not fixed.** Low severity given the data
isn't sensitive; revisit alongside real authentication if book data is
ever meant to be access-controlled. Out of scope for this pass.

**INFORMATIONAL:**
- `data/books.db` ships with realistic-looking seed PII: a `Users` row
  (`john_doe` / `john_doe@example.com`) and five associated review rows,
  now viewable again via the restored `/api/user_account` endpoint (see
  Security Findings above). It's synthetic fixture data, not a real
  person, but worth keeping in mind before reusing this seed data pattern
  in anything beyond a class assignment. `data/books.db` and `data/script.sql`
  are kept in the repo — they are the actual seed data and schema the app
  needs to have anything to display.
- `sqlite3.exe`, `sqldiff.exe`, and `sqlite3_analyzer.exe` were
  compiled Windows binaries committed directly under this directory (then
  named `db/`). Their
  provenance (official SQLite.org build vs. something else) was not
  verifiable from the repo alone.
  **Fixed.** Confirmed via a codebase-wide search (no `subprocess`,
  `os.system`, or other shell-out calls referencing these paths anywhere
  in `src/app.py` or elsewhere in the project) that nothing in the app
  invokes these binaries, so all three were deleted. See "Environment
  Setup" above for how to get a `sqlite3` CLI if you need to rebuild
  `data/books.db` from `data/script.sql`.
- No security headers (e.g. `Content-Security-Policy`,
  `X-Content-Type-Options`), no CORS configuration, and no session
  hardening (cookie flags, etc.) are configured anywhere in `src/app.py`.
  **Status: accepted limitation, not fixed.** Not independently
  exploitable today given the app has no sessions or cross-origin needs;
  address together with real authentication if this app ever grows
  beyond a local demo.

### Confirmed Not Present

A prior security audit checked for and did **not** find:
- SQL injection — all queries are correctly parameterized, including the
  year-search feature (`get_books_by_year`, `src/app.py`).
- CORS misconfiguration — no CORS is configured at all (see
  Informational note above).
- Jinja2 template XSS — `src/templates/index.html` does not interpolate
  unescaped user data through Jinja2; the stored-XSS risk that was found
  was entirely in the client-side `innerHTML` usage in
  `src/static/script.js` (now fixed, see above).

## Status

Coursework project, remediated for a personal-GitHub push, and confirmed
against the actual assignment text (see "Assignment Intent" above). Both
graded requirements are present and working: browse/add/search books by
year, and view the single demo user's account and reviews. Still not
hardened for any use beyond local, single-user demonstration — the
remaining accepted limitations (no auth on `POST /api/add_book` or
`GET /api/user_account`, no authorization on `GET /api/book/<book_id>`, no
security headers/CORS hardening) are documented above and are out of scope
for this coursework project. If this code is ever deployed somewhere
reachable by untrusted users, add real authentication first.
