Checks performed on 24 October 2026 using an isolated Python 3.12.8 virtual environment on Windows. These are executed build checks, not external user feedback.

| Check | Executed result |
|---|---|
| Fresh-kernel notebooks 01–03 | All completed without a cell error, including rerun after chart corrections |
| Recreate v1 | Processed CSV, dictionary, metadata and hypothesis JSON reproduced without Git diff |
| pytest | 15 passed; includes source rejection, band boundaries, known figures, hypothesis outcomes, small cells, empty/reset behaviour, all page functions, all explorer measures and audit selectors |
| Browser pages | All five pages returned HTTP 200 at 390×844, 768×1024 and 1440×1000; no Streamlit exception or horizontal page overflow |
| Actual navigation | All four non-default sidebar page links opened their expected heading |
| Explorer controls | Satisfaction and monthly-income selections worked; chart SVGs rendered |
| Chart payloads | Boxes contain precomputed summaries, without individual points; histograms contain bin aggregates |
| Visual inspection | Reviewed desktop/mobile screenshots, rate labels and separate income-box positions; corrected clipping, overlapping boxes and a version-specific chart warning |
| Dependency compatibility | `pip check` reported no broken requirements |
| Links | No missing local document links; all nine public URLs returned 200; private board returns signed-out 404 and was verified through authenticated GraphQL |
| Content review | No outstanding implementation markers or machine-specific paths found in app modules or authored documentation; source PRD retained as supplied |

The initial 13 checks passed before two further regression cases were added. Early browser runs failed on a test selector that omitted Material icon text from link names; using the real href corrected that harness issue. Screenshot review then found genuine chart defects: overlapping box summaries and a clipped count label. Both were fixed and the visual suite was rerun successfully. Tests now check explicit box categories, and browser QA rejects the observed deprecated-keyword warning.

Detailed browser results are in [qa/browser_results.json](qa/browser_results.json). Representative screenshots are retained in [screenshots](screenshots/). Run `python scripts/browser_qa.py` with the app on localhost:8501 and Microsoft Edge installed to repeat that local check. The supplied CI template covers analytical/app tests and notebook reproduction, not browser QA. It is not activated: the owner's current token lacks workflow permission.

## Accessibility review and limits

The inspected layouts do not overflow the viewport. Labels, source-ordered scales, sample sizes, captions, outcome names, patterned histogram bars and expandable tables provide context beyond colour. Captions and axis labels use darker text for readability; long chart titles wrap. Charts are accompanied by text, but Plotly interaction and Streamlit's grid still need assistive-technology review.

No formal WCAG conformance, full keyboard audit or screen-reader test is claimed. No independent users participated. See [user_testing.md](user_testing.md) for the recorded automated scenarios and independent-review protocol.

## Release limits

No authenticated Streamlit hosting session is available. Docker is installed but its engine is not running, so the supplied Dockerfile has not been built here. No live deployment or hosted-commit verification is claimed. See [deployment.md](deployment.md).
