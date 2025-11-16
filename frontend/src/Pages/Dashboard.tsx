import React, { useState } from "react";
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
  DialogTitle,
  DialogContent,
} from "@mui/material";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import AuhPerTypeChart from "./AuhPerType";
// Chart data
// const chartData = [
//   { name: "postpro", value: 0 },
//   { name: "mesh", value: 0 },
//   { name: "solve", value: 3000 },
// ];

const DashboardPage = () => {
  const [open, setOpen] = useState(false);
  const [startDate, setStartDate] = useState<Date | null>(new Date());
  const [endDate, setEndDate] = useState<Date | null>(
    new Date(new Date().setDate(new Date().getDate() + 56)) // 8 weeks later
  );

  return (
    <>
      {/* Header */}
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: "center" }} >
          <Typography  align="center" variant="h6">Mercedes AMG Petronas Cluster Jobs Tracker</Typography>
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
        </Dialog>

        {/* Stat Boxes */}
        <Grid container spacing={2} sx={{ mt: 2 }} justifyContent="center">
          <Grid >
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">Manual Value</Typography>
              <Typography variant="h4">3000</Typography>
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
        <Box sx={{ mt: 4, height: 300 }}>
          <AuhPerTypeChart />
        </Box>
      </Container>
    </>
  );
};

export default DashboardPage;
