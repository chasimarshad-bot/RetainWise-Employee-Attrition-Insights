Final checks performed on 25 October 2026 using an isolated Python 3.12.8 environment on Windows and a Linux runtime container. Streamlit is pinned to 1.66.1. The initial checks on 24 October are retained as the baseline. These are executed build checks, not external user feedback.

| Check | Executed result |
|---|---|
| Fresh-kernel notebooks 01–03 | All completed without a cell error, including rerun after chart corrections |
| Recreate v1 | Processed CSV, dictionary, metadata and hypothesis JSON reproduced without Git diff |
| Fresh remote checkout | Cloned the pushed repository from GitHub; all three notebooks, 15 tests and v1 reproduction passed using the isolated Python environment |
| pytest | 16 passed; includes source rejection, band boundaries, known figures, hypothesis outcomes, small cells, empty/reset behaviour, all page functions, explorer measures, audit selectors and document-link resolution |
| Browser pages | All five pages returned HTTP 200 at 390×844, 768×1024 and 1440×1000; no Streamlit exception or horizontal page overflow |
| Actual navigation | All four non-default sidebar page links opened their expected heading |
| Explorer controls | Satisfaction and monthly-income selections worked; chart SVGs rendered |
| Chart payloads | Boxes contain precomputed summaries, without individual points; histograms contain bin aggregates |
| Visual inspection | Reviewed desktop/mobile screenshots, rate labels and separate income-box positions; corrected clipping, overlapping boxes and a version-specific chart warning |
| Dependency compatibility | `pip check` reported no broken requirements |
| Accessibility | axe-core 4.10.3: zero violations of selected WCAG 2 A/AA and 2.1 A/AA rules across five pages; incomplete rules remain for manual review |
| Keyboard tasks | Measure selection, tab switching, page navigation and technical disclosure activation passed using keyboard events |
| Linux container | Image built with runtime requirements; health endpoint and all five pages passed; process runs as non-root appuser |
| Links | No missing local document links; all checked public URLs returned 200; private board returns signed-out 404 and was verified through authenticated GraphQL |
| Content review | App modules and authored documentation checked for unfinished implementation markers, machine-specific paths and unsupported claims |

The suite grew from 13 to 16 checks as edge cases were identified. Early browser runs failed on a selector that omitted Material icon text from link names; using the real href corrected the harness issue. Screenshot review found overlapping box summaries and a clipped count label. These were fixed and retested. The final audit also corrected document links that resolved as app routes and restricted test discovery to the intended tests directory. Tests check explicit box categories, and browser QA rejects the observed deprecated-keyword warning.

Detailed results are in [browser results](qa/browser_results.json), [accessibility results](qa/accessibility_results.json), [container results](qa/container_results.json) and [submission verification](qa/submission_verification.json). Representative screenshots are retained in [screenshots](screenshots/). Run `python scripts/browser_qa.py` and `python scripts/accessibility_qa.py` with the app on localhost:8501 and Microsoft Edge installed to repeat the local checks. The CI template covers analytical/app tests and notebook reproduction. It is not activated because the owner's current token lacks workflow permission.

## Accessibility review and limits

The inspected layouts do not overflow the viewport. Labels, source-ordered scales, sample sizes, captions, outcome names, patterned histogram bars and expandable tables provide context beyond colour. Captions and axis labels use darker text for readability; long chart titles wrap. Charts are accompanied by text, but Plotly interaction and Streamlit's grid still need assistive-technology review.

Framework control labels and chart descriptions were improved by the Streamlit update. Caption opacity and inline-code colours were corrected after contrast findings. The repeated automated scan returned no violations for its selected rules. Four keyboard tasks passed. No formal WCAG conformance, exhaustive keyboard audit or screen-reader test is claimed. No independent users participated. See [user_testing.md](user_testing.md) for the scenario record.

## Release limits

The local Linux container is verified. A connected hosting account is still required for a public deployment, and no hosted-commit verification is claimed. See [deployment.md](deployment.md). Final student review and handbook confirmation remain separate from technical validation.
