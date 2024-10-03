from flask import Flask, request, jsonify
import argparse
import ast
import Store
import Firebase

app = Flask(__name__)

# Parse command line arguments to specify database
parser = argparse.ArgumentParser()
# SQLite is default and firebase can be specified with -r firebase
parser.add_argument('-r', '--database', choices=['sqlite', 'firebase'], default='sqlite')
args = parser.parse_args()


""" Function to create / update a cell. """


@app.route('/cells/<string:cell_id>', methods=['PUT'])
def create(cell_id):
    # Get JSON from request
    json = request.get_json()
    # Check cell_id in JSON and URL match
    if cell_id != json.get("id"):
        return "", 400  # Bad Request

    # Get formula from JSON
    formula = json.get("formula")
    # Check for formula
    if formula:
        # SQLite
        if args.database == 'sqlite':
            # Update cell if one exists
            if Store.read(cell_id) is not None:
                Store.update(cell_id, formula)
                return "", 204  # No Content
            # Create new cell if one doesn't exist
            else:
                if Store.create(cell_id, formula):
                    return "", 201  # Created
                else:
                    return "", 500  # Internal Server Error
        # Firebase (update and create are the same)
        elif args.database == 'firebase':
            data = Firebase.read(cell_id)
            # Update
            if data:
                if Firebase.create(cell_id, formula) == 200:
                    return "", 204  # No Content
                else:
                    return "", 400  # Bad Request
            # Create
            else:
                if Firebase.create(cell_id, formula) == 200:
                    return "", 201  # Created
                else:
                    return "", 400  # Bad Request
                
        # Database not specified
        else:
            return "", 500  # Internal Server Error
    # Formula not sent
    else:
        return "", 400  # Bad Request


""" Function to read a cell. """


@app.route("/cells/<string:cell_id>", methods=["GET"])
def read(cell_id):
    # SQLite
    if args.database == 'sqlite':
        # Read database
        data = Store.read(cell_id)
        if data:
            # Calculate formula and return JSON
            post = '{"id":"' + f'{data[0]}' + '","formula":"' + f'{calculate(data[1])}' + '"}'
            return post, 200  # OK
        else:
            return "", 404  # Not Found
    # Firebase
    elif args.database == 'firebase':
        # Read database
        data = Firebase.read(cell_id)
        if data:
            # Calculate formula and return JSON
            post = '{"id":"' + f'{cell_id}' + '","formula":"' + f'{calculate(data)}' + '"}'
            return post, 200  # OK
        else:
            return "", 404  # Not Found
    # Database not specified
    else:
        return "", 500  # Internal Server Error


""" Function to delete a cell. """


@app.route("/cells/<string:cell_id>", methods=["DELETE"])
def delete(cell_id):
    # SQLite
    if args.database == 'sqlite':
        # Attempt to delete cell
        if Store.delete(cell_id):
            return "", 204  # No Content
        else:
            return "", 404  # Not Found
    # Firebase
    elif args.database == 'firebase':
        # requests returns 200 regardless if cell exists
        data = Firebase.read(cell_id)
        if data:
            Firebase.delete(cell_id)
            return "", 204  # No Content
        else:
            Firebase.delete(cell_id)
            return "", 404  # Not Found
    # Database not specified
    else:
        return "", 500  # Internal Server Error


""" Function to list all cell ids. """


@app.route("/cells", methods=["GET"])
def listing():
    # SQLite
    if args.database == 'sqlite':
        # Read all cells as a list of cell ids
        data = Store.readall()
    # Firebase
    elif args.database == 'firebase':
        # Read all cells as a list of cell ids
        data = Firebase.readall()
    # Database not specified
    else:
        return "", 500  # Internal Server Error

    if data:
        return jsonify(data), 200  # OK
    else:
        # Functionality to return empty list if no cells
        return "[]", 200  # OK


""" Function to evaluate the result of formula.

    Args: 
        formula (str): A string that can contain numbers, cell ids
        or a formula containing either numbers, cell ids or a
        combination of both using the operators +, -, *, /.
    Returns: 
           (float,int): The result of calculating formula.
"""


def calculate(formula):
    # Split formula into its components and iterate through them to evaluate
    components = formula.split()
    # Will do lots of checks but its to protect eval from malicious code
    for i in range(len(components)):
        # Get component
        part = components[i]

        # Checks if number
        try:
            if isinstance(ast.literal_eval(part), (int, float)):
                continue  # No need to change
        except (SyntaxError, ValueError):
            pass

        # Changes x to * for eval
        if part == 'x':
            components[i] = '*'
        elif part in ['+', '-', '*', '/']:
            continue  # No need to change

        # Checks if cell
        elif part[0].isalpha():
            # SQLite
            if args.database == 'sqlite':
                read_value = Store.read(part)[1]
            # Firebase
            elif args.database == 'firebase':
                read_value = Firebase.read(part)
            # Database not specified, can't send server error in recursion
            else:
                raise ValueError("500 Internal Server Error: Database not specified")
            # Recursion to evaluate cell id's value
            components[i] = str(calculate(read_value))
        # Not correct format, can't send server error in recursion
        else:
            raise ValueError("400 Bad Request")

    # Calculate formula, checks should make eval safe
    return eval(" ".join(components))


if __name__ == "__main__":
    # test10.sh needed to have the database reset, so this deletes all cells
    reset = True  # Set to False to maintain database through restarts
    if args.database == 'sqlite':
        # Initialise SQLite database
        Store.setup()
        if reset:
            Store.deleteall()
    elif args.database == 'firebase':
        if reset:
            Firebase.deleteall()
    app.run(port=3000)
