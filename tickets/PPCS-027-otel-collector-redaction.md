id: PPCS-027
title: Route app telemetry through a custom OTel Collector with redaction
type: feature
difficulty: 3

## Brief
We want app telemetry in the Lakehouse, but promo payloads carry customer/member
and pricing data that must **not** land in `otel_logs`. Instead of the native
zero-config sidecar, stand up a **custom OpenTelemetry Collector**: instrument
the app to export OTLP to the Collector, add a **redaction / attributes
processor** that strips sensitive fields, then export to the **Zerobus OTLP
endpoint** (`x-databricks-zerobus-table-name` header) so only cleaned telemetry
lands in our governed Unity Catalog tables.

## Acceptance
- App emits OTLP to the custom Collector (not straight to the native sidecar).
- The Collector pipeline redacts/drops the sensitive promo fields before export.
- Telemetry reaches the team's UC telemetry tables via Zerobus, and a sample/test
  shows a sensitive field is **absent** downstream.

## Notes for the dispatcher
The 301 capstone: it operationalizes the telemetry lesson — the control for
"don't leak sensitive data into telemetry" isn't developer discipline, it's a
**redaction processor in the pipeline**. Watch for the agent shortcutting
straight to the Zerobus exporter and skipping the redaction stage.

> Deploy note: redaction processors are standard OTel Collector components
> (vendor-neutral); the exact way the custom Collector is hosted alongside a
> Databricks App is a deploy-layer detail to confirm against the workspace.
