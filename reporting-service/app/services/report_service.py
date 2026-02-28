from app.events.consumer import stats

class ReportService:
    def get_dashboard_metrics(self):
        # We could also do synchronous HTTP calls here to get accurate account counts
        # e.g. CALL ACCOUNT SERVICE to get precise account count if we want to augment stats.
        # But this suffices for an event-driven aggregated view.
        return stats

report_service = ReportService()
