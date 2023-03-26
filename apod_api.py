import requests

'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
APOD_URL = 'https://api.nasa.gov/planetary/apod'
APOD_KEY = 'fkWhvO6Ae3R0wHgghBuomv4Fl84FfPJi7GV3fKlD'

def main():
    # TODO: Add code to test the functions in this module

    info = get_apod_info('1999-02-22')
    url = get_apod_image_url(info)
    print(url)
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    pic_url = f'{APOD_URL}?api_key={APOD_KEY}&date={apod_date}&thumbs=True'
    resp_msg = requests.get(pic_url)
    if resp_msg.ok:
        diction = resp_msg.json()
        return diction
    return   None

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    if 'thumbnail_url' in apod_info_dict:
        thumbs = apod_info_dict['thumbnail_url']
        return thumbs
    else:
        hdurl = apod_info_dict['hdurl']
        return hdurl

if __name__ == '__main__':
    main()