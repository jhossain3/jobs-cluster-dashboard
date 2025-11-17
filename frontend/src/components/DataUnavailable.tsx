import React from "react";
import { Paper, Typography, Box } from "@mui/material";

const DataUnavailable = () => {
  return (
    <Paper elevation={2} sx={{ p: 3, textAlign: "center" }}>
      <Box>
        <Typography variant="h6" color="textSecondary">
          No data available
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Please adjust your date range or try again later.
        </Typography>
      </Box>
    </Paper>
  );
};
export default DataUnavailable;
