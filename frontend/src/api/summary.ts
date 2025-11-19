import { SummaryResponse } from "../types/summary";

//call summary report endpoint with start and end date as query parameters
export async function fetchSummaryReport(
  startDate: string,
  endDate: string
): Promise<SummaryResponse> {
  const url = `http://127.0.0.1:8000/summary/report?start_date=${encodeURIComponent(
    startDate
  )}&end_date=${encodeURIComponent(endDate)}`;
    console.log("url", url);
  const res = await fetch(url);

  console.log("url", url);

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  console.log('res',res)

  return res.json();
}
