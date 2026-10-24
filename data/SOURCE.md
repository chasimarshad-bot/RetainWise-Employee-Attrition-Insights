# Source and attribution

**IBM HR Analytics Employee Attrition & Performance**, published on Kaggle by Pavan Subhash (`pavansubhasht`). The source describes fictional records created by IBM data scientists for analytics practice. These are not IBM's actual employees.

- Dataset: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- Download: https://www.kaggle.com/api/v1/datasets/download/pavansubhasht/ibm-hr-analytics-attrition-dataset
- Metadata: https://www.kaggle.com/api/v1/datasets/view/pavansubhasht/ibm-hr-analytics-attrition-dataset
- Acquired: 24 October 2026, directly from Kaggle, without a third-party mirror.
- Original file: `WA_Fn-UseC_-HR-Employee-Attrition.csv`; 1,470 rows, 35 columns.
- Original SHA-256: `a5c31e38bd7fafc9bc333884eb181b06b41b8e5e488e8f7ccb27199fb3be7659`.

## Source terms

Kaggle's first-party metadata lists **Database: Open Database, Contents: Database Contents**. This corresponds to the [Open Database Licence (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/) and [Database Contents Licence (DbCL)](https://opendatacommons.org/licenses/dbcl/1-0/). Retain these notices and comply with the applicable attribution and share-alike obligations when redistributing database derivatives. This project does not relabel the source as CC0 or apply its code licence to the source data.

The untouched raw CSV is retained for reproducibility. The derived v1 database excludes four fields and adds four documented fields, preserving source records. Source metadata is recorded separately in `data/source_record.json`; processing hashes and transformations are in `data/processed/v1/metadata_v1.json`.

The v1 derivative database is made available under ODbL 1.0, with its contents under DbCL 1.0, retaining the source attribution above. A copy is included in this repository, and the transformation code is in `retainwise/data.py` and notebook 02.

## Interpretation limits

There is no dated observation window, causal design, exit explanation or documented currency. Outcome imbalance and the small fictional population constrain comparisons. Category scales are source labels, not validated measures of real employee experience. The binary Gender field excludes other identities and must not be treated as a legal definition of sex. No result should be extrapolated to an employer's actual workforce.
