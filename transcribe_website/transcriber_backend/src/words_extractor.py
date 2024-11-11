"""
Extract mp4 clips where someone in the video says a specific word from the list.
"""

from __future__ import annotations

import os
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# pyre-fixme[16]
looking_for_lower_case_words: list[str] = os.getenv("WORDS_EXTRACTOR_WORDS").split(";")

# pyre-fixme[6]
out_path = Path(os.getenv("WORDS_EXTRACTOR_OUTPUT_DIRECTORY"))
out_path.mkdir(parents=True, exist_ok=True)

SYMBOLS = "!?.,"
SENTENCE_END_SYMBOLS = "!?."
CHUNK_SIZE = 300  # 5 minutes chunk size
BUFFER_SIZE = 10  # 10 extra seconds
CLIP_BUFFER = 3  # How many seconds of context


def extract_with_ffmpeg(
    input_file_str: str,  # The input file path from which to extract a clip.
    clip_out_path: Path,  # The output file path where the extracted clip will be saved.
    clip_start_str: str,  # The start time of the clip in seconds.
    clip_end_str: str,  # The end time of the clip in seconds.
) -> None:
    """
    Extract a clip from the input video file using ffmpeg.
    """
    # Extract .mp4 clip
    logger.info(f"Extracting: {clip_out_path.as_posix()}")
    subprocess.check_call(
        f'ffmpeg -ss {clip_start_str} -to {clip_end_str} -i "{input_file_str}" -c copy -loglevel error -stats "{clip_out_path.as_posix()}"',  # noqa: E501
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def print_words_overview() -> None:
    """
    Prints a summary of the words found in the videos.

    This function prints a summary of the words found in the videos. It retrieves the words from the database and counts their occurrences in each video. The function then prints the top 10 most common words for each video.
    """  # noqa: E501
    global words_table
    results = words_table.find(video_relative_path={"like": f"{input_path}%"}, order_by=["video_relative_path"])
    counters: dict[str, Counter] = {}
    for row in results:
        video_relative_path, word = row["video_relative_path"], row["word"]
        if video_relative_path not in counters:
            counters[video_relative_path] = Counter()
        counters[video_relative_path][word] += 1
    counter: Counter
    for video_relative_path, counter in counters.items():
        logger.info(f"{video_relative_path} has words:")
        print(counter.most_common(10))
    # pyre-fixme[6, 9]
    total_counter: Counter = sum(counters.values(), start=Counter())
    # Write total word count to file
    words_path = Path(__file__).parent / "words.txt"
    with words_path.open("w") as f:
        for word, count in total_counter.most_common():
            f.write(f"{word}: {count}\n")


def extract_matched_words(
    executor: ThreadPoolExecutor,
    input_file: Path,
    words: list[str],
) -> None:
    """
    Extracts clips from the input video file for the given list of words.

    This function extracts clips from the input video file for the given list of words. It retrieves the words from the database and finds the corresponding timestamps. For each word, it extracts a clip starting 3 seconds before the word and ending 3 seconds after the word. The extracted clips are saved in the output directory with a filename containing the input file name, start and end timestamps, and the word.
    """  # noqa: E501
    global words_table
    assert len(words) >= 1
    input_file_str = str(input_file.resolve())
    results = words_table.find(video_relative_path=input_file_str, word=words, order_by=["word_start_timestamp"])
    for row in results:
        start_time, end_time, word = row["word_start_timestamp"], row["word_end_timestamp"], row["word"]
        clip_start = max(0, start_time - CLIP_BUFFER)
        clip_end = end_time + CLIP_BUFFER

        clip_start_str = f"{clip_start:.3f}"
        clip_end_str = f"{clip_end:.3f}"

        clip_out_path = out_path / f"{input_file.stem} {clip_start_str} {clip_end_str} - {word}.mp4"
        if clip_out_path.is_file():
            continue
        # Extract clip in new thread
        executor.submit(
            extract_with_ffmpeg,
            input_file_str,
            clip_out_path,
            clip_start_str,
            clip_end_str,
        )


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=8) as exec:
        for my_file in recurse_path(input_path, depth=2):
            if my_file.suffix not in [".mp4", ".webm"]:
                continue
            extract_info(exec, my_file)
            extract_matched_words(
                exec,
                my_file,
                looking_for_lower_case_words,
            )
    print_words_overview()
