import requests
'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
APOD_URL = f'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date=1995-06-16&end_date&thumbs=True'
resp_msg = requests.get(APOD_URL)

def main():
    # TODO: Add code to test the functions in this module
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    return   

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    return

if __name__ == '__main__':
    main()