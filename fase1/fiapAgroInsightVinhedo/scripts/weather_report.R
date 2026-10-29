library(jsonlite)

city_name <- "Vinhedo"

geocoding_url <- paste0(
  "https://geocoding-api.open-meteo.com/v1/search?name=",
  URLencode(city_name),
  "&count=1&language=en&format=json"
)

geocoding_data <- fromJSON(geocoding_url)

if (is.null(geocoding_data$results) || length(geocoding_data$results) == 0) {
  cat("City not found.\n")
} else {
  latitude <- geocoding_data$results$latitude[1]
  longitude <- geocoding_data$results$longitude[1]
  location_name <- geocoding_data$results$name[1]
  country_name <- geocoding_data$results$country[1]

  weather_url <- paste0(
    "https://api.open-meteo.com/v1/forecast?",
    "latitude=", latitude,
    "&longitude=", longitude,
    "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
    "&timezone=auto"
  )

  weather_data <- fromJSON(weather_url)

  cat("Location:", location_name, "-", country_name, "\n")
  cat("Temperature:", weather_data$current$temperature_2m, "°C\n")
  cat("Relative humidity:", weather_data$current$relative_humidity_2m, "%\n")
  cat("Precipitation:", weather_data$current$precipitation, "mm\n")
  cat("Wind speed:", weather_data$current$wind_speed_10m, "km/h\n")
}