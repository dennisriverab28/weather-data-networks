# Data Files

The following data files are required to run the client but are excluded from this repository due to size:

| File | Size | Description |
|------|------|-------------|
| `Weather_data.csv` | ~37 MB | Source weather station dataset (input to client) |
| `output.csv` | ~4 MB | Server output — parsed records written by the server |

Place `Weather_data.csv` in the project root (same directory as `client_side.py`) before running.

## CSV Format

The weather data CSV has at minimum these columns (0-indexed):
- Column 0: Station ID
- Column 1: Date
- Column 3: Temperature (Celsius)
- Column 8: Sky Condition
