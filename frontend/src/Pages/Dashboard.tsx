import React, { useEffect, useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Grid,
  Paper,
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
} from "@mui/material";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import DataUnavailable from "../components/DataUnavailable";
import AuhPerTypeChart from "../components/AuhPerType";
import { fetchSummaryReport } from "../api/summary";
import { SummaryResponse } from "../types/summary";

const DashboardPage = () => {
  const today = new Date();
  const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

  const [open, setOpen] = useState(false);
  const [startDate, setStartDate] = useState<Date | null>(today);
  const [endDate, setEndDate] = useState<Date | null>(startOfMonth);

  const [summary, setSummary] = useState<SummaryResponse | null>(null);

  useEffect(() => {
    fetchSummaryReport(today.toISOString(), startOfMonth.toISOString())
      .then((data) => {
        setSummary(data);
      })
      .catch((err) => console.error("Error fetching summary:", err));
  }, []);

  const handleSubmit = () => {
    if (!startDate || !endDate) {
      console.error("Please select both dates");
      return;
    }

    // Convert Date objects to ISO strings
    const startIso = startDate.toISOString();
    const endIso = endDate.toISOString();

    fetchSummaryReport(startIso, endIso)
      .then((data) => {
        console.log("Fetched summary:", data);
        setSummary(data);
        setOpen(false); // close dialog after submit
      })
      .catch((err) => console.error("Error fetching summary:", err));
  };

  return (
    <>
      {/* Header */}
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: "center" }}>
          <Typography align="center" variant="h6">
            Mercedes AMG Petronas Cluster Jobs Tracker
          </Typography>
        </Toolbar>
      </AppBar>

      <Container sx={{ mt: 4 }}>
        {/* Date Range Modal Trigger */}
        <Button variant="contained" onClick={() => setOpen(true)}>
          Select Date Range
        </Button>

        {/* Date Range Modal */}
        <Dialog open={open} onClose={() => setOpen(false)}>
          <DialogTitle>Select Date Range (up to 1 year ago)</DialogTitle>
          <DialogContent>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="Start Date"
                value={startDate}
                onChange={(newValue) => setStartDate(newValue)}
                maxDate={new Date()}
                minDate={
                  new Date(new Date().setFullYear(new Date().getFullYear() - 1))
                }
              />
              <DatePicker
                label="End Date"
                value={endDate}
                onChange={(newValue) => setEndDate(newValue)}
                maxDate={new Date()}
                minDate={
                  new Date(new Date().setFullYear(new Date().getFullYear() - 1))
                }
              />
            </LocalizationProvider>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleSubmit} variant="contained" color="primary">
              Submit
            </Button>
          </DialogActions>
        </Dialog>

        {/* Stat Boxes */}
        <Grid container spacing={2} sx={{ mt: 2 }} justifyContent="center">
          <Grid>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">Total AUH Count</Typography>
              {summary?.overall && summary.overall.length > 0 ? (
                <Typography variant="h4">
                  {summary?.overall[0].grand_total_auh}
                </Typography>
              ) : (
                <Typography variant="h4">N/A</Typography>
              )}
            </Paper>
          </Grid>
          <Grid>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">FIA AUH Limit</Typography>
              <Typography variant="h4">50000</Typography>
            </Paper>
          </Grid>
          <Grid>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">8 Week Limit Time Period</Typography>
              <Typography variant="body1">
                {startDate?.toLocaleDateString()} -{" "}
                {endDate?.toLocaleDateString()}
              </Typography>
            </Paper>
          </Grid>
        </Grid>
        {/* Chart */}
        {summary?.overall && summary.overall.length > 0 ? (
          <Box sx={{ mt: 4, height: 300 }}>
            <AuhPerTypeChart auhPerType={summary.auh_by_type} />
            {/* Example: show grand_total_auh from first element */}
            <Typography variant="h6">
              Grand Total: {summary.overall[0].grand_total_auh}
            </Typography>
          </Box>
        ) : (
          <DataUnavailable />
        )}
      </Container>
    </>
  );
};

export default DashboardPage;
