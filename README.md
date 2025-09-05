# SafeAgri – FMIS ↔ Geobox Compliance Check

## Summary
Automated comparison of FMIS planning data with Geobox reference data and legal rules.  
Returns **permitted / not_permitted / notification_required**, visualizes buffers and no-spray zones, and generates an audit-proof report.

## Problem
- Complex, changing plant-protection and fertilization rules.
- Manual checks are slow and error-prone.
- Missing, inconsistent documentation for audits.

## Solution
- API bridge between **FMIS** and **Geobox** plus a rules engine.
- Map-based visualization of allowed vs. restricted areas.
- Machine-readable outputs for FMIS + human-readable PDF reports.
- Optional verification using machine telemetry (“before/after”).
