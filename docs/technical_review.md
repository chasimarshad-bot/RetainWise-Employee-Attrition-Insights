# Technical review guide

These notes explain the implemented decisions. They support review and discussion; they do not claim that a particular person has completed that review.

## Why use descriptive analysis?

The source is a fictional snapshot without exit dates or recorded reasons for departure. Descriptive comparisons answer the stated business questions without adding an individual prediction system. No classification model, train/test split, probability score or employee ranking is needed for this product.

## How is attrition calculated?

Attrition_Flag maps Yes to 1 and No to 0. The group mean multiplied by 100 is the observed percentage: 237 / 1,470 × 100 = 16.12244898%. The observation window is unknown, so this is not an annual turnover measure. An overtime rate gap subtracts the No rate from the Yes rate: 30.52884615% − 10.43643264% = 20.09241352 percentage points.

## Why retain a Mixed hypothesis?

The four satisfaction rates are approximately 22.84%, 16.43%, 16.52% and 11.33%. The endpoints follow the statement's direction, but category 3 rises slightly above category 2. A monotonic conclusion would discard contradictory evidence. The original statement and all four denominators remain visible.

## Why show both medians and distributions?

A mean can conceal skew and group overlap. Box plots show medians and the middle half of each outcome group. Histograms use shared bins and within-outcome percentages because retained records substantially outnumber attrited records. Income remains in source units because its currency is not documented.

## What changed during preparation?

EmployeeNumber is excluded as an unnecessary identifier. EmployeeCount, Over18 and StandardHours are excluded only after checking that each is constant. Readable outcome labels are retained, and four transparent fields are derived. Missing-value checks do not justify imputation because this source has no missing values. No outlier deletion or resampling is performed.

## What does withholding achieve?

Attrition counts and rates are withheld below n=10; groups below n=30 are flagged. The rule discourages strong interpretation of very small fictional groups. It does not guarantee anonymity for real workers: combinations of attributes and repeated filtering can disclose information. Real use needs a separate access and disclosure policy.

## How can the work be reproduced?

The raw file's hash identifies the acquired source. Notebook 02 writes the v1 dataset, dictionary and metadata. Notebook 03 writes exact hypothesis evidence. The app reads the processed dataset and reuses the same analytical functions. Fresh-kernel execution, regression tests and byte-preserving CSV storage support reproducibility. A new source population requires a reviewed version rather than an undocumented overwrite of v1.

## What would change in a second release?

First collect real stakeholder feedback and test whether readers distinguish counts, proportions and percentage-point differences. Review keyboard and assistive-technology behaviour. If real workforce data were proposed, assess lawful basis, transparency, access, retention, DPIA requirements and worker consultation before any ingestion. Dated records and better variable definitions would be prerequisites for time-based analysis; they should not be invented from this source.
