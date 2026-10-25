# Reflection on project execution

This review evaluates the delivery decisions, observed results and remaining limitations against the project plan.

## Outcome against the plan

RetainWise delivers the planned aggregate workforce analysis across five pages, with reproducible preparation, exact hypothesis evidence and a dedicated governance view. Three notebooks execute from fresh kernels, the versioned outputs reproduce, and the final suite contains 16 passing tests. Browser, keyboard and Linux-container checks provide separate evidence that the calculations can be used through the interface.

The strongest part of the delivery is the connection between evidence and interpretation. The satisfaction hypothesis remains Mixed rather than being rewritten to fit the results. The main limitations are equally clear: no independent stakeholder feedback has been collected, and a public deployment has not been verified. A functioning local product is useful evidence, but it does not establish that an assessor can open a hosted application or that HR users understand its limits.

## Analytical and ethical decisions

**Source terms required a check.** The Kaggle metadata lists “Database: Open Database, Contents: Database Contents”. Treating the dataset as generically public-domain would have been inaccurate. The acquisition record preserves the actual label and distinguishes source-data terms from project code.

**The satisfaction hypothesis needed a qualified result.** Rates fall between categories 1 and 2, rise slightly at 3, then fall at 4. The analysis retains the original question and labels H3 Mixed rather than smoothing the chart or rewriting the hypothesis.

**Filtering changes the evidence.** Intersecting department, role, travel and overtime can yield no rows or a very small cohort. The interface provides an explicit empty state, a reset action, minimum-group withholding and denominators. The Hypothesis Lab stays on the full population so its declared baseline cannot silently change.

**A cleaner file is not an anonymous population.** Removing EmployeeNumber reduces unnecessary exposure but does not establish anonymity. Box plots and histograms send aggregate statistics to the browser; no raw-record download is offered. Documentation explains why repeated filtering still needs a disclosure-control review for real data.

**Hosting must fit the required stack.** A worker runtime cannot replace the persistent Python process required by Streamlit. Rewriting the capstone into a different stack would weaken reproducibility. The project retains Streamlit and supplies a tested container, Render blueprint and Community Cloud procedure, with live status recorded separately from local runtime checks.

**Plain language still needs precision.** “Attrition rate” can imply a time-based measure. The app clarifies that this source provides a snapshot proportion without dates. Income remains in source units, avoiding a currency assumption. These choices limit the story but make it defensible.

These restrictions reduced the number of claims the product could make, but improved the quality of the claims it retained. Adding individual predictions, time trends or estimated savings would have introduced questions the source cannot answer. The descriptive scope therefore served the business question and governance requirements better than additional modelling would have.

## Implementation and validation

**Correct numbers did not guarantee a useful chart.** Screenshot inspection showed that precomputed box summaries overlapped because the traces lacked separate categorical positions. Explicit outcome positions fixed the comparison, and a regression assertion now checks those labels. A blanket update of Streamlit width arguments also exposed a version-specific Plotly warning; chart calls retain the supported argument while tables and buttons use the newer one. Visual review therefore added evidence that execution-only tests could not supply.

**Account permissions constrained automation.** The bot's token supports repository and project writes but not workflow changes. The CI definition is preserved as a template rather than presented as an active or passing remote workflow. Local execution remains the recorded QA evidence.

**The final review found problems outside the calculations.** Document links inside the app initially resolved as application routes; they now point to their repository files. A retained verification copy also exposed overly broad test discovery, so the suite explicitly targets the tests directory. These checks protect the review experience as well as the analytical results.

**Accessibility required testing the rendered interface.** The automated audit found framework control-label issues and low-contrast captions. Updating Streamlit, adding chart descriptions and correcting caption opacity and inline-code colours removed the detected violations. Four keyboard tasks were then exercised. This provides useful evidence without claiming a screen-reader audit or formal conformance.

**Release portability was tested directly.** The runtime container was built from pinned requirements, served all five pages and passed its health check as a non-root user. The remaining hosting dependency is account access, rather than an untested application package.

The tests were most useful when they covered different kinds of failure. Source validation catches invalid categories and impossible values; calculation tests protect the headline figures; browser inspection catches presentation errors; keyboard tasks test an interaction path that pointer-based checks miss. Passing one layer could not replace the others. The overlapping box plots were a concrete example: correct quartiles alone did not produce a readable comparison.

## Planning and scope

Keeping the original business requirements and hypotheses visible helped prevent scope drift. Optional comparisons were deferred, individual scoring remained outside the product boundary, and effort went into reproducibility, explanation and review evidence. The project board distinguishes completed technical work from hosting and stakeholder activities that have not occurred.

Hosting and account permissions should have been checked earlier. Discovering those dependencies during release preparation left the technical package ready before the public release route was available. The container and deployment blueprint reduce the remaining setup work, but they cannot replace an authorised hosting connection. The same distinction applies to continuous integration: a prepared workflow is not an active remote check.

## What a second iteration should change

Recruit an HR reader, an analyst and a governance reviewer before polishing additional features. Ask each to complete the recorded tasks and explain one limitation in their own words. Their actual responses should determine whether the page hierarchy and narrative are clear; more charts would not resolve a misunderstanding of denominators or causality.

Add a screen-reader review alongside the automated accessibility checks, and verify the live app from a signed-out assessor's perspective. A private repository, project board or hosted address needs an explicit sharing plan. Review access and deployment permissions at the start of the next release rather than at its end.

Preserve v1 as the reproducible baseline. A new source population or revised transformation should produce a reviewed v2, with schema checks, changed metrics and governance implications recorded together. If real workforce data is proposed, the first step is a purpose, lawful-basis and disclosure review—not replacing the fictional CSV and treating the existing safeguards as sufficient.
