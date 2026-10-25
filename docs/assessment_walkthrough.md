# Assessor walkthrough

RetainWise is a Unit 3 capstone for Ch Asim Arshad. The audience is HR leadership, people analysts and governance reviewers. All employee records are fictional.

## Suggested review order

1. Read the README's business case, findings and limitations.
2. Run `python -m streamlit run app.py`, or use the verified hosted address if one is recorded in deployment.md.
3. On Executive Overview, check the 1,470-record population, 237 attrited records and 16.1% displayed attrition proportion. Open an aggregate figures table to inspect denominators.
4. On Workforce Patterns, compare satisfaction in source order. Open Tenure & compensation and compare the median and spread in the box plot. Use the histogram to compare distribution shapes rather than raw group sizes.
5. Clear a sidebar filter to check the empty state, then Reset filters. Narrow the cohort to see where small-group warnings or withholding apply.
6. On Hypothesis Lab, inspect each fixed statement, outcome and exact evidence. H3 remains Mixed because the middle satisfaction rates are not monotonic.
7. On Fairness & Governance, check demographic denominators, prohibited uses, real-data governance controls and legal caveats.
8. On Methodology & Project Plan, inspect preparation, dictionary, lifecycle and build evaluation.
9. Reproduce the notebooks and tests using the README commands. Use the evidence map to locate material for each criterion.

## Evidence by audience

| Reader | Start here | Supporting detail |
|---|---|---|
| HR Director | Executive Overview and its three discussion areas | Plain-English chart explanations and limitations |
| People Analyst | Hypothesis Lab and Workforce Patterns | Exact group sizes, means, quartiles, notebook 03 and evidence JSON |
| Governance reviewer | Fairness & Governance | Source terms, identifier exclusions, disclosure limits and lifecycle ownership |

## Assessment coverage

The seven criteria in [the evidence map](evidence_matrix.md) come from the supplied PRD. Source validation, executed analysis, dashboard communication, governance discussion, planning and a factual execution review are available for inspection. The original assessment handbook has not yet been independently checked against this mapping.

## Sharing and submission

The repository and project board are private. An assessor needs authorised GitHub access to use their links, or a copy of the source archive. A live app also needs suitable access for the assessor. Confirm these separately before submitting; a valid private link is not evidence that a signed-out assessor can open it.

`scripts/package_submission.py` exports the committed project into an archive with a revision and checksum manifest. It excludes local virtual environments, Git history, credentials and temporary test artefacts. The archive contains source, data notices, three executed notebooks, documentation, tests and screenshots.
