import pandas as pd
import sys
from geopy.geocoders import Nominatim
from colorama import Fore, Style


def banner():
    print(Fore.BLUE + """
    
 __         ______     ______         __         ______     __   __     ______       
/\ \       /\  __ \   /\__  _\       /\ \       /\  __ \   /\ "-.\ \   /\  ___\      
\ \ \____  \ \  __ \  \/_/\ \/       \ \ \____  \ \ \/\ \  \ \ \-.  \  \ \ \__ \     
 \ \_____\  \ \_\ \_\    \ \_\        \ \_____\  \ \_____\  \ \_\\"\_\  \ \_____\    
  \/_____/   \/_/\/_/     \/_/         \/_____/   \/_____/   \/_/ \/_/   \/_____/    
                                                                                     

    """ + Fore.RESET)

# Read the CSV file into a DataFrame
banner()
csv_location = input("Please Specify Location of CSV File: ")
if not csv_location.endswith(".csv"):
    print(Fore.RED +"Invalid file format. Please enter a filename ending with '.csv'." + Fore.RESET)
    sys.exit()
df = pd.read_csv(csv_location)

# Initialize Nominatim geolocator
geolocator = Nominatim(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3")

# Function to geocode address and return latitude and longitude


def geocode_address(row):
    address = f"{row['Number']} {row['Street']}, {row['PostalCode']}, FL"
    print("Geocoding:", address)  # Debugging statement
    location = geolocator.geocode(address)
    if location:
        print(Fore.GREEN + "Found coordinates:" + Fore.RESET,
              location.latitude, location.longitude)  # Debugging statement
        return location.latitude, location.longitude
    else:
        print(Fore.RED + "Could not find coordinates for:" + Fore.RESET,
              address)  # Debugging statement
        return None, None


# Apply geocoding function to each row in the DataFrame
df['Latitude'], df['Longitude'] = zip(*df.apply(geocode_address, axis=1))

# Drop rows where latitude or longitude is missing
df = df.dropna(subset=['Latitude', 'Longitude'])

# Print the DataFrame with latitude and longitude columns
print(Fore.GREEN + "Data Successfully added to CSV!" + Fore.RESET)

# Write the DataFrame with latitude and longitude to CSV
df.to_csv("output_lat_long_ready.csv", index=False)
