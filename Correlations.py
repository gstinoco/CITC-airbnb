"""
Compute the distance from several Airbnbs to different landmarks on Mexico City, and compute the correlations between distances and different variables on hosts.
    
All the codes were developed by:
    Dr. Gerardo Tinoco Guerrero                             gerardo.tinoco@umich.mx
    Dr. José Alberto Guzmán Torres                          jose.alberto.guzman@umich.mx
    Dr. Narciso Salvador Tinoco Guerrero                    narciso.tinoco@umich.mx
    Universidad Michoacana de San Nicolás de Hidalgo
 
With the funding of:
    National Council of Humanities, Sciences and Technologies, CONAHCyT (Consejo Nacional de Humanidades, Ciencias y Tecnologías, CONAHCyT). México.
    Aula CIMNE-Morelia. México
 
Date:
    October, 2023.

Last Modification:
    February, 2024.
"""

# Library importation
from haversine import haversine, Unit                                       # Importing specific functions from the haversine library for distance calculation
import tarfile                                                              # Importing tarfile to be able to compress the results.
import pandas as pd                                                         # The library pandas will help with all the data analyses.
import seaborn as sns                                                       # This library contains colors for the plots.
import matplotlib.pyplot as plt                                             # matplotlib let us plot the results.

# Main function "Distances"
def Distances(hosts = 'Information/hosts.csv', places = 'Information/places.csv', result = 'Results/hosts_with_distances.csv'):
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
        hosts_df = pd.read_csv(hosts, encoding='ISO-8859-1')
        # Reading the landmarks file with the same encoding
        places_df = pd.read_csv(places, encoding='ISO-8859-1')
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

    # Clean the information to keep only the information of interest.
    columns_of_interest = ["id", "host_id", "host_url", "host_name", "host_is_superhost", "host_listings_count",
                            "host_total_listings_count", "d_t_museo_nacional_de_antropologia", "d_t_castillo_de_chapultepec",
                            "d_t_palacio_de_bellas_artes", "d_t_basilica_de_la_virgen_de_guadalupe", "d_t_museo_frida_kahlo",
                            "d_t_museo_soumaya", "d_t_museo_del_templo_mayor", "d_t_zocalo_(plaza_de_la_constitucion)",
                            "d_t_catedral_metropolitana", "d_t_palacio_nacional", "d_t_palacio_postal", "d_t_museo_de_arte_popular",
                            "d_t_mercado_de_artesanias_de_la_ciudadela", "d_t_museo_memoria_y_tolerancia", "d_t_arena_mexico",
                            "d_t_monumento_a_la_revolucion", "d_t_museo_diego_rivera", "d_t_museo_nacional_de_arte",
                            "d_t_museo_casa_leon_trotsky", "d_t_cineteca_nacional", "d_t_museo_franz_mayer",
                            "d_t_antiguo_colegio_de_san_ildefonso", "d_t_museo_del_tiempo_tlalpan", "d_t_monumento_a_la_independencia_(el_angel)",
                            "d_t_sagrario_metropolitano", "d_t_museo_de_arte_moderno", "d_t_museo_universitario_arte_contemporaneo_(muac)",
                            "d_t_plaza_de_las_tres_culturas", "d_t_monumento_a_los_ninos_heroes", "d_t_zona_arqueologica_tlatelolco",
                            "d_t_museo_jumex", "d_t_museo_tamayo", "d_t_parroquia_san_juan_bautista", "d_t_museo_nacional_de_san_carlos",
                            "d_t_palacio_de_mineria", "d_t_mercado_medellin"]
    
    filtered_data = hosts_df[columns_of_interest]
    filtered_data = filtered_data.copy()
    filtered_data.loc[:, 'host_is_superhost'] = filtered_data['host_is_superhost'].map({'f': 0, 't': 1})
    filtered_data = filtered_data.dropna()

    # Saving the updated DataFrame with the new distance information to a new CSV file.
    filtered_data.to_csv(result, index=False)

    # Console message indicating successful completion of the script.
    print('The distances have been calculated and saved to', result)
    make_tarfile(result+'.tar.gz',result)
    print('The file was compressed and saved to', result+'.tar.gz')

def make_tarfile(output_filename, source_file):
    '''
    This function is defined to compress a file in .tar.gz format

    Requirements:
        output_filename             String          Name of the output file.
        source_file                 File            File to be compressed.
        
    Output:
        output_filename             .tar.gz-File    File Compressed.
    '''
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_file)

def correlations_existing_variable(filename, variable, matrix_path):
    # Data importation.
    data = pd.read_csv(filename)

    # Selection of data of interest.
    data_of_interest = [variable] + list(data.columns[-36:])
    data_interest = data[data_of_interest]

    # Correlation computation.
    correlations = data_interest.corr(method='pearson')

    # Correlation Matrix plot.
    fig = plt.figure(figsize=(30, 24))
    sns.heatmap(correlations, annot=True, fmt=".2f", cmap='YlGnBu', cbar=True)
    plt.title('Correlation Matrix.')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    fig.savefig(matrix_path+'.pdf')
    fig.savefig(matrix_path+'.png')

    # Show correlations
    correlations = correlations.drop(variable)
    print(correlations[variable])

def correlations_new_variable(filename, variable, matrix_path):
    # Data importation.
    data = pd.read_csv(filename)

    # Count the new variable and add to the data
    counts = data[variable].value_counts().to_frame(name='listing_count')
    data_with_counts = data.join(counts, on=variable)
    
    # Selection of data of interest.
    data_of_interest = ['listing_count'] + list(data.columns[-36:])
    data_interest = data_with_counts[data_of_interest]

    # Correlation computation.
    correlations = data_interest.corr(method='pearson')

    # Correlation Matrix plot.
    fig = plt.figure(figsize=(30, 24))
    sns.heatmap(correlations, annot=True, fmt=".2f", cmap='YlGnBu', cbar=True)
    plt.title('Correlation Matrix.')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    fig.savefig(matrix_path+'.pdf')
    fig.savefig(matrix_path+'.png')

    # Show correlations
    correlations = correlations.drop('listing_count')
    print(correlations['listing_count'])

# Run the script as a standalone application
if __name__ == "__main__":
    ## Distances calculation
    hosts            = 'Information/hosts.csv'
    cultural_places  = 'Information/cultural_places.csv'
    cultural_result  = 'Results/hosts_with_distances_cultural.csv'
    Distances(hosts, cultural_places, cultural_result)

    # Correlations First Test
    variable_1       = 'host_is_superhost'
    Matrix_path_1    = 'Results/Correlation_Matrix_1'
    correlations_existing_variable(cultural_result, variable_1, Matrix_path_1)

    # Correlations Second Test
    variable_2       = 'host_total_listings_count'
    Matrix_path_2    = 'Results/Correlation_Matrix_2'
    correlations_existing_variable(cultural_result, variable_2, Matrix_path_2)

    # Correlations Third Test
    variable_3       = 'host_id'
    Matrix_path_3    = 'Results/Correlation_Matrix_3'
    correlations_new_variable(cultural_result, variable_3, Matrix_path_3)