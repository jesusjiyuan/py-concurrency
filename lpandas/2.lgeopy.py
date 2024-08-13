# Import necessary libraries
import geopy
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import folium

# Initialize a Geocoder
geolocator = Nominatim(user_agent="geopy_example")

# Geocode a location (e.g., New York City)
location = geolocator.geocode("Shanghai")

# Print the geocoded location information
print("Location:", location.address)
print("Latitude:", location.latitude)
print("Longitude:", location.longitude)

# Reverse geocode using coordinates
coordinates = (location.latitude, location.longitude)
reverse_location = geolocator.reverse(coordinates)

# Print the reverse geocoded location information
print("Reverse Location:", reverse_location.address)

# Create a map using Folium
map = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)

# Add a marker for the geocoded location
folium.Marker([location.latitude, location.longitude], popup="New York City").add_to(map)

# Save the map to an HTML file for visualization
map.save("map.html")

# Display the map
map
