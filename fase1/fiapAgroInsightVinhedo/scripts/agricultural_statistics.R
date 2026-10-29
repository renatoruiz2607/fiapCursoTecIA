file_path <- "data/agricultural_data.csv"

agricultural_data <- read.csv(file_path, stringsAsFactors = FALSE)

if (nrow(agricultural_data) == 0) {
  cat("No data found in the CSV file.\n")
} else {
  area_mean <- mean(agricultural_data$area, na.rm = TRUE)
  area_sd <- sd(agricultural_data$area, na.rm = TRUE)

  total_input_mean <- mean(agricultural_data$total_input, na.rm = TRUE)
  total_input_sd <- sd(agricultural_data$total_input, na.rm = TRUE)

  grape_data <- agricultural_data[agricultural_data$crop_type == "grape", ]
  corn_data <- agricultural_data[agricultural_data$crop_type == "corn", ]

  grape_area_mean <- mean(grape_data$area, na.rm = TRUE)
  corn_area_mean <- mean(corn_data$area, na.rm = TRUE)

  grape_input_mean <- mean(grape_data$total_input, na.rm = TRUE)
  corn_input_mean <- mean(corn_data$total_input, na.rm = TRUE)

  cat("=== Agricultural Statistics ===\n")
  cat("General area mean:", area_mean, "\n")
  cat("General area standard deviation:", area_sd, "\n")
  cat("General total input mean:", total_input_mean, "\n")
  cat("General total input standard deviation:", total_input_sd, "\n\n")

  cat("=== Statistics by Crop Type ===\n")
  cat("Grape area mean:", grape_area_mean, "\n")
  cat("Corn area mean:", corn_area_mean, "\n")
  cat("Grape total input mean:", grape_input_mean, "\n")
  cat("Corn total input mean:", corn_input_mean, "\n")
}