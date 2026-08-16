from app.repositories.report_repository import (create_report,get_category_by_id,find_duplicate_report,)


class ReportService:

    @staticmethod
    def create_new_report(user_id: str,report_data):

        category = get_category_by_id(report_data.category_id)

        if not category:raise ValueError("Invalid category.")
        data = report_data.model_dump()

        data["report_type"] = (report_data.report_type.value)

        data["visibility"] = (report_data.visibility.value)

        data["importance"] = (report_data.importance.value)

        duplicate = find_duplicate_report(user_id,data)

        if duplicate:
            raise ValueError("You have already submitted a similar active report.")

        report_id = create_report(user_id,data)

        return {"message": "Report created successfully.","report_id": report_id,}