import requests
import os
import ctypes
'''
Library of useful functions for working with images.
'''
def main():
    # TODO: Add code to test the functions in this module
    image_url = 'https://www.boredpanda.com/blog/wp-content/uploads/2021/08/Meet-MeonJi-the-black-cat-that-is-the-instagram-sensation-6124b0458c8f5__700.jpg'
    image_data = download_image(image_url)
    success = save_image_file(image_data, r'C:\temp\kitty.jpg')
    set_desktop_background_image(success)

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if succcessful. None, if unsuccessful.
    """
    # TODO: Complete function body
    resp_msg = requests.get(image_url)
    print(f'Downloading image from {image_url}...', end='')
    if resp_msg.status_code == requests.codes.ok:
        file_content = resp_msg.content
        print('success')
        return file_content
    else:
        print('Error: Invalid url')
        return None
        

def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bool: True, if succcessful. False, if unsuccessful
    """
    # TODO: Complete function body
    try:
        with open(image_path, 'wb') as file:
            file.write(image_data)
        return image_path, True
    except:
        return False
    
def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful        
    """
    # TODO: Complete function body
    path = image_path  # Add this [0] to test the individual function, otherwise remove it
    if os.path.isfile(path):
        print(f'Setting desktop to {image_path}')
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        return True
    else:
        print('Error setting the background')
        return False

def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()