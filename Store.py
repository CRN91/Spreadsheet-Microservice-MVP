import sqlite3

database = "database.db"


""" Function to initialise the SQLite database. """


def setup():
    # Setting up the database
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        # Creates cells table and its columns
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS cells" +
            "(id TEXT PRIMARY KEY , formula TEXT)"
        )
        connection.commit()


""" Function to create a cell in the database.
    Args:
        cell_id (str): The cell id.
        formula (str): The formula to be stored.
    Returns:
        bool: True if successful, False otherwise."""


def create(cell_id, formula):
    success = False
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        # Inserts new cell into the table
        cursor.execute("INSERT INTO cells(id,formula) VALUES (?,?)",
                       (cell_id, formula))
        connection.commit()
        # Check if the cell was inserted
        if cursor.rowcount > 0:
            success = True
    return success


""" Function to update a cell in the database. 
    Args:
        cell_id (str): The cell id.
        formula (str): The formula to be stored.
    Returns:
        bool: True if successful, False otherwise."""


def update(cell_id, formula):
    success = False
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        # Updates the formula of a specific cell
        cursor.execute("UPDATE cells SET formula=? WHERE id=?",
                       (formula, cell_id))
        connection.commit()
        # Check if the cell was updated
        if cursor.rowcount > 0:
            success = True
    return success


""" Function to read a cell from the database.
    Args:
        cell_id (str): The cell id.
    Returns:
        tuple: The cell id and formula if successful, None otherwise."""


def read(cell_id):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        # Selects the cell by its id
        cursor.execute("SELECT id, formula FROM cells WHERE id = ?", (cell_id,))
        row = cursor.fetchone()
    return row


""" Function to delete a cell from the database.
    Args:
        cell_id (str): The cell id.
    Returns:
        bool: True if successful, False otherwise."""


def delete(cell_id):
    success = False
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        # Deletes the cell by its id
        cursor.execute("DELETE FROM cells WHERE id = ?", (cell_id,))
        connection.commit()
        if cursor.rowcount > 0:
            success = True
    return success


""" Function to read all cell ids from the database.
    Returns:
        list: A list of all cell ids."""


def readall():
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        # Selects all cell ids
        cursor.execute("SELECT id FROM cells", )
        cells = []
        for row in cursor.fetchall():
            cells.append(row)
    # Returns in a list format
    return [i[0] for i in cells]
    

""" Function to delete all cells from the database. 
    Return:
        bool: True if all cells deleted from the database. """


def deleteall():
    success = False
    ids = readall()
    if ids:
        success = True
        for cell_id in ids:
            if not delete(cell_id):
                success = False
    return success
