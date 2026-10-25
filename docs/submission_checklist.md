# Submission checklist

**Review date: 25 October 2026. Deadline in the supplied PRD: 25 October 2026, 23:59:59 Europe/London.**

## Technical evidence

| Requirement | Evidence and result |
|---|---|
| Clear problem and audience | README business case and three audience roles |
| BR1–BR5 | Five dashboard pages with findings, aggregate comparisons and responsible-use boundaries |
| H1–H4 | Notebook 03, Lab and versioned evidence JSON; H3 remains Mixed |
| Reproducible preparation | Three executed notebooks, source checksum, validation and dedicated v1 output |
| Multiple useful visuals | Count/rate bars, box plots and shared-bin histograms with explanations |
| Ethics and legal context | Dedicated governance page; source terms, disclosure limits and primary references |
| Planning through evaluation | Project board, lifecycle, maintenance/update plan and factual execution review |
| Testing evidence | Automated data/app tests, browser results, keyboard tasks and accessibility findings |
| Reviewable package | Source archive with revision/checksum manifest, walkthrough and evidence map |

The exact results and remaining test limitations are recorded in [testing.md](testing.md); the [pre-submission review](pre_submission_review.md) maps the reviewed evidence to each criterion. This checklist is an evidence index, not an assessment grade or a claim of formal accessibility conformance.

## Final checks requiring the owner or student

1. **Student review:** Ch Asim must read the completed [execution reflection](retrospective.md), review the evidence and confirm his understanding. [technical_review.md](technical_review.md) supports that discussion but does not attest to it.
2. **Handbook confirmation:** compare [evidence_matrix.md](evidence_matrix.md) with the actual assessment handbook. The mapping currently follows the supplied PRD; the original handbook was not provided.
3. **Hosting and assessor access:** the live Streamlit dashboard passed the hosted smoke check in [deployment.md](deployment.md). Ensure the assessor can also access the private repository/project or the exported archive.

## Optional strengthening

Independent HR, analyst and governance feedback would strengthen the evaluation. No external participants are claimed. The recorded scenario-based checks follow the PRD's allowance for self-testing when independent participants are unavailable. A screen-reader audit would add accessibility evidence; automated checks and keyboard tasks do not replace it.

An active GitHub Actions workflow is also useful but is not one of the seven listed assessment criteria. The template can be enabled after the owner grants workflow permission; local validation remains the executed evidence.
