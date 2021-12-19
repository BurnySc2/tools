import sys
from pathlib import Path

# Be able to launch from root folder
sys.path.append(str(Path(__file__).parents[1]))

# Other
# Coroutines and multiprocessing
import asyncio
import re
import time

# Type annotation / hints
from typing import List

import aiohttp

# Simple logging https://github.com/Delgan/loguru
from loguru import logger

# Local examples
from python_examples.examples.async_await.asyncio_download_upload import download_all_sites, download_file
from python_examples.examples.async_await.rate_limited_example import api_rate_limited_example
from python_examples.examples.databases.mongodb_example import test_database_with_mongodb
from python_examples.examples.databases.sqlalchemy_example import test_database_with_sqlalchemy
from python_examples.examples.databases.sqlite_example import test_database
from python_examples.examples.databases.sqlmodel_example import test_database_with_sqlmodel
from python_examples.examples.databases.tinydb_example import test_database_with_tinydb
from python_examples.examples.dataclasses_and_dicts.import_export_dataclass import test_data_class_to_and_from_json
from python_examples.examples.dataclasses_and_dicts.modify_dictionary import modify_dictionary
from python_examples.examples.other.file_interaction import create_file
from python_examples.examples.other.geometry_example import test_geometry_shapely
from python_examples.examples.other.image_manipulation import mass_convert_images
from python_examples.examples.other.measure_time import measure_time
from python_examples.examples.other.multiprocessing_example import do_math, do_multiprocessing
from python_examples.examples.other.regex_example import regex_match_test, test_all_roman_numbers

logger.remove()  # Remove previous default handlers
# Log to console
logger.add(sys.stdout, level='INFO')
# Log to file, max size 1 mb, max log file age 7 days before a new one gets created
logger.add('main.log', rotation='1 MB', retention='7 days', level='INFO')


def main_sync():
    asyncio.run(main())


async def main():
    logger.info('Simple {} logger output', 'loguru')

    regex_match_test()

    measure_time()

    sites: List[str] = ['http://www.jython.org', 'http://olympus.realpython.org/dice'] * 80
    start_time = time.perf_counter()
    await download_all_sites(sites)

    # Download an image with download speed throttle
    async with aiohttp.ClientSession() as session:
        _result: bool = await download_file(
            session,
            url='https://file-examples.com/wp-content/uploads/2017/10/file_example_PNG_1MB.png',
            file_path=Path(__file__).parent / 'data' / 'image.png',
            temp_file_path=Path(__file__).parent / 'data' / 'image_download_not_complete',
            # Download at speed of 100kb/s
            download_speed=100 * 2**10,
        )
    # Gather a ton of responses from an API
    await api_rate_limited_example()

    end_time = time.perf_counter()
    logger.info(f'Time for sites download taken: {end_time - start_time}')

    _math_result = do_math(6)

    start_time = time.perf_counter()
    _result2 = do_multiprocessing()
    end_time = time.perf_counter()
    logger.info(f'Time for multiprocessing taken: {end_time - start_time}')

    mass_replace()

    logger.info('Creating hello world file...')
    create_file()

    logger.info('Testing writing dataclass to json and re-load and compare both objects')
    test_data_class_to_and_from_json()

    modify_dictionary()

    logger.info('Validating all roman numbers up to 3999')
    test_all_roman_numbers()

    test_geometry_shapely()

    # TODO Table printing / formatting without library: print table (2d array) with 'perfect' row width

    logger.info('Converting all .jpg images in /images folder')
    mass_convert_images()

    logger.info('Testing database interaction')
    test_database()
    test_database_with_sqlalchemy()
    test_database_with_tinydb()
    test_database_with_sqlmodel()
    await test_database_with_mongodb()


def mass_replace():
    # Source: https://stackoverflow.com/a/6117124
    text = 'my text cond\nition1 condition2'
    replace_dict = {'cond\nition1': 'loves', 'condition2': 'fun'}
    # In case there is escape characters in k, it will not work without "re.escape"
    replace_dict = {re.escape(k): v for k, v in replace_dict.items()}
    pattern = re.compile('|'.join(replace_dict.keys()))
    new_text = pattern.sub(lambda m: replace_dict[re.escape(m.group(0))], text)
    logger.info(f'Mass replaced\n{text}\nto\n{new_text}')


def plot_lists():
    # TODO
    pass


def plot_numpy_array():
    # TODO
    pass


if __name__ == '__main__':
    main_sync()
