import pandas as pd                                                         # Importing pandas library for data manipulation
from haversine import haversine, Unit                                       # Importing specific functions from the haversine library for distance calculation

def main():
    """
    Main function to execute the script's workflow:
    reading the CSVs, calculating distances, and saving the new data.
    """

    # Attempt to load the data from CSV files
    try:
        # Reading the hotels file, with latitude and longitude columns, using 'ISO-8859-1' encoding to ensure compatibility with a variety of CSV file encodings
        hosts_df = pd.read_csv('hosts.csv', encoding='ISO-8859-1')
        # Reading the landmarks file with the same encoding
        places_df = pd.read_csv('places.csv', encoding='ISO-8859-1')
    except UnicodeDecodeError as e:
        # Handling a potential exception that occurs if there is an encoding conflict
        print(f"An error occurred when reading the CSV files: {e}")
        print("Please ensure your files are correctly encoded.")
        return  # Exiting the function early due to the error

    # Adding new columns to the hotels DataFrame, one for each place, initializing with None (null values)
    for i, place in places_df.iterrows():
        # The column name is composed of a base string and the unique place name
        hosts_df[f'distance_to_{place["place_name"]}'] = None

    # Iterating over each hotel in the DataFrame to calculate distances
    for i, host in hosts_df.iterrows():
        # Retrieving the coordinates of the current hotel
        host_coord = (host['latitude'], host['longitude'])

        # Nested loop to iterate over each landmark for distance calculation
        for j, place in places_df.iterrows():
            # Retrieving the coordinates of the current landmark
            place_coord = (place['latitude'], place['longitude'])
            # Calculating the geographical distance using the haversine formula
            distance = haversine(host_coord, place_coord, unit=Unit.KILOMETERS)

            # Storing the calculated distance in the appropriate column of the hotel's DataFrame
            hosts_df.at[i, f'distance_to_{place["place_name"]}'] = distance

    # Saving the updated DataFrame with the new distance information to a new CSV file
    hosts_df.to_csv('hosts_with_distances.csv', index=False)

    # Console message indicating successful completion of the script
    print("The distances have been calculated and saved to 'hosts_with_distances.csv'.")

# Python best practice for making the script runnable as a standalone application
if __name__ == "__main__":
    main()
