# Pre-submission review

**25 October 2026 · Scope: supplied PRD, current source, executed evidence, application and project board.**

This is a project evidence review, not an official assessment decision. The original handbook was not available for independent comparison.

## Outcome

Explicit evidence is present for the seven criteria listed in the PRD. Preparation is reproducible, numerical findings agree with versioned evidence, and the dashboard separates executive interpretation, analytical detail and governance limits. The reflection evaluates recorded decisions and shortcomings without inventing user feedback.

A public deployment is not verified. Student understanding and the original handbook mapping remain unconfirmed. The repository and board are private, so assessor access must also be checked. These external conditions are not marked complete.

## Corrections made during review

| Finding | Correction |
|---|---|
| The outcome explanation assumed fewer leavers in every filtered cohort | Use a neutral explanation based on outcome counts; filtered populations can have a different balance |
| A comparison could display an empty plot when every group was withheld | Explain the withheld result and retain group sizes; a regression test covers two six-record groups |
| Preparation could overwrite v1 after a schema-valid source change | Check the reviewed source hash before writing; a regression test rejects a valid-looking altered source |

## Criterion coverage

| Criterion | Evidence reviewed |
|---|---|
| 1.1 · Ethics, privacy and governance | [README safeguards](../README.md#ethics-privacy-and-governance), Governance page, [source terms](../data/SOURCE.md), small-group rules |
| 1.2 · Legal and social implications | [Legal discussion](../README.md#legal-and-social-implications), Governance page, primary sources and guidance-under-review notice |
| 2.1 · Communication for different audiences | Overview narrative, Lab calculations, technical expanders and [notebook 03](../jupyter_notebooks/03_analysis_and_hypotheses.ipynb) |
| 2.2 · Visuals and narrative | Bars, box plots, histograms, explanations, filter/reset states and [browser evidence](qa/browser_results.json) |
| 2.3 · Structured documentation | README, executed notebooks, [dictionary](../data/processed/v1/data_dictionary_v1.csv), labels and reproduction commands |
| 3.1 · Project planning | Project board, [plan](plan.md), [lifecycle](lifecycle.md), maintenance, updates and evaluation |
| 3.2 · Reflection | [Execution review](retrospective.md), [changelog](CHANGELOG.md) and recorded implementation corrections |

## Verification

The source contains 1,470 records, including 237 recorded as attrited. H1, H2 and H4 are descriptively Supported; H3 remains Mixed. No causal effect, individual score, invented trend or financial saving is claimed.

The automated suite has 18 passing cases. The three notebooks execute without error outputs, and v1 reproduces without a data diff. Browser, accessibility and Linux-container results retain their stated limitations; no formal accessibility conformance or screen-reader audit is claimed.

Source attribution and derivative-database terms remain present. The submission archive excludes Git history, local dependencies and temporary verification copies.

## Recommendation

The technical candidate is suitable for final owner/student review against the supplied PRD. Use the [assessor walkthrough](assessment_walkthrough.md), resolve hosting and sharing before claiming a live release, and confirm the handbook mapping and student understanding before submission. Independent stakeholder feedback would strengthen evaluation; the PRD permits the accurately labelled scenario-based checks already recorded.
