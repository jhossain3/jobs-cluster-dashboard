import React, { useEffect, useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Grid,
  Snackbar,
  Alert,
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
import { format } from "date-fns";
import { SummaryResponse } from "../types/summary";
import { FiaCompliance } from "../types/fiacompliance";
import mercedesAMGLogo from "../assets/mercedes_amg_logo.png";

const DashboardPage = () => {
  const today = new Date();
  const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

  const [open, setOpen] = useState(false);
  const [startDate, setStartDate] = useState<Date | null>(today);
  const [endDate, setEndDate] = useState<Date | null>(startOfMonth);
  const [compliance, setCompliance] = useState(false);
  const [fiaData, setFiaData] = useState<FiaCompliance | null>(null);
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [showPopup, setShowPopup] = useState(false);
  const [showBanner, setShowBanner] = useState(false);

  const fiaWindowStart = fiaData?.start_date;
  const fiaWindowEnd = fiaData?.end_date;
  const fiaLimit = fiaData?.limit;

  useEffect(() => {
    // 1️⃣ Fetch summary report
    fetchSummaryReport(today.toISOString(), startOfMonth.toISOString())
      .then((data) => {
        setSummary(data);
      })
      .catch((err) => console.error("Error fetching summary:", err));

    // 2️⃣ Fetch compliance snapshot
    fetch("http://localhost:8000/compliance/currentstatus")
      .then((res) => res.json())
      .then((data) => {
        setFiaData(data);
        setCompliance(data.limit_exceeded);
        if (data.limit_exceeded) {
          setShowPopup(true);
          setShowBanner(false);
        }
      })
      .catch((err) => console.error("Error fetching compliance status:", err));

    // 3️⃣ Open WebSocket for live compliance updates
    const ws = new WebSocket("ws://localhost:8000/compliance/ws/limit");

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("WebSocket update:", data);
        setCompliance(data); // update compliance state
      } catch (err) {
        console.error("Error parsing WS message:", err);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    // Cleanup on unmount
    return () => {
      ws.close();
    };
  }, []);
  console.log("compliance state:", compliance);
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

  const handleClosePopup = () => {
    setShowPopup(false);
    setShowBanner(true);
  };

  return (
    <>
      {/* Header */}
      <AppBar position="static" sx={{ bgcolor: "#000000" }}>
        <Toolbar sx={{ justifyContent: "center" }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            {/* Logo */}
            <img
              src={mercedesAMGLogo}
              alt="Mercedes AMG Petronas"
              style={{ height: 100 }}
            />

            <Typography align="center" variant="h6">
              Mercedes AMG Petronas Cluster Jobs Tracker
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>

      {showBanner && (
        <Box
          sx={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            bgcolor: "error.main",
            color: "white",
            textAlign: "center",
            py: 1,
            zIndex: 1300,
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: "bold" }}>
            ⚠️ AUH Limit Exceeded
          </Typography>
        </Box>
      )}

      <Snackbar
        open={showPopup}
        onClose={handleClosePopup}
        autoHideDuration={null}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          severity="error"
          onClose={handleClosePopup}
          sx={{ fontSize: "1.2rem", fontWeight: "bold" }}
        >
          ⚠️ AUH Limit Exceeded! Current: {fiaData?.current_auh} / Limit:{" "}
          {fiaData?.limit}
        </Alert>
      </Snackbar>

      <Container sx={{ mt: 4 }}>
        {/* Date Range Modal Trigger */}
        <Button
          sx={{ bgcolor: "#00A19B" }}
          variant="contained"
          onClick={() => setOpen(true)}
        >
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
                slotProps={{
                  textField: {
                   
                    margin: "normal",
                  },
                }}
              />
              <DatePicker
                label="End Date"
                value={endDate}
                onChange={(newValue) => setEndDate(newValue)}
                maxDate={new Date()}
                minDate={
                  new Date(new Date().setFullYear(new Date().getFullYear() - 1))
                }
                slotProps={{
                  textField: {
      
                    margin: "normal",
                  },
                }}
              />
            </LocalizationProvider>
          </DialogContent>
          <DialogActions>
            <Button
              sx={{ bgcolor: "#00A19B" }}
              onClick={handleSubmit}
              variant="contained"
              color="primary"
            >
              Submit
            </Button>
          </DialogActions>
        </Dialog>

        {/* Stat Boxes */}
        <Grid container spacing={2} sx={{ mt: 2 }} justifyContent="center">
          <Grid>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">Current Date Range Total AUH</Typography>
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

              {fiaLimit ? (
                <Typography variant="h4">{fiaLimit}</Typography>
              ) : (
                <Typography variant="h4">N/A</Typography>
              )}
            </Paper>
          </Grid>
          <Grid>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">FIA 8 week Date Range</Typography>
              {fiaWindowStart && fiaWindowEnd ? (
                <Typography variant="h6">
                  {`${format(
                    new Date(fiaWindowStart),
                    "MMMM d, yyyy"
                  )} - ${format(new Date(fiaWindowEnd), "MMMM d, yyyy")}`}
                </Typography>
              ) : (
                <Typography variant="h6">N/A</Typography>
              )}
            </Paper>
          </Grid>
        </Grid>
        {/* Chart */}
        {summary?.overall && summary.overall.length > 0 ? (
          <Box sx={{ mt: 4, height: 300 }}>
            <AuhPerTypeChart auhPerType={summary.auh_by_type} />
            {/* Example: show grand_total_auh from first element */}
          </Box>
        ) : (
          <DataUnavailable />
        )}
      </Container>
    </>
  );
};

export default DashboardPage;
