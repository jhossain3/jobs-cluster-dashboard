// src/pages/AuhPerTypeChart.tsx
import React from "react";
import Chart from "react-apexcharts";
import { ByType } from "../types/summary";

interface AuhPerTypeChartProps {
  auhPerType: ByType[] | undefined;
}

const AuhPerTypeChart: React.FC<AuhPerTypeChartProps> = ({ auhPerType }) => {

  console.log('summary', auhPerType)
  
  const categories = auhPerType?.map((item) => item._id) || [];
  const values = auhPerType?.map((item) => item.total_auh) || [];
  const options: ApexCharts.ApexOptions = {
    chart: { type: "bar" },
    xaxis: { categories },
    title: { text: "Task Counts" },
  };

  const series = [{ name: "Values", data: values }];

  return <Chart options={options} series={series} type="bar" height={350} />;
};

export default AuhPerTypeChart;
