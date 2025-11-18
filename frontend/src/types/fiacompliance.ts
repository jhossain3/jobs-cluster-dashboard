export interface FiaCompliance {
  period: string;
  start_date: string;   // ISO string from API
  end_date: string;     // ISO string from API
  current_auh: number;
  limit: number;
  limit_exceeded: boolean;
}
