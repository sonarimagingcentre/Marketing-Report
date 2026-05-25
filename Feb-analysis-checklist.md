# February–March Analysis Prompt Checklist

- Ingest February Excel (same structure as January) plus the first‑week‑of‑March file (`MARCH MARKETING 2026`) and normalize doctor names, KNH, marketer, and patient IDs (including numeric-only).
- Concatenate the two sources before processing so the dataset covers late February through early March.
- Compute total patients by row count (not unique) and group doctors by >5 vs ≤5 referrals.
- Produce summary KPIs: total patients, total doctors, % patients from >5, % doctors with >5.
- Generate high/low tables with doctor, marketer, patients (row count), and revenue (Row Total).
- Build chart for >5 doctors with total patients and revenue tooltip.
- Update executive summary text and insights to match the combined metrics.
- Regenerate data files: doctor_referrals_with_revenue.json and doctor_referrals_with_revenue.js (new logic handles multiple input files).
- Refresh web_report/index.html, web_report_feb/* and web_report/including-revenue.html with updated labels/date ranges and totals.
- Verify local load (file://) and GitHub Pages compatibility (relative paths, logo, data).
- Validate marketer column visibility and mobile responsiveness.
