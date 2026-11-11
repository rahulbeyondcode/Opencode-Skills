---
name: Zimbra Coder
description: Use when writing, changing, refactoring, reviewing, testing, or preparing PRs for Zimbra JavaScript, Node.js, React/Preact, Redux, or Modern UI GraphQL code. Apply all seven standards from this self-contained skill, with optional targeted references, self-review, TestCafe/Playwright automation instead of unit tests under the confirmed repository policy, and approval/QA gates.
---

# Zimbra Coder

Apply the complete Zimbra JavaScript, React/Preact, Redux, GraphQL, code-review process, general review checklist, and frontend review checklist below. Use review criteria as implementation requirements from the start, not merely as checks after a PR is opened. The aim is to prevent avoidable review comments through correct, maintainable, secure, tested, review-ready code; do not promise zero comments or bypass human review. Do not silently omit a rule because a task is small, a convention is inconvenient, or a newer framework offers a different default.

## Confirmed repository testing policy — overrides legacy test requirements

The user has confirmed, after consulting leadership, that **this repository no longer writes unit tests and relies only on TestCafe and Playwright automation**. This is the confirmed policy for the repository discussed in this skill's setup, not a claim about every Zimbra repository. Do not generalize this exception to an unrelated repository without establishing its policy.

- **Apply this explicit override before the historical source documents.** Their unit-test/JUnit requirements are preserved for traceability, but are superseded for this repository. Do not repeatedly ask for confirmation of the already resolved JUnit applicability question.
- **Do not write or require unit tests or JUnit tests, introduce a unit-test framework, or reject/block a change solely because unit tests are absent.** Do not delete existing tests or alter existing test infrastructure merely because of this policy; those actions need their own task scope.
- **Use TestCafe and Playwright automation for regression and behavior verification.** Add or update relevant automation for changed behavior where the task permits, following the existing suites and platform split: TestCafe for Web/Mobile and Playwright for Desktop. Inspect actual repository scripts and setup; do not invent commands or require both tools for an unaffected platform.
- **Keep meaningful coverage and honest evidence.** Check intended behavior, affected flows, regressions, errors, and boundary cases through the applicable automation. Do not impose an obsolete unit-test/code-coverage percentage. Use any currently agreed automation coverage criteria. Report automation added or updated, runs actually performed, results, and missing coverage or environment blockers.
- **Keep other quality gates.** Linting, formatting, self-review, two-reviewer approval, QA approval, and testing/pre-UAT gates still apply. Manual diagnostic checks may supplement automation and must be reported honestly if performed; they are not a substitute for the confirmed automation strategy or a new mandatory unit/manual-test suite.

## Mandatory workflow

1. **Use this self-contained skill by default.** The rules, exceptions, and confirmed overrides needed for normal coding and review are included below. Do not open files in `references/` merely because this skill was invoked or a topic is relevant. Only when a specific ambiguity, missing example detail, or conflict needs clarification, follow the relevant link in the optional-reference table and read the section needed to resolve it. Usually one file is enough; read a second only if the question spans sources, and expand further only for a concrete unresolved need. Leave all other references unread. Supporting files are not loaded automatically. If a needed section is truncated, continue that section; do not bulk-load the folder. If a source necessary to resolve the question is unavailable, disclose that specific gap rather than guessing. Unread optional references are not a compliance gap.
2. **Establish the task context.** Inspect applicable repository instructions, surrounding code, `package.json`, dependency versions, lint/format configuration, and relevant tests. These standards apply to frontend JavaScript and backend Node.js; React guidance also applies to Zimbra's Preact code.
3. **Track every rule.** Keep a task-local compliance ledger for every ID below: `PASS`, `N/A` with a reason, or `BLOCKED` with the missing evidence or conflict. Alternatives under Redux are alternatives, not a demand to use all three approaches. A preference must be considered and followed where applicable, not misrepresented as an unconditional ban.
4. **Apply the standards while working.** Before implementation, identify likely review concerns, acceptance criteria, affected areas, tests, security boundaries, documentation, and dependency approvals. During implementation, use every applicable review criterion to guide design and code, including affected callers, component rendering, Redux updates, and backend-to-GraphQL data flow. Before handoff, self-review the final diff as a reviewer would and address in-scope findings. In review-only work, report findings without modifying files. Do not expand a task into unrelated cleanup.
5. **Resolve uncertainty explicitly.** Preserve the intent of the source prose rather than reproducing malformed examples. Do not invent content for missing references, guess backend types, or silently replace these standards with personal preferences. If a genuine conflict with project requirements, runtime compatibility, or higher-priority instructions prevents compliance, explain it and seek clarification when needed.
6. **Verify before completion.** Re-check every ID against the final diff or reviewed code, not just the initial plan. Run applicable existing lint, formatting, and TestCafe/Playwright automation scripts from `package.json`; inspect what scripts run rather than invoking a generic test command that introduces a legacy unit-test requirement. Check runtime warnings and affected-area behavior through applicable automation, with optional manual diagnostics when useful. Report actual results, unrun checks, and every blocked rule or necessary deviation. Do not claim full compliance while any applicable rule is unchecked or blocked. Distinguish coding completion, review readiness, permission to start QA, and permission to merge; a local self-review cannot supply reviewer or QA approvals.

After context compaction or loss of these instructions, reload `SKILL.md`, not the reference folder. Reopen only a previously consulted source section whose detail is still needed and no longer available in context. Do not reread all sources as a routine recovery step. The ledger is a working verification aid; the final response may be concise, but it must disclose gaps honestly.

## Optional references — read only for clarification

These links are an on-demand lookup index, not a reading checklist. Normally only `SKILL.md` is loaded. The files preserve verbatim Confluence exports, including source URLs, page IDs, examples, and export limitations; keep them intact. Paths are relative to this skill's directory. Open only the file and section needed for a specific clarification, not all files for the current task. Source line ranges below are lookup aids, not instructions to load those ranges routinely. Historical unit-test/JUnit wording does not override the confirmed repository testing policy above.

**Clarification trigger:** Before opening a reference, identify the affected rule ID and the exact question this skill does not answer. Consult the source only if a rule has materially different plausible interpretations, a necessary exception/example detail is missing here, or an apparent conflict between rules or repository requirements could change the implementation or review verdict. If this skill already resolves the question, do not open a reference. Task size, topic relevance, routine self-review, or a desire to reread everything “just in case” are not triggers. Stop reading once the question is resolved. This restriction concerns the archived standards, not inspection of project code, installed APIs, test results, or authoritative backend definitions required as task evidence.

| Optional source | Original page ID | Rules | Consult only to clarify |
| --- | --- | --- | --- |
| [JavaScript Coding Standards](references/javascript-coding-standards-3502964753.md) | 3502964753 | JS-01 through JS-17 | JavaScript style, tooling, or examples |
| [React Coding Standards](references/react-coding-standards-3502964766.md) | 3502964766 | REACT-01 through REACT-13 | Component, hook, form, or rendering guidance |
| [Redux Coding Standards](references/redux-coding-standards-3503030279.md) | 3503030279 | REDUX-01 through REDUX-04 | Selector alternatives or dispatch batching |
| [GraphQL schema types in Modern UI](references/graphql-schema-types-in-modern-ui-4210557083.md) | 4210557083 | GQL-01 through GQL-04 | Backend scalar mappings or the schema example |
| [Code Review Process](references/code-review-process-3309469738.md) | 3309469738 | PROCESS-01 through PROCESS-15 | Review responsibilities, approvals, or QA sequence |
| [Code Review Checklist](references/code-review-checklist-2724626481.md) | 2724626481 | REVIEW-01 through REVIEW-36 | General, security, documentation, or review-template details |
| [Frontend Code Review - Checklist](references/frontend-code-review-checklist-3305570360.md) | 3305570360 | FE-01 through FE-23 | Frontend examples, cleanup, or optimistic cache updates |

The JavaScript, React, and Redux documents explicitly describe themselves as incomplete, evolving guides based on recurring PR feedback. Follow every supplied instruction, but do not mistake these documents for an exhaustive specification of all valid JavaScript, security, correctness, or project requirements.

## JavaScript standards

Source: `references/javascript-coding-standards-3502964753.md`.

- **JS-01 — Supported environment (lines 23–31).** Respect the documented baseline: ECMAScript 2015; Chrome, Firefox, Safari, and MS Edge; Node v18. Check the project's actual build/transpilation and runtime setup before introducing syntax or APIs. Do not upgrade these baselines merely because newer versions exist; disclose genuine conflicts with the repository.
- **JS-02 — Tooling (lines 34–47).** The documented stack is Visual Studio Code, ESLint, Prettier, TestCafe for Web and Mobile, Playwright for Desktop, and NPM. The confirmed repository policy uses TestCafe/Playwright automation only, not new unit tests. Consult `package.json` for the actual scripts; most tooling is already automated. Use the applicable existing tools rather than inventing commands or replacing the toolchain. The IDE listing is context, not a requirement to operate an editor through tools.
- **JS-03 — Intention-revealing names (lines 53–116).** Use meaningful variable and function names, not unexplained abbreviations or vague names such as `d`, `cust`, `getData`, or `setData`. Name meaningful conditions, such as `isAuthenticated` and `shouldGetNewForecast`. A function name must reveal important behavior and side effects: for example, `handleErrorAndRedirectTo` rather than `handleError` when it also redirects. Use domain-specific names such as `elapsedTimeInDays`, `customer`, `getSingleProductData`, and `setProductName`.
- **JS-04 — Meaningful constants (lines 118–155).** Prefer meaningful constants over inline strings or numbers. Examples include reusable error messages shared with test assertions, password-length thresholds, and color values. Keep the behavior and comparisons correct; the examples demonstrate naming, not new product requirements.
- **JS-05 — Group related constants (lines 157–170).** Prefer objects for related constants, such as `MAIL_ACTIONS.REPLY` and `MAIL_ACTIONS.FORWARD`, rather than isolated action constants.
- **JS-06 — Boolean names (lines 172–185).** Prefix boolean variables with `is`, `has`, or `should`, for example `isActive` or `hasError`.
- **JS-07 — Object destructuring (lines 187–211).** Use object destructuring when accessing multiple properties of the same object. Prefer destructuring directly in the function parameters when appropriate; local destructuring is also shown as good.
- **JS-08 — Strings (lines 213–226).** Prefer template strings over string concatenation for interpolated strings.
- **JS-09 — Function arguments (lines 228–249).** Prefer functions with no more than four arguments. Group additional related arguments into an options object instead of extending a long positional argument list.
- **JS-10 — Default parameters (lines 251–267).** Use default parameter syntax rather than mutating an argument to assign a default. Preserve intended semantics: a default parameter applies to `undefined`, not to every falsy value. The type annotations in the source example are illustrative, not permission to add unsupported syntax to `.js` files.
- **JS-11 — Composition and higher-order functions (lines 269–308).** Avoid anonymous functions for composed functions. Return a named function expression or a meaningfully named function variable, as in `functionLogger`.
- **JS-12 — Unnecessary else branches (lines 310–343).** Avoid unnecessary `else` statements, especially after a branch has already returned.
- **JS-13 — Early returns (lines 310–343).** Return as early as possible. Prefer guard clauses over deeply nested success/error branches and temporary values used only to defer a return.
- **JS-14 — Functional iteration (lines 345–383).** Prefer array prototype iteration methods over `for-in` and `for-of`, and use appropriate functional methods instead of manual accumulation loops. The examples favor `reduce` for a sum and `filter` for selecting values; `forEach` is also shown as better than a manual loop for accumulation.
- **JS-15 — Large-array iteration (lines 345–383).** Avoid long iteration-method chains on large arrays. Do not apply the functional-iteration preference by creating excessive repeated passes or intermediate arrays.
- **JS-16 — Focused imports (lines 385–402).** Prefer destructured/named imports for named exports rather than importing an entire module to access one member. Preserve the example's ordering for Lodash: whole `_` import is good, `import { get } from 'lodash'` is better, and the supported direct-member import `import get from 'lodash/get'` is best. Verify the dependency's available entrypoints; do not invent a subpath.
- **JS-17 — Named exports (lines 404–414).** Prefer named exports over default exports for code you author. This preference does not forbid importing an existing dependency's default export, including the direct Lodash import above.

## React and Preact standards

Source: `references/react-coding-standards-3502964766.md`. Zimbra uses Preact; these React guidelines still apply (lines 14–22).

- **REACT-01 — Component extension (lines 24–31).** Use `.js` for React/Preact component files.
- **REACT-02 — Filenames (lines 24–31).** Use kebab-case `.js` filenames, such as `html-body.js` and `text-body.js`.
- **REACT-03 — Function components (lines 33–39).** Prefer function components when creating new components. Class components are no longer preferred, except for components requiring `componentDidCatch`. Preserve that exception; do not force an error boundary into an unsuitable function-component implementation.
- **REACT-04 — Component names (lines 42–53).** Use meaningful component names, such as `UserInformation` rather than the vague `User`.
- **REACT-05 — State and function names (lines 55–64).** Use meaningful state-variable, setter, and function names, such as `[messages, setMessages]` rather than `[data, setData]`.
- **REACT-06 — Prop names (lines 66–75).** Use meaningful component prop names, such as `<ProductList products={products} />` rather than a generic `data` prop.
- **REACT-07 — Hook dependencies (lines 77–92).** Always specify all necessary dependencies for `useEffect`, `useCallback`, and `useMemo`. Determine the actual reactive values captured from the component scope; do not use an empty array to conceal a dependency. The source's `handleClick` example is syntactically malformed and lists `value` ambiguously. Apply the stated dependency rule using valid hooks: a value passed only as a callback parameter is not itself a captured dependency, whereas a referenced `onClick` prop is. Do not copy the malformed snippet or blindly add out-of-scope identifiers.
- **REACT-08 — Generic components stay generic (lines 94–100).** Components such as `FolderList`, `FolderListItem`, and `Viewer` must not care about domain-specific details of what they render.
- **REACT-09 — No child special-casing (lines 94–100).** Avoid passing special-purpose props to a child or adding conditions to special-case a child inside generic components. Keep domain-specific behavior outside the generic component instead of polluting its contract.
- **REACT-10 — Form state and refs (lines 103–119).** Avoid `useState` for form elements when state does not need to update on every interaction. Prefer an uncontrolled input with `useRef` and read `inputRef.current.value` when needed to avoid re-rendering on each keypress. This is conditional guidance: retain controlled state when per-interaction state updates are genuinely required.
- **REACT-11 — Avoid wasted renders (lines 121–123).** Write performant components and examine unnecessary renders. The source specifically asks the reader to read the document on “tackling wasted renders”, but its URL is unavailable in the export and the document is not bundled. Look for an accessible project reference when relevant; if unavailable, disclose that the linked guidance remains unverified. Do not claim to have read it or invent its contents. Apply all available render-related rules regardless.
- **REACT-12 — Minimal DOM (lines 126–143).** Do not introduce unnecessary DOM nodes. Use `Fragment` to group siblings when a wrapper element has no necessary purpose.
- **REACT-13 — Simple render branches (lines 145–199).** Do not nest conditional renders. Return early for loading and error states, or extract subcomponents for complex components. Prefer separate view/loading/error components when this makes a complex component clearer, as in `ForecastView`, `ForecastLoading`, and `ForecastError`.

## Redux standards

Source: `references/redux-coding-standards-3503030279.md`.

Returning a newly allocated object **or array** from `useSelector` on each call forces re-renders under default reference equality. For multiple store values, choose an appropriate option from REDUX-01, REDUX-02, or REDUX-03. Mark the unused alternatives `N/A — another documented selector strategy is used`; do not require all three together.

- **REDUX-01 — Separate selectors (lines 21–44).** Call `useSelector` separately for each field, for example separate selectors for `userInfo`, `products`, and `shoppingCart`, rather than an unprotected fresh aggregate array/object.
- **REDUX-02 — Memoized aggregate selectors (lines 23–29).** Alternatively, use Reselect or a similar memoization library for a multi-value selector. Return a new aggregate object only when one of its selected values changes; merely constructing a fresh object inside the selector does not satisfy this rule.
- **REDUX-03 — Shallow equality (lines 23–29).** Alternatively, pass React-Redux's `shallowEqual` as the `equalityFn` argument to `useSelector` when returning multiple values in an aggregate.
- **REDUX-04 — Batch dispatches (lines 48–63).** Use `batch` to wrap multiple dispatches that belong together, preventing unnecessary re-renders. Do not silently drop this explicit Zimbra rule based on assumptions about automatic batching in a newer framework version. If the project's runtime or API creates a genuine conflict, disclose and resolve it rather than guessing.

The source directs readers to the [React-Redux hooks documentation](https://react-redux.js.org/api/hooks) for details (line 46). Consult it when selector API or equality behavior needs clarification, using the project's installed version. It supplements, rather than silently replaces, the supplied Zimbra rules.

## GraphQL schema type standards

Source: `references/graphql-schema-types-in-modern-ui-4210557083.md`.

- **GQL-01 — Backend alignment (lines 14–22).** Every newly added GraphQL field, whether added for a bug fix or a feature, must have a type aligned with the backend schema. Apply the same alignment check when correcting an existing field. Misalignment can cause unpredictable behavior; do not infer the type from the field name, a UI string, or a single observed payload.
- **GQL-02 — Authoritative attribute definitions (lines 20–22).** For String/Int/Float field decisions involving LDAP attributes, inspect the attribute's actual definition and type in [Zimbra's LDAP attributes list](https://github.com/Zimbra/zm-mailbox/blob/develop/store/conf/attrs/zimbra-attrs.xml#L2239), at `store/conf/attrs/zimbra-attrs.xml`. Locate the named attribute, not just the historic line anchor; use the backend version relevant to the task. Record the definition used as evidence. If it is unavailable, report a blocker instead of guessing or declaring the schema verified.
- **GQL-03 — Scalar mappings (lines 20–22).** Preserve these exact LDAP-to-GraphQL mappings:

  | LDAP attribute type | GraphQL schema scalar |
  | --- | --- |
  | String | `String` |
  | Integer | `Int` |
  | Long | `Float` |

  GraphQL does not have a built-in `Long` scalar; this guide requires `Float` for an LDAP Long. “Integer” in the prose means the GraphQL `Int` scalar, not a new scalar named `Integer`. Do not substitute `String` or invent a custom scalar for these mappings without an explicitly resolved requirement. For other backend types, inspect authoritative definitions and project conventions rather than inventing a mapping. The source links [GraphQL basic types](https://graphql.org/graphql-js/basic-types/) as supporting documentation.
- **GQL-04 — Preserve the concrete regression example (line 16).** `zimbraDataSourceMaxNumEntries` was incorrectly added as `String`; its integer backend type requires GraphQL `Int`. Treat this as a specific warning against numeric attributes accidentally being exposed as strings, not a reason to change unrelated schema fields without checking their definitions.

The linked screenshot is preserved in the source reference but was not downloaded or interpreted in the export (lines 9–10 and 18). Do not claim it was inspected. The scalar rules above are supported by the supplied text independently of that image.

## Code-review process, applied proactively

Source: `references/code-review-process-3309469738.md`.

- **PROCESS-01 — Initiation (lines 16–20).** When a completed set of changes is ready for integration, initiate the review stage so it is checked against project requirements and coding standards. Prepare for this stage while coding rather than waiting for reviewers to find basic issues.
- **PROCESS-02 — Reviewer selection (lines 23–27).** The team lead, tech lead, or development team selects reviewers based on expertise and availability. Reviewers must know the codebase and relevant aspects of the changes. Suggest appropriate expertise when useful, but do not assign people without authorization or fabricate approvals.
- **PROCESS-03 — Required checklist (lines 30–32).** Apply the general code-review checklist rules below when reviewing a PR and during author self-review; also apply the frontend rules where relevant. Their requirements remain mandatory, but reading the original documents is optional. The process export's checklist link is unresolved; the bundled general checklist is linked in the optional-reference table if a specific detail needs clarification. Do not skip checklist rules or routinely load the original document because of that missing link.
- **PROCESS-04 — Author preparation (lines 35–39).** Before review, ensure coding-standard compliance, necessary documentation, and attention to pre-existing issues. Proactively address potential concerns. Inspect pre-existing issues relevant to the change, fix those within authorized scope, and flag out-of-scope issues instead of silently ignoring them or performing unrelated rewrites.
- **PROCESS-05 — Examine changes (lines 42–46).** Review correctness, completeness, and adherence to standards. Apply that same examination to your own implementation before handoff.
- **PROCESS-06 — Constructive feedback (line 48).** Give constructive, actionable feedback: identify issues, suggest improvements, and ask useful questions. Support findings with evidence rather than manufacturing comments.
- **PROCESS-07 — Automation review (line 50; confirmed policy override).** The source's unit-test requirement is superseded for this repository. Plan, add or update, and review appropriate TestCafe/Playwright automation during implementation rather than waiting for reviewer feedback. Verify applicable automation evidence; do not require unit tests.
- **PROCESS-08 — Respond to reviewers (lines 52–54).** Respond to comments, clarify intentions, and make necessary adjustments. Do not dismiss or silently leave relevant comments unresolved.
- **PROCESS-09 — Design rationale (line 56).** Explain the rationale behind design decisions when needed. Capture non-obvious reasons while implementing so reviewers do not need to infer them.
- **PROCESS-10 — Iterate (lines 59–63).** If issues are found, repeat review and adjustment until concerns are addressed and the code meets project goals. An additional iteration is optional only when there are no concerns requiring it; re-run relevant verification after fixes.
- **PROCESS-11 — Reviewer, QA, and merge gates (lines 66–70).** Require **at least two reviewer approvals before proceeding to testing/QA**. Require QA approval after its testing and passage of the testing/pre-UAT stage before merging to `main`/`develop`. Normal author tests and self-review still occur before reviewer approval. Do not equate local tests, a self-review verdict, or a single approval with authorization to merge. Record pending workflow gates when reporting readiness; do not claim approvals without evidence.
- **PROCESS-12 — Post-review documentation (lines 73–75).** Update relevant documentation, including code comments, to reflect the final changes and review-driven adjustments.
- **PROCESS-13 — Knowledge sharing (line 77).** Share useful insights gained during review with the wider team through an appropriate handoff or authorized team channel. This is not authorization to publish private material or send messages on the user's behalf.
- **PROCESS-14 — Continuous improvement (line 79).** Use review feedback to improve personal coding practice and team processes. Apply relevant lessons to the current work rather than repeating known review mistakes.
- **PROCESS-15 — Principles and benefits (lines 82–108).** Detect issues early; collaborate and share knowledge; maintain consistent standards and a maintainable codebase; communicate positively and respectfully; treat reviews as continuous learning and mentorship opportunities, especially for less experienced developers. Prioritize quality, reliability, and mitigation of bugs, regressions, and vulnerabilities. These goals guide coding and review; they do not replace the concrete checks or approval gates.

## General code-review checklist

Source: `references/code-review-checklist-2724626481.md`. Apply these checks while writing code and again during self-review.

### Review/PR template

When preparing a review request or PR description, include all four fields below. Do not force this template onto unrelated coding updates or replace a separately required review-report format; include the information in the appropriate artifact.

- **REVIEW-01 — Problem (line 16).** Explain the problem being fixed.
- **REVIEW-02 — Approach And Fix (line 18).** Explain the chosen approach and the actual fix applied.
- **REVIEW-03 — Testing done (line 20; confirmed policy override).** State TestCafe/Playwright automation added or updated, runs actually performed, outcomes, and affected areas actually tested. Include manual diagnostic checks only if actually performed. Distinguish automation added from automation executed; do not invent results or require an added-unit-tests section.
- **REVIEW-04 — Testing to be done by QA (line 22; confirmed policy override).** List affected areas, remaining TestCafe/Playwright automation and QA verification scope, required automation updates, and environment blockers. Do not reinstate unit tests or a mandatory manual-test suite; describe any additional QA checks actually requested.

### General checks

- **REVIEW-05 — Correct behavior (line 27).** Verify that the code works, performs its intended function, and has correct logic.
- **REVIEW-06 — Understandability (line 29).** Ensure all changed code is easy to understand.
- **REVIEW-07 — Agreed conventions (line 31).** Follow agreed brace placement, variable/function naming, line length, indentation, formatting, and comment conventions, together with the coding standards above.
- **REVIEW-08 — Duplication (line 33).** Remove redundant and duplicate code within the scope of the change.
- **REVIEW-09 — Modularity (line 35).** Keep code as modular as practical with clear responsibilities.
- **REVIEW-10 — Global variables (line 37).** Check whether globals can be replaced with appropriately scoped state or dependencies; do not introduce avoidable global variables.
- **REVIEW-11 — Commented-out code (line 39).** Remove commented-out implementation code rather than leaving dead alternatives in the change.
- **REVIEW-12 — Loop bounds (line 41).** Verify loops have defined bounds/set length and correct termination conditions; prevent infinite loops and off-by-one errors.
- **REVIEW-13 — Existing library functions (line 43).** Check whether established library functions can replace custom code. Do not add a new dependency without checking approval and bundle-impact requirements.
- **REVIEW-14 — Logging (line 45).** Ensure logging is sufficient but not excessive and uses the correct level; follow the production-console restriction in FE-10.
- **REVIEW-15 — Unused code (line 47).** Remove unused variables and imports.
- **REVIEW-16 — Enum suitability (line 49).** Consider whether related constants are better represented as an enum. This is an assessment, not permission to introduce unsupported enum syntax into ECMAScript 2015 `.js` files; use the project's supported representation, including the grouped constants object required by JS-05 where appropriate.
- **REVIEW-17 — API documentation (line 51).** Document API changes.
- **REVIEW-18 — Superseded JUnit gate (line 53; confirmed policy override).** The historical source requires JUnit and rejection when it is absent. The user has explicitly confirmed that leadership replaced unit testing with TestCafe/Playwright automation for this repository. Mark this legacy gate `N/A — superseded by confirmed automation-only repository policy`, not `BLOCKED`. Do not require JUnit, reject for missing unit tests, or seek the same confirmation again. Verify current automation requirements under PROCESS-07 and REVIEW-33/34 instead.
- **REVIEW-19 — Debugging artifacts (line 55).** Remove unnecessary debugging code before handoff.
- **REVIEW-20 — Open-source approval (line 57).** A newly introduced open-source library must follow the organization's approval process. The process link is unresolved in the export and its procedure is not bundled. Locate authoritative policy and approval evidence when adding a library; if unavailable, report the missing approval as a blocker. Do not invent a process, assume approval, or add the library first and seek permission later.

### Security checks

- **REVIEW-21 — Inputs (line 62).** Check all data inputs for correct type, length, format, and range, and apply context-appropriate encoding. Do not confuse encoding with validation.
- **REVIEW-22 — Third-party errors (line 64).** Catch and handle errors returned or thrown by third-party utilities, including rejected asynchronous calls.
- **REVIEW-23 — Outputs (line 66).** Check output values and encode them appropriately for their destination.
- **REVIEW-24 — Invalid parameters (line 68).** Handle invalid parameter values explicitly and safely.
- **REVIEW-25 — Private until release (line 70).** Keep unreleased PRs/code private until release. Verify the actual repository/PR visibility model before claiming compliance; a draft PR in a public repository is not private. Do not publish unreleased changes, change repository visibility, or create/move PRs without authorization. If privacy cannot be verified or the requested destination is public, flag the issue before publishing.

### Documentation checks

- **REVIEW-26 — Intent comments (line 75).** Ensure comments describe code intent.
- **REVIEW-27 — Function comments (line 77).** Check that all functions are commented as the general checklist requests. For frontend code, satisfy this with concise meaningful intent, contract, or rationale comments, not the redundant implementation narration prohibited by FE-02. If repository policy makes the requirements incompatible, disclose the conflict rather than silently skipping one.
- **REVIEW-28 — Unusual behavior (line 79).** Describe unusual behavior and edge-case handling.
- **REVIEW-29 — Third-party documentation (line 81).** Document the use and purpose of third-party libraries.
- **REVIEW-30 — Data semantics (line 83).** Explain data structures and units of measurement.
- **REVIEW-31 — Incomplete code (line 85).** Identify incomplete code; remove it or flag it clearly with a suitable marker such as `TODO` where appropriate. A marker does not make missing required behavior complete.

### Testing checks

- **REVIEW-32 — Automation testability (line 90; confirmed policy override).** Keep dependencies manageable and visible and changed behavior exercisable through the existing TestCafe/Playwright suites. Preserve clear, testable design without adding unit-test-only interfaces or requiring methods to be exposed solely to a unit-test framework.
- **REVIEW-33 — Comprehensive automation coverage (line 92; confirmed policy override).** Ensure applicable TestCafe/Playwright automation meaningfully covers changed and affected behavior and meets currently agreed automation coverage criteria. Do not invent a percentage, impose a legacy unit-test coverage threshold, or claim measured coverage without evidence.
- **REVIEW-34 — Behavioral automation (line 94; confirmed policy override).** Apply the source's behavioral-testing intent to TestCafe/Playwright: assert intended user-visible functionality and relevant regressions, errors, and boundary cases, not merely page loading, code execution, or incidental implementation details. Do not add or require unit tests.
- **REVIEW-35 — Array bounds (line 96).** Check array out-of-bounds behavior and relevant boundary cases.
- **REVIEW-36 — Existing test APIs (line 98).** Replace unnecessary custom test code with suitable existing APIs where possible.

## Frontend review checklist

Source: `references/frontend-code-review-checklist-3305570360.md`. The IDs match the source's 23 numbered checklist entries. The rules below include the relevant example details; consult the linked original only if a specific detail remains unclear.

- **FE-01 — Component size (lines 13–17).** Keep components small. When a component exceeds **200–300 lines**, consider extracting child components; this is a review trigger, not an absolute line-count ban. Separate distinct responsibilities, such as `UserInformation` and `UserActions` from `UserProfile`.
- **FE-02 — Why comments (lines 19–36).** Remove unnecessary comments explaining how obvious code works; add necessary comments explaining why decisions were made. Reconcile this with REVIEW-26/27 using meaningful intent/rationale comments. The source's localStorage-versus-cookies example demonstrates a comment's purpose, not a general security endorsement of localStorage for authentication.
- **FE-03 — Lint (lines 38–42).** Ensure there are no linter errors; run the applicable ESLint script and fix errors introduced by the changes. Report unrelated existing failures rather than claiming a clean run or making unauthorized broad cleanup.
- **FE-04 — Runtime warnings (lines 44–48).** Resolve React/Preact console warnings, including missing unique `key` props in rendered lists. Check the running affected UI when possible; otherwise report runtime warning verification as unperformed.
- **FE-05 — Reuse (lines 50–54).** Avoid repeated code by extracting reusable functions/components, for example shared form-submission handling. Do not pollute generic components with domain-specific exceptions while doing so.
- **FE-06 — Existing patterns (lines 56–60).** Follow established code patterns and conventions in the surrounding codebase. Surface genuine conflicts with explicit supplied standards instead of silently choosing one.
- **FE-07 — Unused props (lines 62–66).** Do not pass unused props; remove unused child-component props from changed code.
- **FE-08 — Consistent naming (lines 68–72).** Keep variable, filename, and translation naming consistent. Use camelCase for variables and PascalCase for component names as illustrated, alongside the required kebab-case `.js` filenames. Component identifier casing does not change the filename rule.
- **FE-09 — Constants (lines 74–78).** Avoid hardcoded values; use meaningful constants such as `MAX_LOGIN_ATTEMPTS`, and group related constants according to JS-05.
- **FE-10 — Production console logs (lines 80–84).** Avoid `console.log` in production code unless necessary for an explicitly justified debugging need. Remove temporary debugging logs before deployment; do not treat illustrative `console.log` examples elsewhere as permission to leave them behind. Preserve appropriately leveled, necessary error handling under REVIEW-14.
- **FE-11 — Promises, not async/await (lines 86–90).** Use Promises instead of `async`/`await` in frontend code and handle API rejections gracefully, for example with `.catch()`. This is an explicit checklist instruction even though the JavaScript forecast and frontend optimistic-response examples contain `async`/`await`. Follow the prose rule for new implementation; do not copy those example inconsistencies or rewrite unrelated existing code. Surface a genuine incompatible project requirement for resolution.
- **FE-12 — Destructuring (lines 92–102).** Use array and object destructuring where applicable, including object destructuring in function parameters.
- **FE-13 — Custom hooks (lines 104–114).** Encapsulate reusable component logic in custom hooks for organization and reuse, such as a shared data-fetching hook.
- **FE-14 — useCallback with useEffect (lines 116–129).** Use `useCallback` for functions invoked by `useEffect` when the function is an effect dependency. Include its actual dependencies in `useCallback` and the callback in the effect dependencies, as in the `fetchData` example; do not suppress dependencies or blindly copy the placeholder `dependency` identifier.
- **FE-15 — Shared helpers (lines 131–141).** Extract repeated functions into shared helpers, for example common date formatting, instead of duplicating implementations elsewhere.
- **FE-16 — Exceptions and cleanup (lines 143–157).** Handle exceptions and release resources to avoid memory leaks and unexpected behavior. Use appropriate `try`/`catch`/`finally` for synchronous work and proper rejection/cleanup handling for Promises; a synchronous `try`/`catch` alone does not catch a later Promise rejection. Preserve FE-11 for asynchronous frontend code.
- **FE-17 — Safe rendering (lines 159–163).** Avoid `dangerouslySetInnerHTML` whenever possible to mitigate XSS. Prefer safe component rendering of dynamic content; do not bypass input/output validation and encoding.
- **FE-18 — Library size (lines 165–169).** Before adding a library, check its size and bundle/performance impact using appropriate evidence, such as Bundlephobia or Webpack Bundle Analyzer. Avoid significantly harming application performance, and satisfy the separate open-source approval requirement REVIEW-20.
- **FE-19 — Timer cleanup (lines 171–175).** Unregister timers created during mounting in effect cleanup, for example `clearInterval` for `setInterval` and corresponding cleanup for other timers, to avoid leaks.
- **FE-20 — Image alternative text (lines 177–185).** Provide meaningful image `alt` text for accessibility and non-visual browsing, such as a description conveying the image's relevant content.
- **FE-21 — Commit messages (lines 187–189).** When asked to prepare or make commits, write small, understandable messages clearly describing the changes. This requirement does not authorize creating a commit without the user's request.
- **FE-22 — Immutable reducers (lines 191–200).** Do not mutate reducer state objects directly; return new state objects/arrays for changes, for example `[...state, action.payload]`. Ensure nested updates do not mutate existing state either.
- **FE-23 — Optimistic mutation/cache updates (lines 202–311).** Use `optimisticResponse` rather than refetching after a mutation, and maintain an accurate cache consistent with the eventual server response. Preserve the source example's essential flow: define the mutation and selected fields with `gql`; call it through `useMutation`; provide variables and an optimistic entity with required fields, `__typename`, and a temporary ID; provide a correctly shaped mutation `optimisticResponse`; update the cached collection using the project's supported APIs, such as `cache.modify` and `cache.writeFragment`; handle and log mutation failures appropriately; clear form input **after success**. Reconcile optimistic and server results without duplicate entries or temporary-ID collisions, and handle failure/rollback correctly. Inspect the installed Apollo/cache APIs instead of assuming the example's exact version. If a mutation cannot be represented accurately with this approach, surface the conflict rather than silently substituting refetching and claiming compliance.

### Example conflicts and limitations

Preserve the source snapshots, but do not copy their incidental defects into production code. In particular, the optimistic-response sample uses `async`/`await` despite FE-11, a default export despite JS-17's preference for named exports, a random temporary ID that is not guaranteed unique, and clears the input after the catch even on failure despite the prose saying “after successfully adding”. Implement the stated behavior using Promises, appropriate exports, safe cache identities, and success-only input reset. Check optimistic/server cache reconciliation rather than blindly appending duplicates. Its example endpoint/data model does not authorize changing the product schema or installing `@apollo/client`.

The review process's unresolved checklist link is addressed by the bundled general checklist. The open-source approval policy remains unavailable and must be obtained when applicable. Keep the earlier wasted-render reference and screenshot limitations visible too. Do not claim that copying a linked document means its unavailable linked policies, attachments, or examples have been independently verified.

## Completion gate

Before saying the task is complete:

- Check all **112 rule IDs**: JS-01–JS-17, REACT-01–REACT-13, REDUX-01–REDUX-04, GQL-01–GQL-04, PROCESS-01–PROCESS-15, REVIEW-01–REVIEW-36, and FE-01–FE-23. Every rule needs an explicit working-ledger outcome; no silent skips. `N/A` means outside the task, a workflow stage not requested yet, an unused documented alternative, or a requirement explicitly superseded by the confirmed repository policy, not “forgotten”. Mark the legacy JUnit gate REVIEW-18 `N/A` under that policy; missing unit tests are not a blocker. Genuinely unresolved requirements, such as missing required dependency approval or unavailable automation verification, must still be disclosed rather than assumed satisfied.
- Check applicable rules, exceptions, confirmed overrides, and known limitations using this skill. Read an optional source only if needed to resolve a concrete uncertainty; no reference read is required when these instructions are clear. Do not claim unread references were inspected or mark the task incomplete merely because they remain unread.
- Review applicable naming, constants, control flow, iteration, imports/exports, component shape/size, hooks, form handling, rendering/accessibility, selector identity, dispatch batching, reducer immutability, backend scalar evidence, mutation/cache behavior, input/output security, errors/cleanup, dependencies, documentation, and TestCafe/Playwright automation against the final code. Fix in-scope self-review findings before handoff. Preserve the confirmed testing override even if a historical reference is consulted; do not restore its superseded unit-test requirements.
- When preparing a PR/review request, include Problem, Approach And Fix, Testing done, and Testing to be done by QA. Verify unreleased-code privacy before publishing. Report pending reviewer/QA gates separately from coding/test completion; do not request publication, assign reviewers, change visibility, submit a review, or merge on the user's behalf without authorization. Preserve the two-reviewer-then-QA-then-merge sequence.
- Report checks actually run and their results. Distinguish verified compliance from assumptions, unavailable evidence needed for the task, unrun tests, and unresolved conflicts. Optional references left unread are not failures and do not need routine reporting. Do not promise that a skill can mechanically guarantee future adherence; enforce the rule-by-rule verification and targeted-clarification workflow instead.
- Keep the final report focused on the requested task and important verification results. Include the full ledger when asked or when it helps explain a compliance gap; otherwise retain the detailed check as working evidence and disclose every relevant limitation.
