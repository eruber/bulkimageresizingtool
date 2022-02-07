"""
cli - Command Line Interface module for the bulk image resizing tool (BIRT) module.

See --help for more details.

DEPENDENCIES
    Click (8.0.3)  - manages the command line interface, https://palletsprojects.com/p/click/
    Pillow (9.0.1) - manages image processing, https://pillow.readthedocs.io/en/stable/index.html

AUTHOR
    E.R. Uber (eruber@gmail.com)

CREATED
    6 FEB 2020 using Python 3.9 and the free version of PyCharm (https://www.jetbrains.com/help/pycharm/)

LICENSE
    MIT (https://opensource.org/licenses/MIT)

ARCHITECTURAL NOTES
    BIRT is command line utility written as a module with all its functionality contained within a single source file;
    however, it is also distributed with setup tools so it is easy to configure a virtual environment, install birt,
    and execute it. As in the following on Windows when birt's setup.py is in the current directory:

        > python -m venv BIRT_VENV
        > BIRT_VENV/Scripts/activate.bat
        > pip install --editable .
        > birt --help

    Or on Linux with virtualenv:

       $ virtualenv BIRT_VENV
       $ . BIRT_VENV/bin/activate
       $ pip install --editable .
       $ birt --help

USAGE
    birt some/dir/with/images/to/resize 1200 800

    The above usage will create any resized images in some/dir/with/images/to/resize/resized
"""
# Python Standard Library
import logging as LOGGING

# 3rd Party Dependencies
import click

# Application Specific
import version
import birt

IDENT = 'BIRT (Bulk Image Resizing Tool)'
VERSION = version.VERSION
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DEFAULT_SUBDIR = "resized"

LEVELS = {
    'NOTSET': LOGGING.NOTSET,
    'DEBUG': LOGGING.DEBUG,
    'INFO': LOGGING.INFO,
    'WARNING': LOGGING.WARNING,
    'ERROR': LOGGING.ERROR,
    'CRITICAL': LOGGING.CRITICAL,
}


def setup_logging(level_ch):
    """
    Configure console and file logging handlers.

    :param level_ch: logging level for console
    :return: logger
    """
    logger = LOGGING.getLogger('birt')
    logger.setLevel(LOGGING.DEBUG)
    # create file handler which logs even debug messages
    fh = LOGGING.FileHandler('birt.log', 'w')
    fh.setLevel(LOGGING.DEBUG)
    formatter_fh = LOGGING.Formatter('%(asctime)s : %(name)s : %(funcName)s : LINE %(lineno)s : %(levelname)s : %(message)s')
    fh.setFormatter(formatter_fh)
    logger.addHandler(fh)

    # create console handler with a higher log level
    ch = LOGGING.StreamHandler()
    ch.setLevel(LEVELS[level_ch])
    # create formatter and add it to the handlers
    formatter_ch = LOGGING.Formatter('%(asctime)s : %(name)s : %(funcName)s : %(levelname)s : %(message)s')
    ch.setFormatter(formatter_ch)
    # add the handlers to logger
    logger.addHandler(ch)

    return logger, ch, fh


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('path', type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True))
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.option('--subdir', type=click.Path(exists=False, file_okay=False, writable=True, resolve_path=True),
              metavar='SUBDIR', default=DEFAULT_SUBDIR, help='Create resized images in SUBDIR with the same file names. Default: "{}"'.format(DEFAULT_SUBDIR))
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output (--logging_level=DEBUG)')
@click.option('--quiet', '-q', is_flag=True, help='Enable quiet output (--logging_level=ERROR)')
@click.option('--logging-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=True))
@click.option('--test', '-t', is_flag=True, help='Test Mode, do not process images, just emit what would be done.')
def cli(path, width, height, subdir, verbose, quiet, logging_level, test):
    """
    Resize images in PATH to a size that is limited to (WIDTH, HEIGHT).

    By default the resized image files will be placed in a sub-directory of PATH named "resized".
    Use the --subdir SUBDIR option to change the default name of this sub-directory.

    """
    if logging_level is None:
        logging_level = 'INFO'

    logr, console_handler, file_handler = setup_logging(logging_level)

    logr.info("{} {}".format(IDENT, VERSION))

    if verbose:
        console_handler.setLevel(LOGGING.DEBUG)

    if quiet:
        console_handler.setLevel(LOGGING.ERROR)

    logr.debug('path: {}'.format(path))
    logr.debug('width: {}'.format(width))
    logr.debug('height: {}'.format(height))
    logr.debug('subdir: {}'.format(subdir))
    logr.debug('test: {}'.format(test))
    logr.debug('logging_level: {}'.format(logging_level))
    logr.debug('verbose: {}'.format(verbose))

    # Call the birt module's resize function
    birt.resize_images(path, width, height, test, subdir)


if __name__ == '__main__':
    cli()

