**Unreleased**
* Handle responses without a Content-Type header without raising a connector exception.
* Report scalar JSON responses as unsupported response shapes instead of raising a connector exception.
* Parse Z-suffixed hunt time parameters as UTC regardless of the SOAR host timezone.
* Preserve polling retry coverage when ProtectWise event-detail retrieval fails.
