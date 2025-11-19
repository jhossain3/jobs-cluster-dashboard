// src/pages/__tests__/AuhPerTypeChart.test.tsx
import { render } from "@testing-library/react";
import AuhPerTypeChart from "../components/AuhPerType"
import { ByType } from "../types/summary";

// Mock Chart component from react-apexcharts
jest.mock("react-apexcharts", () => (props: any) => {
  return (
    <div data-testid="chart">
      <div data-testid="categories">{JSON.stringify(props.options.xaxis.categories)}</div>
      <div data-testid="series">{JSON.stringify(props.series)}</div>
    </div>
  );
});

describe("AuhPerTypeChart", () => {
  it("renders chart with correct categories and values", () => {
    const mockData: ByType[] = [
      { _id: "mesh", total_auh: 0 },
      { _id: "solve", total_auh: 5120 },
      { _id: "postpro", total_auh: 0 },
    ];

    const { getByTestId } = render(<AuhPerTypeChart auhPerType={mockData} />);

    expect(getByTestId("categories").textContent).toContain("mesh");
    expect(getByTestId("categories").textContent).toContain("solve");
    expect(getByTestId("categories").textContent).toContain("postpro");

    expect(getByTestId("series").textContent).toContain("0");
    expect(getByTestId("series").textContent).toContain("5120");
    expect(getByTestId("series").textContent).toContain("0");
  });

  it("renders empty chart when auhPerType is undefined", () => {
    const { getByTestId } = render(<AuhPerTypeChart auhPerType={undefined} />);
    expect(getByTestId("categories").textContent).toBe("[]");
    expect(getByTestId("series").textContent).toContain("[]");
  });
});
