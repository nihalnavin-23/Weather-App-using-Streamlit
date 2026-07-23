import streamlit as st
import requests

# ============================================
# YOUR API KEY IS HERE
# ============================================
API_KEY = "3b0b2ea08ae26d7fa2b6e4be9eb9e8a7"
# ============================================

# Page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# Title
st.title("🌤️ Weather App")
st.markdown("---")

# City input
city = st.text_input("Enter City Name", value="New York")

# Function to get weather
def get_weather(city):
    url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return {"error": {"info": f"Connection error: {str(e)}"}}

# Get weather button
if st.button("🌤️ Get Weather", type="primary"):
    if not city:
        st.warning("⚠️ Please enter a city name")
    else:
        with st.spinner(f"Fetching weather for {city}..."):
            data = get_weather(city)
            
            # Check for errors
            if "error" in data:
                st.error(f"❌ {data['error']['info']}")
                
                # Helpful tips
                st.info("💡 Tips:")
                st.info("• Make sure your API key is valid")
                st.info("• Check if city name is spelled correctly")
                st.info("• Free tier allows 1000 requests/month")
            else:
                # Extract data
                current = data["current"]
                location = data["location"]
                
                # Display weather
                st.success(f"✅ Weather data for {city} fetched successfully!")
                st.markdown("---")
                
                # Weather icon and description
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if current.get("weather_icons"):
                        st.image(current["weather_icons"][0], width=150)
                    if current.get("weather_descriptions"):
                        st.markdown(f"### {current['weather_descriptions'][0]}")
                
                st.markdown("---")
                
                # Weather metrics in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "🌡️ Temperature",
                        f"{current['temperature']}°C"
                    )
                    st.metric(
                        "🌡️ Feels Like",
                        f"{current['feelslike']}°C"
                    )
                
                with col2:
                    st.metric(
                        "💧 Humidity",
                        f"{current['humidity']}%"
                    )
                    st.metric(
                        "☁️ Cloud Cover",
                        f"{current['cloudcover']}%"
                    )
                
                with col3:
                    st.metric(
                        "💨 Wind Speed",
                        f"{current['wind_speed']} km/h"
                    )
                    st.metric(
                        "👁️ Visibility",
                        f"{current['visibility']} km"
                    )
                
                st.markdown("---")
                
                # Location details
                st.subheader("📍 Location Details")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**City:** {location['name']}")
                    st.write(f"**Country:** {location['country']}")
                    st.write(f"**Region:** {location.get('region', 'N/A')}")
                
                with col2:
                    st.write(f"**Latitude:** {location.get('lat', 'N/A')}")
                    st.write(f"**Longitude:** {location.get('lon', 'N/A')}")
                    if "localtime" in location:
                        st.write(f"**Local Time:** {location['localtime']}")
                
                # Raw data expander
                with st.expander("🔍 View Raw API Response"):
                    st.json(data)

# Footer
st.markdown("---")
st.caption("Powered by Weather Stack API | Get free API key at weatherstack.com")