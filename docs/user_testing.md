# Usability scenarios

No external participants have taken part. The evidence below records automated, scenario-based checks, not independent user feedback or a claim about user satisfaction.

| Perspective and task | Expected result | Actual evidence | Issue and change | Retest |
|---|---|---|---|---|
| HR: find overall attrition | 237/1,470; 16.1% to one decimal | AppTest verifies the displayed overview KPIs against source calculations | No KPI discrepancy found | Passed |
| HR: identify one workplace association and a limit | Overtime rates with denominators; no causal claim | Notebook 03 and Lab show 30.53% vs 10.44%; overview includes absent-hours/exit-reason limitations | Avoided describing this snapshot as annual turnover | Calculations and rendered page checks passed |
| HR: narrow a group to no results | Clear message and a working reset | AppTest clears Department and restores the full population | Explicit empty state added; empty does not mean all | Passed |
| HR: compare a cohort whose groups are all too small | An explanation and group sizes without a misleading empty chart | Regression fixture contains two six-record groups; the rate chart is withheld with an explicit message | Added a separate fully withheld state | Passed |
| Analyst: inspect a hypothesis denominator | Full-population n and rates in Lab detail | AppTest executes Lab; notebook outputs record all group sizes | Lab explicitly ignores sidebar filters to preserve baseline | Passed |
| Analyst: verify a derived field | Age/tenure intervals and flag mapping in dictionary/notebook | Notebook 02 executes; boundary tests check band edges | Bands are documented, with out-of-range ages rejected | Passed |
| Governance: determine whether records are real | Fictional nature visible before audit interpretation | Governance page renders with source statement and responsible-use boundaries | Avoided treating identifier removal as anonymisation | Page execution passed |
| Governance: find prohibited uses and demographic limitations | No individual targeting; source-label caveats | Dedicated panels and legal/social explanation on Governance | Added guidance-under-review notice and differencing caveat | Page execution passed |

Browser navigation, responsive layouts and explorer interaction checks are recorded separately in `docs/testing.md`. Early browser checks failed because the test assumed navigation accessible names excluded Material icon text; the selector was corrected to use actual page links. This was a test-harness issue, not evidence that a user could not navigate.

## Independent review still needed

Ask one non-technical HR reader, one analyst and one governance reader to attempt the tasks above without prompting. With permission, record role, date, task completion, their explanation of a limitation, difficulties, changes and retest outcomes. Do not fill those results until people actually participate.

Ch Asim should also explain each hypothesis calculation and transformation in his own words. Automated success does not establish student understanding.

Use the [independent feedback session guide](final_review.md) to record real responses and follow-up changes.
