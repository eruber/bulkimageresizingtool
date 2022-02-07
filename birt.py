"""
birt - Bulk Image Resizing Tool Module

OVERVIEW
Resize a group of images that reside in a specified directory PATH to be less than or equal to WIDTH, HEIGHT while
maintaining the correct image orientation.

By default the resized images will be placed in a sub-directory of PATH named 'resized'. Use the --subdir SUBDIR to
change this default directory name.

If a resized image save throws an exception, an attempt will be made to convert the image to JPG and save it again.
This functionality was added when a .HEIC image could not be saved, but the converted JPG image could be saved.

DEPENDENCIES
    Pillow (9.0.1) - manages image manipulation

AUTHOR
    E.R. Uber (eruber@gmail.com)

CREATED
    6 FEB 2020 using Python 3.9 and the free version of PyCharm (https://www.jetbrains.com/help/pycharm/)

LICENSE
    MIT (https://opensource.org/licenses/MIT)
"""
# Python Standard Library
import os
import os.path
import logging

logr = logging.getLogger('birt').getChild(__name__)

# 3rd Party Dependencies
from PIL import Image


def determine_resize(constraint_x, constraint_y, img_x, img_y):
    """
    Given constraint dimensions and image dimensions, determine the correct
    resizing dimensions.

    :param constraint_x: integer, constraint width
    :param constraint_y: integer, constraint height
    :param img_x: integer, image width
    :param img_y: integer, image height
    :return: A tuple of integers of resized dimensions, (width, height)
    """
    new_y = int((constraint_x * img_y) / img_x)
    if new_y <= constraint_y:
        return constraint_x, new_y
    else:
        new_x = int((constraint_y * img_x) / img_y)
        if new_x <= constraint_x:
            return new_x, constraint_y
        else:
            return constraint_x, constraint_y


def reorient_image(im):
    """
    Explanation text mostly from: https://stackoverflow.com/a/4228725

    When a picture is taller than it is wide, it means the camera was rotated.
    Some cameras can detect this and write that info in the picture's EXIF metadata.
    Some image viewers take note of this metadata and transpose (which is better than rotate) the image
    to display it correctly.

    Note: PIL can read the picture's metadata, but it does not write/copy metadata when you save an Image.

    Without this function, pictures taken with a rotated camera do not have the correct orientation
    after being resized. So this function is necessary for a complete image resizing solution.

    Code for this function lifted verbatim from: https://stackoverflow.com/a/48691518

    Also a complete set of test images that illustrate this orientation issue are available at:
    https://github.com/recurser/exif-orientation-examples

    :param im: PIL Image object
    :return:  PIL Image object
    """
    try:
        # Stackoverflow indicates that the EXIF metadata is only available for JPG images...
        # image_exif = im._getexif()
        image_exif = im.getexif()  # PIL 6.2.2 offers a non-private method to use

        image_orientation = image_exif[274]
        if image_orientation in (2, '2'):
            return im.transpose(Image.FLIP_LEFT_RIGHT)
        elif image_orientation in (3, '3'):
            return im.transpose(Image.ROTATE_180)
        elif image_orientation in (4, '4'):
            return im.transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (5, '5'):
            return im.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (6, '6'):
            return im.transpose(Image.ROTATE_270)
        elif image_orientation in (7, '7'):
            return im.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (8, '8'):
            return im.transpose(Image.ROTATE_90)
        else:
            return im
    except (KeyError, AttributeError, TypeError, IndexError):
        return im


def resize_images(path, width, height, test, subdir):
    """
    Resize and possible rename and/or relocate resized images.

    :param path: PathObject, location of source images
    :param width: int, maximum x size of resized images
    :param height: int, maximum y size of resized images
    :param test: bool, if True only output what would be done, but don't do it
    :param subdir: PathObject, sub-directory to relocate resized images
    :return: None
    """
    # Count Images Processed
    i = 0  # Total file count
    r = 0  # Resized file count
    rf = 0  # Resized failure count
    nf = 0  # Not recognized as an image count
    sf = 0  # Save failure count
    d = 0  # Not files (probably directories) count
    abspath = os.path.abspath(path)

    # If necessary create a sub-directory
    abs_subdir = os.path.join(abspath, subdir)
    if not os.path.exists(abs_subdir):
        os.makedirs(abs_subdir)

    path_contents = os.listdir(abspath)

    for pth_item in path_contents:
        logr.debug("="*80)
        i = i + 1
        logr.debug("Path Item {}: {}".format(i, pth_item))
        pth_item_abs = os.path.join(abspath, pth_item)
        if os.path.isfile(pth_item_abs):
            logr.info("Image.open('{}')".format(pth_item_abs))
            image = None
            if not test:
                try:
                    image = Image.open(pth_item_abs)
                except Exception as e:
                    logr.info("File '{}' not image file: {}".format(pth_item_abs, e))
                    nf = nf + 1
                    continue

                image = reorient_image(image)

                file_path, ext = os.path.splitext(pth_item_abs)
                img_path = os.path.dirname(file_path)
                img_basename = os.path.basename(file_path)

                size = image.size
                img_x = size[0]
                img_y = size[1]
                logr.debug("Image Size: {} {}".format(img_x, img_y))

                new_x, new_y = determine_resize(width, height, img_x, img_y)
                logr.debug("New Width: {}  New Height: {}".format(new_x, new_y))

                try:
                    image = image.resize((new_x, new_y), Image.ANTIALIAS)
                except Exception as e:
                    logr.error("Unable to resize file '{}' exception: {}".format(pth_item_abs, e))
                    image.close()
                    rf = rf + 1
                    continue

                new_name = os.path.join(abs_subdir, img_basename) + ext

                logr.info("Resized and saving image: '{}'".format(new_name))

                try:
                    image.save(new_name)
                    # image.save(new_name, 'JPEG', quality=95)
                except Exception as e:
                    logr.error("Unable to save '{}' exception: {}".format(new_name, e))

                    sf = sf + 1

                    # If throw save exception, try and convert the image to JPG and then try and save it
                    logr.info("Attempt to convert {} image to JPG and save it...".format(ext))
                    try:
                        rgb_img = image.convert('RGB')
                    except Exception as e:
                        logr.error("Unable to convert image to JPG from {} after save failure, exception: {}".format(ext, e))
                        image.close()
                        continue

                    new_name = os.path.join(abs_subdir, img_basename) + '.jpg'

                    logr.debug("Saving image: {}".format(new_name))
                    try:
                        rgb_img.save(new_name)
                    except Exception as e:
                        logr.error("Unable to save '{}' after JPG conversion, exception: {}".format(new_name, e))
                        image.close()
                        continue

                    image.close()
                    continue

                r = r + 1

            if not test:
                if image:
                    image.close()
        else:
            # Not a file
            logr.debug("Not a file!")
            d = d + 1

    T = r + d + nf + rf + sf

    logr.info("Files Processed: {:>4}".format(i))
    logr.info("------------------------")
    logr.info("        Resized: {:>4}".format(r))
    logr.info("      Not files: {:>4}".format(d))
    logr.info("     Not images: {:>4}".format(nf))
    logr.info("   Resized Fail: {:>4}".format(rf))
    logr.info("     Saved Fail: {:>4}".format(sf))
    logr.info("               ---------")
    logr.info("          Total: {:>4}".format(T))

