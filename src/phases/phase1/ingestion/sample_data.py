from __future__ import annotations

# Minimal fallback sample rows for local smoke testing when
# Hugging Face access is unavailable or optional dependencies are missing.
SAMPLE_ROWS: list[dict[str, object]] = [
    {
        "Restaurant Name": "Spice Route",
        "City": "Delhi",
        "Cuisines": "North Indian, Mughlai",
        "Average Cost for two": "900",
        "Aggregate rating": "4.2/5",
        "Votes": "1240",
    },
    {
        "Restaurant Name": "Urban Wok",
        "City": "Bangalore",
        "Cuisines": "Chinese, Thai",
        "Average Cost for two": "650",
        "Aggregate rating": "4.0",
        "Votes": "530",
    },
    {
        "Restaurant Name": "Bella Pasta",
        "City": "Pune",
        "Cuisines": "Italian",
        "Average Cost for two": "1400",
        "Aggregate rating": "4.5",
        "Votes": "810",
    },
]

