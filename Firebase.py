import requests
import os

# Set environment variable, database url and node string
name = os.environ['FBASE']
database_url = 'https://' + name + '-default-rtdb.europe-west1.firebasedatabase.app/'
node = 'cells'  # Parent node of noSQL database


""" Function to create / update a cell in the database.
    Args:
        cell_id (str): The cell id.
        formula (str): The formula to be stored.
    Returns:
        int: HTTP status code."""


def create(cell_id, formula):
    return requests.put(f'{database_url}/{node}/{cell_id}.json', json=formula).status_code


""" Function to read a cell from the database.
    Args:
        cell_id (str): The cell id.
    Returns:
        str: The formula if successful, None otherwise."""


def read(cell_id):
    return requests.get(f'{database_url}/{node}/{cell_id}.json').json()


""" Function to check if a cell exists in the database.
    Args:
        cell_id (str): The cell id.
    Returns:
        int: HTTP status code """


def exists(cell_id):
    return requests.get(f'{database_url}/{node}/{cell_id}.json').status_code


""" Function to delete a cell from the database.
    Args:
        cell_id (str): The cell id.
    Returns:
        int: HTTP status code."""


def delete(cell_id): # returns 200 on success not 204
    return requests.delete(f'{database_url}/{node}/{cell_id}.json').status_code


""" Function to read all cells from the database.
    Returns:
        list: A list of cell ids."""


def readall():
    ids = requests.get(f'{database_url}/{node}.json').json()
    if ids:
        return list(ids.keys())
    else:
        return []
    

""" Function to delete all cells from the database.
    Return:
        bool: True if cells successfully deleted from the database. """


def deleteall():
   success = False
   ids = readall()
   if ids:
       success = True
       for cell_id in ids:
           if delete(cell_id) != 200:
               success = False
   return success