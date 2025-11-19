import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

jest.mock("@mui/x-date-pickers/AdapterDateFns", () => ({
  AdapterDateFns: jest.fn(),
}));


describe("App", () => {
  it("renders Dashboard header", () => {
    render(<App />);
    expect(
      screen.getByText(/Mercedes AMG Petronas Cluster Jobs Tracker/i)
    ).toBeInTheDocument();
  });
});
