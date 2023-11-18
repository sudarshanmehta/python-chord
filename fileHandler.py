import os
import hashlib

def upload_file(hashed_file_name, data):
    # Assuming 'FileData' is a global dictionary
    # global FileData

    # Get the current working directory
    current_directory = os.getcwd()

    # Create a file path using the hashed file name in the current directory
    file_path = os.path.join(current_directory, str(hashed_file_name)+".txt ")

    # Write data to the file
    with open(file_path, 'w') as file:
        file.write(data)

    # Update the FileData map
    # FileData[hashed_file_name] = file_path

def download_file(hashed_file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, str(hashed_file_name)+".txt ")

    with open(file_path, 'w') as file:
        file_data = file.read()
        return file_data

# Example usage:
# Assuming FileData is an empty dictionary initially
# FileData = {}

# # Example data and hashed file name
# data = "This is the content of the file."
# hashed_file_name = hashlib.md5(data.encode()).hexdigest()

# # Call the file_handler function
# file_handler(hashed_file_name, data)

# # Print the updated FileData map
# print(FileData)
