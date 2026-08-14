import pandas as pd

df = pd.read_excel("tourism_dataset.xlsx")


def get_place(destination):

    result = df[
        df["destination"].str.lower()
        == destination.strip().lower()
    ]

    if result.empty:
        return None

    row = result.iloc[0]

    return {
        "destination": row["destination"],
        "state": row["state"],
        "best_time": row["best_season"],
        "budget": row["avg_budget_per_day"],
        "attractions": row["top_attractions"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "rating": row["rating"],
        "category": row["category"],
        "ideal_duration": row["ideal_duration"],
        "nearest_airport": row["nearest_airport"],
        "nearest_railway_station": row["nearest_railway_station"],
        "famous_food": row["famous_food"]
    }


def get_hotels(city, travel_style):

    hotels = pd.read_csv("hotel_data.csv")

    result = hotels[
        hotels["City"].astype(str).str.lower()
        == city.strip().lower()
    ].copy()

    if result.empty:
        return result

    result["Hotel_Price"] = pd.to_numeric(
        result["Hotel_Price"],
        errors="coerce"
    )

    result["Hotel_Rating"] = pd.to_numeric(
        result["Hotel_Rating"],
        errors="coerce"
    )

    result = result.dropna(
        subset=[
            "Hotel_Price",
            "Hotel_Rating"
        ]
    )

    if travel_style == "Budget":

        result = result.sort_values(
            by=[
                "Hotel_Price",
                "Hotel_Rating"
            ],
            ascending=[
                True,
                False
            ]
        )

    elif travel_style == "Standard":

        result = result.sort_values(
            by=[
                "Hotel_Rating",
                "Hotel_Price"
            ],
            ascending=[
                False,
                True
            ]
        )

    elif travel_style == "Luxury":

        result = result.sort_values(
            by=[
                "Hotel_Price",
                "Hotel_Rating"
            ],
            ascending=[
                False,
                False
            ]
        )

    return result