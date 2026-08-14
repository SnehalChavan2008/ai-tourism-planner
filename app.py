import streamlit as st
import pandas as pd
import hashlib
import os

from data import get_place, get_hotels
from weather import get_weather
from ai import generate_itinerary, chat_with_ai
from map_utils import show_map


st.set_page_config(
    page_title="AI Tourism Planner",
    page_icon="🌍",
    layout="wide"
)


st.markdown(
    """
    <style>

    .destination-card {
        border-radius: 20px;
        overflow: hidden;
        margin: 10px 0 25px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.18);
        background: white;
    }

    .destination-title {
        padding: 18px 22px 5px 22px;
        font-size: 30px;
        font-weight: 700;
        margin: 0;
    }

    .destination-subtitle {
        padding: 0 22px 18px 22px;
        font-size: 16px;
        color: #666;
        margin: 0;
    }

    .food-card {
        border-radius: 18px;
        overflow: hidden;
        margin: 10px 0 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        background: white;
    }

    .food-title {
        padding: 14px 18px 5px 18px;
        font-size: 22px;
        font-weight: 700;
    }

    .food-subtitle {
        padding: 0 18px 16px 18px;
        font-size: 15px;
        color: #666;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if "users" not in st.session_state:
    st.session_state["users"] = {}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = ""

if "trip_generated" not in st.session_state:
    st.session_state["trip_generated"] = False

if "place" not in st.session_state:
    st.session_state["place"] = None

if "destination" not in st.session_state:
    st.session_state["destination"] = ""

if "travel_style" not in st.session_state:
    st.session_state["travel_style"] = "Standard"

if "days" not in st.session_state:
    st.session_state["days"] = 3

if "budget" not in st.session_state:
    st.session_state["budget"] = 10000

if "travelers" not in st.session_state:
    st.session_state["travelers"] = 1

if "interests" not in st.session_state:
    st.session_state["interests"] = []

if "itinerary" not in st.session_state:
    st.session_state["itinerary"] = None


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def get_destination_image(destination):

    image_folder = "images"

    if not os.path.exists(image_folder):
        return None

    destination_name = (
        destination.strip().lower()
    )

    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    for extension in image_extensions:

        image_path = os.path.join(
            image_folder,
            destination_name + extension
        )

        if os.path.exists(image_path):
            return image_path

    return None


def get_food_image(destination):

    image_folder = "food_images"

    if not os.path.exists(image_folder):
        return None

    destination_name = (
        destination.strip().lower()
    )

    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    for extension in image_extensions:

        image_path = os.path.join(
            image_folder,
            destination_name + extension
        )

        if os.path.exists(image_path):
            return image_path

    return None


if not st.session_state["logged_in"]:

    st.title("🌍 AI Tourism Planner")

    st.markdown(
        "### Welcome to AI-Powered Travel Planning ✈️"
    )

    st.write("---")

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )

    with login_tab:

        st.subheader(
            "🔐 Login"
        )

        login_username = st.text_input(
            "👤 Username",
            key="login_username"
        )

        login_password = st.text_input(
            "🔑 Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if (
                login_username.strip()
                and login_password
            ):

                username = (
                    login_username.strip()
                )

                password_hash = hash_password(
                    login_password
                )

                if (
                    username
                    in st.session_state["users"]
                    and
                    st.session_state["users"][
                        username
                    ] == password_hash
                ):

                    st.session_state[
                        "logged_in"
                    ] = True

                    st.session_state[
                        "current_user"
                    ] = username

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

            else:

                st.warning(
                    "⚠️ Please enter username and password."
                )

    with register_tab:

        st.subheader(
            "📝 Create New Account"
        )

        register_username = st.text_input(
            "👤 Choose Username",
            key="register_username"
        )

        register_password = st.text_input(
            "🔑 Create Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "🔐 Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "📝 Register",
            use_container_width=True
        ):

            username = (
                register_username.strip()
            )

            if not username:

                st.warning(
                    "⚠️ Please enter a username."
                )

            elif not register_password:

                st.warning(
                    "⚠️ Please enter a password."
                )

            elif (
                register_password
                != confirm_password
            ):

                st.error(
                    "❌ Passwords do not match."
                )

            elif username in st.session_state["users"]:

                st.error(
                    "❌ Username already exists."
                )

            else:

                st.session_state["users"][
                    username
                ] = hash_password(
                    register_password
                )

                st.success(
                    "✅ Registration successful! "
                    "You can now login."
                )

    st.stop()


st.title("🌍 AI Tourism Planner")

st.markdown(
    "### Plan Your Dream Trip with AI ✈️"
)


col1, col2 = st.columns(
    [5, 1]
)

with col1:

    st.write(
        f"👋 Welcome, "
        f"**{st.session_state['current_user']}**"
    )

with col2:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.session_state["current_user"] = ""
        st.session_state["trip_generated"] = False
        st.session_state["place"] = None
        st.session_state["itinerary"] = None

        st.rerun()


st.write("---")


destination = st.text_input(
    "📍 Enter Destination"
)


col1, col2 = st.columns(2)

with col1:

    days = st.number_input(
        "📅 Number of Days",
        min_value=1,
        max_value=30,
        value=3
    )

with col2:

    budget = st.number_input(
        "💰 Budget (₹)",
        min_value=1000,
        value=10000,
        step=1000
    )


travelers = st.number_input(
    "👨‍👩‍👧 Number of Travelers",
    min_value=1,
    value=1
)


travel_style = st.selectbox(
    "✈️ Travel Style",
    [
        "Budget",
        "Standard",
        "Luxury"
    ]
)


interests = st.multiselect(
    "❤️ Select Interests",
    [
        "Adventure",
        "Beach",
        "Nature",
        "Food",
        "History",
        "Wildlife",
        "Shopping",
        "Photography"
    ]
)


if st.button(
    "🚀 Generate Trip Plan"
):

    if not destination.strip():

        st.warning(
            "⚠️ Please enter a destination."
        )

    else:

        st.success(
            "Trip Planning Started!"
        )

        place = get_place(
            destination.strip()
        )

        if place:

            st.session_state["place"] = place

            st.session_state[
                "destination"
            ] = destination.strip()

            st.session_state[
                "travel_style"
            ] = travel_style

            st.session_state[
                "days"
            ] = days

            st.session_state[
                "budget"
            ] = budget

            st.session_state[
                "travelers"
            ] = travelers

            st.session_state[
                "interests"
            ] = interests

            st.session_state[
                "trip_generated"
            ] = True

            st.session_state[
                "itinerary"
            ] = None

        else:

            st.session_state[
                "trip_generated"
            ] = False

            st.error(
                "❌ Destination not found in dataset."
            )


if st.session_state.get(
    "trip_generated",
    False
):

    place = st.session_state[
        "place"
    ]

    current_destination = (
        st.session_state[
            "destination"
        ]
    )

    current_travel_style = (
        st.session_state[
            "travel_style"
        ]
    )

    current_days = (
        st.session_state[
            "days"
        ]
    )

    current_budget = (
        st.session_state[
            "budget"
        ]
    )

    current_travelers = (
        st.session_state[
            "travelers"
        ]
    )

    current_interests = (
        st.session_state[
            "interests"
        ]
    )


    st.success(
        "Destination Found"
    )


    destination_image = (
        get_destination_image(
            current_destination
        )
    )


    if destination_image:

        st.markdown(
            '<div class="destination-card">',
            unsafe_allow_html=True
        )

        st.image(
            destination_image,
            use_container_width=True
        )

        st.markdown(
            f"""
            <div class="destination-title">
                🌍 {current_destination}
            </div>

            <div class="destination-subtitle">
                ✈️ Explore, discover and enjoy your journey
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    st.success(
        f"🌍 Welcome to "
        f"{current_destination}!"
    )


    st.write(
        f"📍 State : {place['state']}"
    )

    st.write(
        f"🌤 Best Time : "
        f"{place['best_time']}"
    )

    st.write(
        f"💰 Average Budget : "
        f"₹{place['budget']}"
    )


    st.markdown("---")


    st.subheader(
        "⭐ Destination Highlights"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "⭐ Rating",
            place["rating"]
        )


    with col2:

        st.metric(
            "🏷️ Category",
            place["category"]
        )


    with col3:

        st.metric(
            "⏱️ Ideal Duration",
            f"{place['ideal_duration']} Days"
        )


    st.subheader(
        "🍽️ Famous Food"
    )


    food_image = (
        get_food_image(
            current_destination
        )
    )


    if food_image:

        col1, col2 = st.columns(
            [1, 2]
        )

        with col1:

            st.markdown(
                '<div class="food-card">',
                unsafe_allow_html=True
            )

            st.image(
                food_image,
                use_container_width=True
            )

            st.markdown(
                f"""
                <div class="food-title">
                    🍛 Local Speciality
                </div>

                <div class="food-subtitle">
                    Famous food of {current_destination}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        with col2:

            st.info(
                f"🍽️ **{place['famous_food']}**"
            )

    else:

        st.info(
            f"🍽️ **{place['famous_food']}**"
        )


    st.markdown("---")


    st.subheader(
        "🏖️ Tourist Attractions"
    )


    attractions = (
        place["attractions"]
        .split("|")
    )


    for attraction in attractions:

        st.success(
            f"📍 {attraction}"
        )


    st.markdown("---")


    st.subheader(
        "🚆✈️ How to Reach"
    )


    railway_station = place.get(
        "nearest_railway_station",
        "Not available"
    )

    airport = place.get(
        "nearest_airport",
        "Not available"
    )


    if pd.isna(
        railway_station
    ):

        railway_station = (
            "Not available"
        )


    if pd.isna(
        airport
    ):

        airport = (
            "Not available"
        )


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            f"🚆 Nearest Railway Station\n\n"
            f"**{railway_station}**"
        )


    with col2:

        st.info(
            f"✈️ Nearest Airport\n\n"
            f"**{airport}**"
        )


    st.markdown("---")


    try:

        weather = get_weather(
            place["latitude"],
            place["longitude"]
        )


        if weather:

            st.subheader(
                "🌤 Live Weather"
            )


            col1, col2, col3 = (
                st.columns(3)
            )


            with col1:

                st.metric(
                    "🌡 Temperature",
                    f"{weather['temperature_2m']} °C"
                )


            with col2:

                st.metric(
                    "💧 Humidity",
                    f"{weather['relative_humidity_2m']} %"
                )


            with col3:

                st.metric(
                    "💨 Wind Speed",
                    f"{weather['wind_speed_10m']} km/h"
                )


    except Exception:

        st.warning(
            "⚠️ Live weather is currently unavailable."
        )


    st.markdown("---")


    st.subheader(
        "📍 Destination Map"
    )


    try:

        show_map(
            place["latitude"],
            place["longitude"]
        )

    except Exception as e:

        st.warning(
            f"Map unavailable: {e}"
        )


    st.markdown("---")


    st.subheader(
        "📌 Destination Information"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "📅 Best Time",
            place["best_time"]
        )


    with col2:

        st.metric(
            "💰 Estimated Budget",
            f"₹{place['budget']}"
        )


    with col3:

        st.metric(
            "📍 State",
            place["state"]
        )


    st.markdown("---")


    st.subheader(
        "🤖 AI Trip Plan"
    )


    if st.session_state[
        "itinerary"
    ] is None:

        try:

            with st.spinner(
                "Generating your personalized itinerary..."
            ):

                itinerary = generate_itinerary(
                    current_destination,
                    current_days,
                    current_budget,
                    current_travelers,
                    current_interests,
                    place
                )


            st.session_state[
                "itinerary"
            ] = itinerary


        except Exception as e:

            if (
                "429" in str(e)
                or
                "ResourceExhausted"
                in str(e)
                or
                "quota"
                in str(e).lower()
            ):

                st.warning(
                    "⚠️ Gemini API quota exhausted. "
                    "AI Trip Plan is temporarily unavailable."
                )

            else:

                st.error(
                    f"AI Error: {e}"
                )


    if st.session_state[
        "itinerary"
    ]:

        st.markdown(
            st.session_state[
                "itinerary"
            ]
        )


    st.markdown("---")


    st.subheader(
        "💰 Budget Breakdown"
    )


    total_budget = current_budget

    hotel_budget = (
        total_budget * 0.35
    )

    food_budget = (
        total_budget * 0.20
    )

    travel_budget = (
        total_budget * 0.20
    )

    activities_budget = (
        total_budget * 0.15
    )

    other_budget = (
        total_budget * 0.10
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "🏨 Hotel",
            f"₹{hotel_budget:.0f}"
        )

        st.metric(
            "🍽️ Food",
            f"₹{food_budget:.0f}"
        )

        st.metric(
            "🚕 Local Travel",
            f"₹{travel_budget:.0f}"
        )


    with col2:

        st.metric(
            "🎟️ Activities",
            f"₹{activities_budget:.0f}"
        )

        st.metric(
            "🛍️ Other Expenses",
            f"₹{other_budget:.0f}"
        )

        st.metric(
            "💰 Total Budget",
            f"₹{total_budget:.0f}"
        )


    st.markdown("---")


    st.subheader(
        "🏨 Recommended Hotels"
    )


    st.subheader(
        "🔎 Filter Hotels"
    )


    try:

        hotels = get_hotels(
            current_destination,
            current_travel_style
        )


        if (
            hotels is not None
            and not hotels.empty
        ):

            hotels[
                "Hotel_Rating"
            ] = pd.to_numeric(
                hotels[
                    "Hotel_Rating"
                ],
                errors="coerce"
            )


            hotels[
                "Hotel_Price"
            ] = pd.to_numeric(
                hotels[
                    "Hotel_Price"
                ],
                errors="coerce"
            )


            hotels = hotels.dropna(
                subset=[
                    "Hotel_Rating",
                    "Hotel_Price"
                ]
            )


            with st.form(
                "hotel_filter_form"
            ):

                min_rating = st.slider(
                    "⭐ Minimum Rating",
                    min_value=1.0,
                    max_value=5.0,
                    value=3.0,
                    step=0.5
                )


                max_price = st.number_input(
                    "💰 Maximum Hotel Price",
                    min_value=500,
                    value=5000,
                    step=500
                )


                apply_filter = (
                    st.form_submit_button(
                        "🔎 Apply Filters"
                    )
                )


            if apply_filter:

                filtered_hotels = hotels[
                    (
                        hotels[
                            "Hotel_Rating"
                        ] >= min_rating
                    )
                    &
                    (
                        hotels[
                            "Hotel_Price"
                        ] <= max_price
                    )
                ]

            else:

                filtered_hotels = hotels


            if not filtered_hotels.empty:

                if apply_filter:

                    st.success(
                        f"✨ {len(filtered_hotels)} "
                        f"hotel(s) found"
                    )


                for _, hotel in (
                    filtered_hotels
                    .head(3)
                    .iterrows()
                ):

                    st.markdown("---")


                    st.subheader(
                        f"🏨 "
                        f"{hotel['Hotel_Name']}"
                    )


                    col1, col2, col3 = (
                        st.columns(3)
                    )


                    with col1:

                        st.metric(
                            "⭐ Rating",
                            str(
                                hotel[
                                    "Hotel_Rating"
                                ]
                            )
                        )


                    with col2:

                        st.metric(
                            "💰 Price",
                            f"₹{hotel['Hotel_Price']}"
                        )


                    with col3:

                        st.metric(
                            "📍 City",
                            str(
                                hotel["City"]
                            )
                        )


                    features = []


                    for i in range(1, 10):

                        column_name = (
                            f"Feature_{i}"
                        )


                        if (
                            column_name
                            in hotel.index
                        ):

                            value = hotel[
                                column_name
                            ]


                            if pd.notna(
                                value
                            ):

                                value = str(
                                    value
                                ).strip()


                                if value:

                                    features.append(
                                        value
                                    )


                    if features:

                        st.write(
                            "✨ Features"
                        )


                        for feature in features:

                            st.write(
                                f"• {feature}"
                            )


            else:

                st.warning(
                    "😕 No hotels match your "
                    "selected filters."
                )


        else:

            st.info(
                "No hotels found for this destination."
            )


    except Exception as e:

        st.error(
            f"Hotel data error: {e}"
        )


    st.markdown("---")


    st.subheader(
        "🎒 Smart Packing List"
    )


    packing_items = []


    packing_items.extend(
        [
            "🪪 ID / Travel Documents",
            "📱 Mobile Phone",
            "🔌 Phone Charger",
            "🔋 Power Bank",
            "🧴 Toiletries",
            "💊 Basic Medicines",
            "🧴 Sunscreen",
            "🕶️ Sunglasses",
            "💧 Water Bottle"
        ]
    )


    if current_days >= 5:

        packing_items.extend(
            [
                "👕 Extra Clothes",
                "🧦 Extra Socks",
                "👟 Comfortable Shoes"
            ]
        )

    else:

        packing_items.extend(
            [
                "👕 Comfortable Clothes",
                "👟 Comfortable Shoes"
            ]
        )


    if "Beach" in current_interests:

        packing_items.extend(
            [
                "🩴 Sandals",
                "🩱 Swimwear",
                "🏖️ Beach Towel"
            ]
        )


    if "Adventure" in current_interests:

        packing_items.extend(
            [
                "🎒 Small Backpack",
                "🥾 Trekking Shoes",
                "🔦 Flashlight"
            ]
        )


    if "Photography" in current_interests:

        packing_items.extend(
            [
                "📷 Camera",
                "🔋 Extra Battery",
                "💾 Extra Storage"
            ]
        )


    if "Wildlife" in current_interests:

        packing_items.extend(
            [
                "🔭 Binoculars",
                "📷 Camera",
                "🦟 Mosquito Repellent"
            ]
        )


    if "Shopping" in current_interests:

        packing_items.extend(
            [
                "👜 Extra Bag",
                "💳 Extra Payment Method"
            ]
        )


    if "Nature" in current_interests:

        packing_items.extend(
            [
                "🥾 Comfortable Walking Shoes",
                "🧢 Cap / Hat",
                "🦟 Mosquito Repellent"
            ]
        )


    if "History" in current_interests:

        packing_items.extend(
            [
                "👟 Comfortable Walking Shoes",
                "📷 Camera"
            ]
        )


    if "Food" in current_interests:

        packing_items.extend(
            [
                "💧 Water Bottle",
                "🧴 Hand Sanitizer"
            ]
        )


    packing_items = list(
        dict.fromkeys(
            packing_items
        )
    )


    st.write(
        f"🎯 Recommended items for your "
        f"{current_days}-day trip:"
    )


    col1, col2 = st.columns(2)


    half = (
        len(packing_items) + 1
    ) // 2


    with col1:

        for index, item in enumerate(
            packing_items[:half]
        ):

            st.checkbox(
                item,
                key=f"packing_left_{index}"
            )


    with col2:

        for index, item in enumerate(
            packing_items[half:]
        ):

            st.checkbox(
                item,
                key=f"packing_right_{index}"
            )


    st.markdown("---")


    st.subheader(
        "🤖 AI Travel Chatbot"
    )


    question = st.chat_input(
        f"Ask me anything about "
        f"{current_destination}..."
    )


    if question:

        st.chat_message(
            "user"
        ).write(
            question
        )


        with st.chat_message(
            "assistant"
        ):

            try:

                with st.spinner(
                    "Thinking..."
                ):

                    answer = chat_with_ai(
                        question,
                        current_destination
                    )


                st.write(
                    answer
                )


            except Exception as e:

                if (
                    "429" in str(e)
                    or
                    "ResourceExhausted"
                    in str(e)
                    or
                    "quota"
                    in str(e).lower()
                ):

                    st.warning(
                        "⚠️ Gemini API quota exhausted. "
                        "Chatbot is temporarily unavailable."
                    )

                else:

                    st.error(
                        f"Chatbot Error: {e}"
                    )


st.markdown("---")


st.write(
    "### 🧳 Your Details"
)


st.write(
    f"📍 Destination : "
    f"{destination}"
)


st.write(
    f"📅 Days : "
    f"{days}"
)


st.write(
    f"💰 Budget : "
    f"₹{budget}"
)


st.write(
    f"👨‍👩‍👧 Travelers : "
    f"{travelers}"
)


st.write(
    f"✈️ Style : "
    f"{travel_style}"
)


st.write(
    f"❤️ Interests : "
    f"{', '.join(interests)}"
)


st.markdown("---")


st.caption(
    "Made with ❤️ using Streamlit + Gemini AI"
)