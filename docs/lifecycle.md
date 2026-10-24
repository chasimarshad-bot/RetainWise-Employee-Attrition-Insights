**Discovery and planning.** The supplied PRD defines HR leadership, analysts and governance reviewers as distinct audiences. BR1–BR5 and H1–H4 are the scope baseline. The deadline is 25 October 2026, 23:59:59 Europe/London; the plan prioritises reproducible evidence over optional modelling.

**Preparation and analysis.** Retrieve the source from Kaggle, verify its hash, validate the schema and categories, then execute notebooks 01–03. Preserve raw records unchanged. Write reviewed outputs to `data/processed/v1`; publish descriptive evidence and its limitations together.

**Dashboard and testing.** Reuse analytical functions across notebooks and pages. Check denominators, hypothesis rules, navigation, empty and narrow cohorts, responsive layouts and chart alternatives. Record actual outcomes in `docs/testing.md`. External stakeholder feedback remains a separate activity from automated checks.

**Release.** Require passing automated checks, fresh notebook execution, a source-licence review, no secrets, a clean repository and a working deployment before claiming a live release. The repository is private; deployment must preserve appropriate access. Deployment instructions are in `docs/deployment.md`.

**Maintenance.** The student/project maintainer owns this educational release. There is no scheduled refresh of the static fictional dataset. Before each submission or demonstration, check dependencies, source links, notebook reproducibility and legal references. In a real service, the HR data owner would approve a refresh schedule and the governance owner would review lawful basis, retention, access and worker communications. Review access quarterly and after role changes; investigate errors before republishing.

**Updates.** Do not overwrite v1 with a different population. Create a v2 folder, review schema and licence changes, record transformations and checksums, rerun notebooks and regression tests, compare headline metrics, review disclosure risk and update documentation. Retain v1 for educational reproducibility; retention of real employee versions would require a separate, justified policy.

**Evaluation and retirement.** Ask an HR user to find a pattern and state its limitation, an analyst to reproduce a number, and a governance reviewer to find the prohibited uses. Record task completion, misunderstandings and corrections without inventing feedback. Reassess whether the dashboard meets its purpose; archive the release and remove hosting/access when its purpose ends, applying any real-data deletion schedule.
