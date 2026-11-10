---
name: Track PR
description: Create or refresh the approved colour-coded PR review tracker from a GitHub pull-request link. Keep one Excel workbook in the current OpenCode working folder, with one tab per PR named BRANCH_NAME-#PR_ID. Track reviews, comments, approvals, author turnaround and waiting time using authenticated gh.
---

# Track PR

## Invoke

Use this skill when the user invokes `@track-pr` with a GitHub PR link, or asks to
create, refresh, or update their PR tracker. A link is required. Never assume the
PR used while developing the skill is the requested PR.

Read the approved tracker rules below before running the script. Script and
template paths are relative to the folder containing `track-pr.md`, not the user's
working folder. The skill needs only this file, `scripts/`, and `templates/`.

## Workflow

1. Determine the **current OpenCode session working directory**. Do not substitute
   the skill's directory, the repository named in the link, `~/Documents`, or a
   previous session's output folder.
2. Verify `python3` and `gh` are available. Use the existing authenticated `gh`
   account; do not request tokens or change authentication. All GitHub access is
   read-only. A private PR requires account access.
3. Read the current folder's workbook if it exists. The script defaults to
   `PR-Review-Tracker.xlsx`. If there is exactly one differently named compatible
   tracker in that folder, reuse it. If there are multiple candidates, ask which
   to use and pass `--workbook`; do not create another workbook to avoid deciding.
4. If the workbook is open, ask the user to save and close it. Do not remove lock
   files or overwrite unsaved edits. The script checks application locks and
   checks for concurrent file changes before saving.
5. Run the bundled script, quoting paths containing spaces and passing the
   absolute current working directory explicitly:

   ```bash
   python3 "<skill-directory>/scripts/track_pr.py" \
     "https://github.com/OWNER/REPO/pull/NUMBER" \
     --directory "/absolute/current/session/working/directory"
   ```

   The first run uses the sanitized bundled template to create the workbook.
   Later runs update the existing PR tab in place, or add a new tab for a new PR.
   A tab is identified by its full PR URL, not just its number or branch name.
   Never overwrite another PR whose requested tab name happens to collide.
6. Full reviewer and author names must be Title Case. Use public display names
   or the bundled previously confirmed names. If the script asks for missing
   names, verify them from public profile/commit data or ask the user. Do not
   invent names by splitting usernames. Then rerun with, for example:

   ```bash
   --name "login=Full Name"
   ```

7. Tabs must be `SOURCE_BRANCH-#PR_ID`. Excel forbids `[]:*?/\` and limits names
   to 31 characters. If the exact name is invalid or collides, ask the user for
   an Excel-safe alternative and pass `--tab-name`. Never silently truncate or
   rename a different PR's tab.
8. Inspect the script result and validate the workbook can be read as an XLSX.
   For layout changes, render a preview in a temporary folder if LibreOffice is
   installed. Do not generate a PDF or other report in the output folder unless
   the user asks.
9. Respond briefly with the **same workbook path** and the updated tab name.
   Explain estimates or blockers only when relevant. No API dumps or long
   methodology in the response or sheet.

## Boundaries

- One report workbook per working folder; one tab per PR.
- No timestamped copies, exports, CSV bundles, scripts, or source-data folders in
  the working folder. Helpers and template stay in the skill; API snapshots stay
  under the local user cache, never in the output folder.
- Preserve unrelated tabs, notes, styles, and workbook parts. Never rebuild the
  whole workbook to refresh one PR. If an existing sheet has incompatible edits
  or formulas that prevent safe row insertion, stop and ask.
- Do not delete existing trackers, old helper scripts, or other user files.
- Never post GitHub comments, request reviews, edit PRs, push, or merge.
- Never claim timing-only matches prove which commit fixed an issue, or that
  elapsed time is active work effort. Use the approved concise `Estimated` label
  for fallback matches. Do not reintroduce explanatory warning rows.

## Approved tracker rules

### Output and identity

Create/update `PR-Review-Tracker.xlsx` in the **current session working folder**.
Reuse an existing compatible tracker rather than create duplicates. Every PR has
one tab named `SOURCE_BRANCH-#PR_ID`. Find an existing tab by its full PR URL,
including owner and repository. Keep all unrelated tabs unchanged.

### Appearance

- Use the bundled approved template. Four sections on the same tab: Summary,
  Copilot Reviews, Human Reviews, Waiting for Review.
- Navy title; blue section bars; dark slate labels with white bold text and pale
  value cells. Keep the visible spacer after the PR title row.
- Green resolved comments; amber waiting/push associations; blue author timings.
- Full human names in Title Case, not usernames. First-person labels (`My`).
- Bold headings inside a value cell. Bold **Unavailable**, alone, for a required
  value that cannot be observed or calculated. No explanation after it.
- Approval-only reviews: push and response duration say `Not needed`.
- Plain comment counts such as `10`, never `8 roots + 2 replies`. Counts include
  that reviewer's published inline comments and follow-up replies, excluding the
  PR author's replies. Do not count review-summary bodies again as comments.
- Resolution follows each comment's current discussion state. No GitHub jargon
  such as roots, threads, node IDs, commit SHAs, or feedback submission counts.
- Use `TIME WAITING FOR REVIEW`, not a technical heading with the format appended.
- No disclaimer rows, colour legend, requested-but-never-reviewed user list,
  API data tables, or timezone banner. Do not add missing resolution-date fields.

### Time rules

- Convert every timestamp to **IST, UTC+05:30**, but do not print IST/UTC in cells
  or a banner. Format: `Fri, 06 Nov 2026, 02:24 PM`.
- Calendar ages/durations: `15d 08h 35m` (days, hours, minutes, zero-padded).
- Effective working hours: Mon–Fri, 10:00–19:00 IST. A full 9-hour window counts
  as 8 effective hours. Partial windows are multiplied by 8/9. Weekends excluded;
  no public-holiday assumptions. Do not invent a fixed lunch hour.
- PR age ends at merge/close, or at the current snapshot when open. Working-age
  hours are numeric, two decimal places. Response/wait intervals remain calendar
  durations; they are not active development or review effort.
- Feedback timing uses submitted/published reviews, not private draft-comment
  creation times. A comment may have been created before its review was visible.
- Prefer the **last recorded author force-push before the latest author reply**
  in that comment's discussion, after the review submission. Show only that
  associated push, not an unrelated earlier push as well.
- If a comment has no usable reply-based push match, use the **first author
  force-push after its review submission**, with the concise `Estimated` label
  beside both the date and calculated duration. Never mistake a Git author or
  committer timestamp for an actual GitHub push event.
- Deduplicate push dates for the same reviewer. If there are multiple associated
  pushes, list them and calculate reviewer response duration from first feedback
  to the latest associated push. Mark the aggregate as estimated when any match
  is estimated. Never add overlapping reviewer intervals into total work effort.
- If no subsequent push exists, a required push/time is bold `Unavailable`.
- Current resolved status is observable. Exact resolution timestamps are not
  exposed by the queried thread API and must not be guessed from reply/push time.
  Omit those optional datetime subfields rather than adding explanatory filler.
- Waiting: latest active review request to that person's next submitted review,
  or snapshot/closure if unanswered. Removed/cancelled requests are not pending.
- Keep approvals separate from author replies and bot reviews. Record actual
  approval events, not an inferred approval because all comments were resolved.

### Fetching and safety

Fetch fresh PR metadata, paginated reviews, inline comments, issue timeline,
review requests/force-push events, and GraphQL review discussions with complete
pagination. Separate Copilot and human reviews. Exclude pending unpublished
reviews. Exclude author reply review records from reviewer counts. No invented
sample values in the finished report.

On authentication/network/API errors, incomplete data, name/tab collisions,
unsupported workbook structures, or concurrent changes, preserve the old
workbook and report the blocker. Do not silently delete, rebuild, or partially
overwrite it. Raw snapshots and audits live in the local cache, not alongside
the report. Never publish private PR information.

## Maintenance

- Engine: `scripts/track_pr.py` (Python standard library only).
- Approved sanitized layout: `templates/tracker.xlsx`.
- Confirmed names: `KNOWN_NAMES` in `scripts/track_pr.py`; `--name` can override them.
- All formatting, timing, and safety rules are included above.
- No separate rule, name-map, or test folders are needed to run this skill.

The engine is bundled and must remain installed. The old loose script in a
Documents folder is not used or required by this skill.
