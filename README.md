# Spreadsheet Self-Contained Microservice MVP

<img src="rmimg/ECM3408.svg" height="28"> <img src="rmimg/Solo.svg" height="28">

> Development has ended

The minimum viable product of a digital spreadsheet made up of a self contained microservice that uses a RESTful interface to communicate with either an onsite SQLite database or a cloud based No-SQL database.
This project was part of the continuous assessment for the Enterprise Computing module taught by Dr David Wakeling.

## Installation

## Configuration

### Database Reset

For the purposes of development, the database is **RESET** each time the program is run. To disable this simply set the variable 'reset' from 'True' to 'False' in the main entry point of file `sc.py`.

```Python
if __name__ == "__main__":
    reset = True  # Set to False to maintain database through restarts
```

### Firebase No-SQL address

The program takes the name of your server and inserts it into the middle of a string to get the web address as part of the specification. However this limits the use of the cloud provider and server location and so can be manually edited to allow any address in the global variables at the top of the `Firebase.py` file.

```Python
# Set environment variable, database url and node string
name = os.environ['FBASE']
database_url = # Manually enter your server here
```

## Usage



## License

[MIT](https://choosealicense.com/licenses/mit/)
