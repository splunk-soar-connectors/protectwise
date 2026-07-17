**Unreleased**

* Escape connector output before embedding values in widget JavaScript contexts.
* Encode caller-controlled identifiers as individual URL path segments before calling ProtectWise API endpoints.
* Report ProtectWise reputation and packet-capture server failures as action errors instead of successful empty results.
* Retain scheduled-ingestion checkpoints when event retrieval or persistence fails so affected events can be retried.
