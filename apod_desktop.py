""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
import sqlite3
from datetime import date
import os
import image_lib
import inspect
import re
import urllib.parse
from sys import argv, exit
import apod_api
import image_lib
import hashlib

# Global variables
image_cache_dir = None  # Full path of image cache directory
image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body
    if len(argv) == 1:
        today = date.today()
        return today
    
    elif len(argv) == 2:
        try: 
            time = argv[1]
            apod_date = date.fromisoformat(time)
        except Exception as error:
            print(f'Error: Invalid date format: {error}')
            print('Script execution aborted')
            exit()

        lower = date(1995, 6, 16)
        if apod_date < lower:
            print('Error: Date is too far in the past')
            print('Script execution aborted')
            exit()
        elif apod_date > date.today():
            print('Error: APOD date cannot be in the futre')
            print('Script execution aborted')
            exit()
        else:
            return apod_date
        
    else:
        exit()
    

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    global image_cache_dir
    global image_cache_db
    # TODO: Determine the path of the image cache directory
    image_cache_dir = os.path.join(parent_dir, 'image_cache')
    print(f'Image cache directory: {image_cache_dir}')
    # TODO: Create the image cache directory if it does not already exist
    if os.path.isdir(image_cache_dir):
        print('Image cache directory already exists.')
    else:
        os.mkdir(image_cache_dir)

    # TODO: Determine the path of image cache DB
    image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')
    print(f'Image cache DB: {image_cache_db}')
    # TODO: Create the DB if it does not already exist
    if not os.path.exists(image_cache_db):
        con = sqlite3.connect(image_cache_db)
        cur = con.cursor()
        create_image_cache_tbl="""
            CREATE TABLE IF NOT EXISTS image_cache
            (
                id              INTEGER PRIMARY KEY,
                title           TEXT NOT NULL,
                explanation     TEXT NOT NULL,
                path            TEXT NOT NULL,
                hash            TEXT NOT NULL,
                date            TEXT NOT NULL
            );
        """
        cur.execute(create_image_cache_tbl)
        con.commit()
        con.close()
        print('Image cache DB created.')
    else:
        print('Image cache DB already exists.')


def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date)
    
    # TODO: Download the APOD information from the NASA API
    print(f'Getting {apod_date} APOD information from NASA...', end='')
    apod_info = apod_api.get_apod_info(apod_date)
    if apod_info:
        print('success')
    else:
        print('failure')
    apod_url = apod_api.get_apod_image_url(apod_info)
    title = apod_info['title']
    print(f'APOD title: {title}')
    print(f'APOD URL: {apod_url}')
    apod_explanation = apod_info['explanation']

    # TODO: Download the APOD image
    download_apod = image_lib.download_image(apod_url)
    check_hash = hashlib.sha256(download_apod).hexdigest()
    print(f'APOD SHA-256: {check_hash}')

    # TODO: Check whether the APOD already exists in the image cache
    check_db = get_apod_id_from_db(check_hash)
    
    if check_db != 0:
        print('APOD image already in cache.')
        return check_db
    elif check_db == 0:
        print('APOD image is not already in cache')
        path = determine_apod_file_path(title, apod_url)
        print(f'APOD file path: {path}')
        save_image = image_lib.save_image_file(download_apod, path)
        print(f'Saving image file as {save_image[0]}')
        adding_info = add_apod_to_db(title, apod_explanation, path, check_hash, apod_date)
        return adding_info
    else:
        return 0

    # TODO: Save the APOD file to the image cache directory
    # TODO: Add the APOD information to the DB

    # return 0

def add_apod_to_db(title, explanation, file_path, sha256, date):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
    # TODO: Complete function body
    print('Adding APOD to image cache DB...', end='')
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    add_image_cache_query = """
        INSERT INTO image_cache
        (
            title,
            explanation,
            path,
            hash,
            date   
        )
        VALUES (?, ?, ?, ?, ?);
    """
    image_cache = (
        title,
        explanation,
        file_path,
        sha256,
        date
        )
    id = cur.execute(add_image_cache_query, image_cache)
    con.commit()
    con.close()
    last_row = id.lastrowid
    if last_row:
        print('success')
        return last_row
    else:
        print('failure')
        return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    get_sha256 = f"""
        SELECT id FROM image_cache
        WHERE hash='{image_sha256}'
    """
    cur.execute(get_sha256)
    query_result = cur.fetchall()
    con.close()
    if query_result:
        return query_result[0][0]
    else:
        return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    path = urllib.parse.urlsplit(image_url).path
    ext = os.path.splitext(path)[1]
    title = re.sub(r'[\s+\#:;!@\$%\^&\*()\-=\+\.,\/"\|\{\}<>?\[\]\'\"]', r'_', image_title)
    whole_title = re.sub(r'_+', '_', title)
    file_name = whole_title + ext
    image_path = os.path.join(image_cache_dir, file_name)      
    return image_path

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    add_image_cache_query = f"""
    SELECT title, explanation, path FROM image_cache
    WHERE id='{image_id}'
    """
    cur.execute(add_image_cache_query)
    query_result = cur.fetchone()
    con.close()
    # TODO: Put information into a dictionary
    apod_info = {
        'title': query_result[0], 
        'explanation': query_result[1],
        'file_path': query_result[2],
    }
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    add_image_cache_query = f"""
    SELECT title FROM image_cache
    """
    cur.execute(add_image_cache_query)
    query_result = cur.fetchall()
    con.close()
    results = [query for r in query_result for query in r]

    # NOTE: This function is only needed to support the APOD viewer GUI
    return results

if __name__ == '__main__':
    main()