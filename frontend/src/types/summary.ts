export interface ByType {
  _id: string;
  total_auh: number;
}

export interface Overall {
    _id: string | undefined ;
  grand_total_auh: number;
}

export interface SummaryResponse {
  auh_by_type: ByType[];
  overall: Overall[];
}
