from ..db.mongo import jobs_collection
# from datetime import datetime, timedelta


class SummaryRepository:
    def __init__(self):
        self.collection = jobs_collection

    #aggregate the auh totals by job type and overall total within a date range
    async def get_summary(self, start_date, end_date):
        pipeline = [
            {"$match": {"start_time": {"$gte": start_date, "$lt": end_date}}},
            {
                "$facet": {
                    "auh_by_type": [
                        {
                            "$group": {
                                "_id": "$type",
                                "total_auh": {"$sum": "$calculated_auh"},
                            }
                        }
                    ],
                    "overall": [
                        {
                            "$group": {
                                "_id": None,
                                "grand_total_auh": {"$sum": "$calculated_auh"},
                            }
                        }
                    ],
                }
            },
        ]

        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)  
        return results[0] if results else {}


# testing code
# if __name__ == "__main__":
#     summary_repo = SummaryRepository()
#     start_date = datetime.fromisoformat("2025-10-01T06:28:39")

# # End date = start date + 1 day
#     end_date = start_date + timedelta(days=1)
#     summary = summary_repo.get_summary(
#         start_date=start_date,
#         end_date=end_date,
#     )
#     print(summary)
