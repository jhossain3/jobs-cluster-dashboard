module.exports = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"],
  transformIgnorePatterns: [
    "node_modules/(?!(date-fns|@mui/x-date-pickers|@mui/material)/)",
  ],
};
