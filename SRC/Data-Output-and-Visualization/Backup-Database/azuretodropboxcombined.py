##Author: Sumay Kalra

from azure.storage.blob import BlobServiceClient
import os
import dropbox



def csv(CSV_FILE_NAME):
    # Azure Storage credentials
    AZURE_STORAGE_CONNECTION_STRING =   ##                                                     # add your access key
    AZURE_CONTAINER_NAME = 'containertest'
    BLOB_FOLDER = 'combined_table'
    LOCAL_DIRECTORY = ##                                                                       # add your desired local directory

    # Initialize Azure Storage client
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    # Get the blob client for the CSV file within the specified folder
    blob_client = container_client.get_blob_client(blob=BLOB_FOLDER + '/' + CSV_FILE_NAME)
    # Download the blob to the local directory
    local_file_path = LOCAL_DIRECTORY + '\\' + CSV_FILE_NAME
    print(local_file_path)
    with open(local_file_path, 'wb') as file:
        blob_data = blob_client.download_blob()
        file.write(blob_data.readall())

    print(f"Blob '{CSV_FILE_NAME}' downloaded to '{local_file_path}'.")


CSV_FILE_NAME = ['database_combined.csv']
for name in CSV_FILE_NAME:
    csv(name)

