"""
Compute the distance from several Airbnbs to different landmarks on Mexico City.
    
All the codes were developed by:
    Dr. Gerardo Tinoco Guerrero                             gerardo.tinoco@umich.mx
    Dr. José Alberto Guzmán Torres                          jose.alberto.guzman@umich.mx
    Dr. Narciso Salvador Tinoco Guerrero                    narciso.tinoco@umich.mx
    Universidad Michoacana de San Nicolás de Hidalgo
 
With the funding of:
    National Council of Humanities, Sciences and Technologies, CONAHCyT (Consejo Nacional de Humanidades, Ciencias y Tecnologías, CONAHCyT). México.
    Coordination of Scientific Research, CIC-UMSNH (Coordinación de la Investigación Científica de la Universidad Michoacana de San Nicolás de Hidalgo, CIC-UMSNH). México
    Aula CIMNE-Morelia. México
 
Date:
    October, 2023.

Last Modification:
    October, 2023.
"""

# Library importation
import pandas as pd                                                         # Importing pandas library for data manipulation
from haversine import haversine, Unit                                       # Importing specific functions from the haversine library for distance calculation

# Main function "Distances"
def Distances():
    '''
    In this main function two different files are read. The first "hosts.csv" contains the information of all the airbnbs that you want to study,
    while the second "places.csv" contains the places of interest in the city that you want to study.

    Requirements:
        hosts.csv                   csv-File        File with all the information of the airbnbs to be studied.
        places.csv                  csv-File        File with all the name, latitude, and longitude for the landmarks.
        
    Output:
        hosts_with_distances.csv    csv-File        The original hosts.csv file with added columns containing the distances to all the landmarks.
    '''

    # Attempt to load the data from CSV files
    try:
        # Reading the hotels file, with latitude and longitude columns, using 'ISO-8859-1' encoding to ensure compatibility with a variety of CSV file encodings.
        hosts_df = pd.read_csv('hosts.csv', encoding='ISO-8859-1')
        # Reading the landmarks file with the same encoding
        places_df = pd.read_csv('places.csv', encoding='ISO-8859-1')
    except UnicodeDecodeError as e:
        # Handling a potential exception that occurs if there is an encoding conflict.
        print(f"An error occurred when reading the CSV files: {e}")
        print("Please ensure your files are correctly encoded.")
        return  # Exiting the function early due to the error.

    # Adding new columns to the hotels DataFrame, one for each place, initializing with None.
    for i, place in places_df.iterrows():
        # The column name is composed of a base string and the unique place name.
        hosts_df[f'd_t_{place["place_name"]}'] = None

    # Iterating over each airbnb in the DataFrame to calculate distances.
    for i, host in hosts_df.iterrows():
        # Retrieving the coordinates of the current airbnb.
        host_coord = (host['latitude'], host['longitude'])

        # Nested loop to iterate over each landmark for distance calculation.
        for j, place in places_df.iterrows():
            # Retrieving the coordinates of the current landmark.
            place_coord = (place['latitude'], place['longitude'])
            # Calculating the geographical distance using the haversine formula.
            distance = haversine(host_coord, place_coord, unit=Unit.KILOMETERS)

            # Storing the calculated distance in the appropriate column of the airbnb's DataFrame.
            hosts_df.at[i, f'd_t_{place["place_name"]}'] = distance

    # Saving the updated DataFrame with the new distance information to a new CSV file.
    hosts_df.to_csv('hosts_with_distances.csv', index=False)

    # Console message indicating successful completion of the script.
    print("The distances have been calculated and saved to 'hosts_with_distances.csv'.")

# Tun the script as a standalone application
if __name__ == "__main__":
    Distances()