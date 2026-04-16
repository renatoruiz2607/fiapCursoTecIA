args <- commandArgs(trailingOnly = TRUE)

# ============================
# VALIDATE INPUT ARGUMENTS
# ============================

if (length(args) != 5) {
  stop(
    "Usage: Rscript irrigation_model.R <soil_moisture> <ph_value> <active_nutrients> <potassium_ok> <rain_forecast_level>"
  )
}

soil_moisture <- as.numeric(args[1])
ph_value <- as.numeric(args[2])
active_nutrients <- as.integer(args[3])
potassium_ok <- as.integer(args[4])
rain_forecast_level <- as.integer(args[5])

# ============================
# LOAD TRAINING DATA
# ============================

training_data <- read.csv("scripts/irrigation_training_data.csv")

# ============================
# TRAIN LOGISTIC REGRESSION MODEL
# ============================

irrigation_model <- glm(
  should_irrigate ~ soil_moisture + ph_value + active_nutrients + potassium_ok + rain_forecast_level,
  data = training_data,
  family = binomial
)

# ============================
# PREPARE NEW INPUT DATA
# ============================

current_data <- data.frame(
  soil_moisture = soil_moisture,
  ph_value = ph_value,
  active_nutrients = active_nutrients,
  potassium_ok = potassium_ok,
  rain_forecast_level = rain_forecast_level
)

# ============================
# PREDICT IRRIGATION PROBABILITY
# ============================

irrigation_probability <- predict(
  irrigation_model,
  newdata = current_data,
  type = "response"
)

# ============================
# CONVERT PROBABILITY TO DECISION
# ============================

irrigation_decision <- ifelse(irrigation_probability >= 0.5, 1, 0)

# ============================
# OUTPUT RESULT
# ============================

cat("=== IRRIGATION MODEL RESULT ===\n")
cat(sprintf("Soil moisture: %.2f\n", soil_moisture))
cat(sprintf("pH value: %.2f\n", ph_value))
cat(sprintf("Active nutrients: %d\n", active_nutrients))
cat(sprintf("Potassium OK: %d\n", potassium_ok))
cat(sprintf("Rain forecast level: %d\n", rain_forecast_level))
cat("\n")
cat(sprintf("Irrigation probability: %.4f\n", irrigation_probability))
cat(sprintf("Irrigation decision: %d\n", irrigation_decision))