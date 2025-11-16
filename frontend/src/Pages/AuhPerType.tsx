// src/pages/AuhPerTypeChart.tsx
import React from "react";
import Chart from "react-apexcharts";

const AuhPerTypeChart: React.FC = () => {
  const options: ApexCharts.ApexOptions = {
    chart: {
      type: "bar",
    },
    xaxis: {
      categories: ["postpro", "mesh", "solve"],
    },
    title: {
      text: "Task Counts",
    },
  };

  const series = [
    {
      name: "Values",
      data: [0, 0, 3000], // postpro=0, mesh=0, solve=3000
    },
  ];

  return <Chart options={options} series={series} type="bar" height={350} />;
};

export default AuhPerTypeChart;
