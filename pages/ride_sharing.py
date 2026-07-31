# -*- coding: utf-8 -*-

import streamlit as st
import folium
import requests
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from datetime import date
from database import get_connection


st.set_page_config(
    page_title="Ride Sharing",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Campus Ride Sharing")
st.caption("Offer or Find Rides Within Campus")

# LOGIN CHECK
if "logged_in" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")

geolocator = Nominatim(user_agent="campus_connect")


# DELETE FUNCTION
def delete_ride(ride_id, user_id):
    """Delete a ride only if user owns it"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id FROM rides WHERE ride_id = %s",
            (ride_id,)
        )
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            cursor.execute(
                "DELETE FROM rides WHERE ride_id = %s AND user_id = %s",
                (ride_id, user_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False
    except Exception as e:
        st.error(f"Error deleting ride: {e}")
        return False

# SESSION
defaults = {
    "pickup_lat": 23.1815,
    "pickup_lng": 79.9864,
    "destination_lat": 23.1815,
    "destination_lng": 79.9864,
    "pickup_address": "",
    "destination_address": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# FUNCTIONS
def search_place(place):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": place,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "CampusConnect"
        }
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        data = response.json()
        if len(data) > 0:
            return (
                float(data[0]["lat"]),
                float(data[0]["lon"])
            )
    except:
        pass
    return None, None

# OFFER RIDE
st.subheader("🚗 Offer a Ride")

source = st.text_input(
    "📍 Pickup Location",
    value=st.session_state.pickup_address
)

col1, col2 = st.columns([4,1])

with col2:
    if st.button("🔍 Search Pickup"):
        lat, lng = search_place(source)
        if lat:
            st.session_state.pickup_lat = lat
            st.session_state.pickup_lng = lng
            st.session_state.pickup_address = source
            st.success("Pickup Found")
            st.rerun()
        else:
            st.error("Location Not Found")

pickup_map = folium.Map(
    location=[
        st.session_state.pickup_lat,
        st.session_state.pickup_lng
    ],
    zoom_start=15
)

folium.Marker(
    [
        st.session_state.pickup_lat,
        st.session_state.pickup_lng
    ],
    tooltip="Pickup",
    icon=folium.Icon(color="green")
).add_to(pickup_map)

st_folium(
    pickup_map,
    width=750,
    height=350,
    key="pickup_map"
)

st.divider()

destination = st.text_input(
    "🎯 Destination",
    value=st.session_state.destination_address
)

col1, col2 = st.columns([4,1])

with col2:
    if st.button("🔍 Search Destination"):
        lat, lng = search_place(destination)
        if lat:
            st.session_state.destination_lat = lat
            st.session_state.destination_lng = lng
            st.session_state.destination_address = destination
            st.success("Destination Found")
            st.rerun()
        else:
            st.error("Location Not Found")

destination_map = folium.Map(
    location=[
        st.session_state.destination_lat,
        st.session_state.destination_lng
    ],
    zoom_start=15
)

folium.Marker(
    [
        st.session_state.destination_lat,
        st.session_state.destination_lng
    ],
    tooltip="Destination",
    icon=folium.Icon(color="red")
).add_to(destination_map)

st_folium(
    destination_map,
    width=750,
    height=350,
    key="destination_map"
)

# RIDE DETAILS
ride_date = st.date_input(
    "📅 Travel Date",
    value=date.today()
)

ride_time = st.time_input(
    "🕒 Travel Time"
)

available_seats = st.number_input(
    "💺 Available Seats",
    min_value=1,
    max_value=10,
    value=1
)

vehicle = st.selectbox(
    "🚘 Vehicle",
    [
        "Bike",
        "Scooter",
        "Car",
        "Auto"
    ]
)

contact = st.text_input(
    "📞 Contact Number"
)

# ROUTE PREVIEW
st.subheader("🗺 Route Preview")

route_map = folium.Map(
    location=[
        (
            st.session_state.pickup_lat +
            st.session_state.destination_lat
        ) / 2,
        (
            st.session_state.pickup_lng +
            st.session_state.destination_lng
        ) / 2
    ],
    zoom_start=13
)

folium.Marker(
    [
        st.session_state.pickup_lat,
        st.session_state.pickup_lng
    ],
    tooltip="Pickup",
    icon=folium.Icon(color="green")
).add_to(route_map)

folium.Marker(
    [
        st.session_state.destination_lat,
        st.session_state.destination_lng
    ],
    tooltip="Destination",
    icon=folium.Icon(color="red")
).add_to(route_map)

folium.PolyLine(
    [
        [
            st.session_state.pickup_lat,
            st.session_state.pickup_lng
        ],
        [
            st.session_state.destination_lat,
            st.session_state.destination_lng
        ]
    ],
    color="blue",
    weight=5,
    opacity=0.8
).add_to(route_map)

st_folium(
    route_map,
    width=900,
    height=450,
    key="route_preview"
)

st.divider()

# OFFER RIDE
if st.button("🚗 Offer Ride", use_container_width=True):
    if source.strip() == "":
        st.error("Enter Pickup Location")
    elif destination.strip() == "":
        st.error("Enter Destination")
    elif contact.strip() == "":
        st.error("Enter Contact Number")
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO rides
            (user_id, source, destination, ride_date, ride_time, available_seats,
             vehicle, contact, source_lat, source_lng, destination_lat, destination_lng)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state["user_id"],
                source,
                destination,
                ride_date,
                ride_time,
                available_seats,
                vehicle,
                contact,
                st.session_state.pickup_lat,
                st.session_state.pickup_lng,
                st.session_state.destination_lat,
                st.session_state.destination_lng
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Ride Posted Successfully")
        st.balloons()
        st.rerun()

st.divider()

# SEARCH RIDES WITH DELETE BUTTON

st.header("🚗 Available Rides")

search = st.text_input(
    "🔍 Search Ride",
    placeholder="Search by Pickup, Destination or Vehicle"
)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute(
    """
    SELECT
        r.*,
        u.full_name,
        u.user_id as owner_id
    FROM rides r
    LEFT JOIN users u
    ON r.user_id = u.user_id
    WHERE
        r.source LIKE %s
        OR r.destination LIKE %s
        OR r.vehicle LIKE %s
    ORDER BY r.created_at DESC
    """,
    (
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
    )
)

rides = cursor.fetchall()
cursor.close()
conn.close()

if len(rides)==0:
    st.info("No Ride Available")
else:
    for ride in rides:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.subheader(f"📍 {ride['source']} ➜ {ride['destination']}")
                st.write("👤 Driver :", ride["full_name"])
                st.write("🚘 Vehicle :", ride["vehicle"])
                st.write("📅 Date :", ride["ride_date"])
                st.write("🕒 Time :", ride["ride_time"])
                st.write("💺 Seats :", ride["available_seats"])
                st.write("📞 Contact :", ride["contact"])
                st.write("📌 Status :", ride["status"])

            with col2:
                m = folium.Map(
                    location=[
                        ride["source_lat"],
                        ride["source_lng"]
                    ],
                    zoom_start=12
                )
                folium.Marker(
                    [
                        ride["source_lat"],
                        ride["source_lng"]
                    ],
                    tooltip="Pickup",
                    icon=folium.Icon(color="green")
                ).add_to(m)
                folium.Marker(
                    [
                        ride["destination_lat"],
                        ride["destination_lng"]
                    ],
                    tooltip="Destination",
                    icon=folium.Icon(color="red")
                ).add_to(m)
                folium.PolyLine(
                    [
                        [
                            ride["source_lat"],
                            ride["source_lng"]
                        ],
                        [
                            ride["destination_lat"],
                            ride["destination_lng"]
                        ]
                    ],
                    color="blue",
                    weight=5
                ).add_to(m)
                st_folium(
                    m,
                    width=350,
                    height=200,
                    key=f"ride_{ride['ride_id']}"
                )
                google_route = (
                    f"https://www.google.com/maps/dir/"
                    f"{ride['source_lat']},{ride['source_lng']}/"
                    f"{ride['destination_lat']},{ride['destination_lng']}"
                )
                st.link_button(
                    "🗺 Open Route",
                    google_route,
                    use_container_width=True
                )

            with col3:
                
                # DELETE BUTTON 
        
                if st.session_state.get('user_id') == ride['user_id']:
                    st.warning("⚠️ You are the owner")
                    
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_ride_{ride['ride_id']}",
                        use_container_width=True
                    ):
                        if delete_ride(ride['ride_id'], st.session_state['user_id']):
                            st.success("✅ Ride deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete ride")
                else:
                    st.info("🔒 Ride by other user")

st.divider()


# NAVIGATION
col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

# RIDE SUMMARY
st.divider()

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM rides WHERE status='Available'")
available = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM rides")
total = cursor.fetchone()[0]

cursor.close()
conn.close()

c1,c2 = st.columns(2)

with c1:
    st.metric("🚗 Available Rides", available)

with c2:
    st.metric("📦 Total Posted Rides", total)

# SAFETY TIPS
st.divider()

st.info(
"""
### 🛡 Ride Safety Tips

✅ Verify driver's identity before starting.
✅ Share trip details with friends.
✅ Wear helmet while riding bike.
✅ Do not share OTP or personal passwords.
✅ Meet only at safe public places.
✅ Follow college transport guidelines.
✅ Save emergency contacts.
"""
)

# EMERGENCY CONTACTS
st.subheader("☎ Emergency Contacts")

col1,col2,col3 = st.columns(3)

with col1:
    st.success("""
Campus Security
📞 100
""")

with col2:
    st.warning("""
College Help Desk
📞 0761-XXXXXXX
""")

with col3:
    st.error("""
Ambulance
📞 108
""")

st.divider()
st.caption("🚗 CampusConnect | Ride Sharing")