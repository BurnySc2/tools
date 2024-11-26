# https://github.com/m-bain/whisperX
import os
from pathlib import Path
from typing import Literal

import whisperx  # pyre-fixme[21]
from dotenv import load_dotenv
from loguru import logger
from whisperx.types import AlignedTranscriptionResult, SingleAlignedSegment, SingleWordSegment

from prisma import Prisma
from src.helper import recurse_path

load_dotenv()

# from faster_whisper import utils
# See "faster_whisper/utils.py:_MODELS"
# https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/utils.py
type model_sizes = Literal[
    "tiny",
    "base",
    "small",
    "medium",
    "large",
    "turbo",
    "tiny.en",
    "base.en",
    "small.en",
    "medium.en",
    # https://huggingface.co/distil-whisper/distil-large-v2
    # Only avaliable for english!
    "distil-large-v2",
    "distil-large-v3",
    "distil-medium.en",
    "distil-small.en",
]
type language_codes = Literal["en", "fr", "de", "es", "it", "ja", "zh", "nl", "uk", "pt"]


def transcribe_file(
    file_path: Path,
    model_size: model_sizes,
    language: language_codes | None = None,
) -> AlignedTranscriptionResult:
    # Models: https://github.com/openai/whisper#available-models-and-languages

    device = "cpu"
    batch_size = 4
    compute_type = "int8"

    # save model to local path (optional)
    model_dir = "whisper_models"

    # TODO Reply to issues:
    # https://github.com/m-bain/whisperX/issues/333
    # https://github.com/m-bain/whisperX/issues/466
    # Maybe using model that only supports english?

    model = whisperx.load_model(model_size, device, compute_type=compute_type, download_root=model_dir)

    audio = whisperx.load_audio(file_path)
    result = model.transcribe(audio, batch_size=batch_size, language=language)

    # delete model if low on GPU resources
    # import gc; gc.collect(); torch.cuda.empty_cache(); del model

    # Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result2 = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device,
        # Does it increase accuracy if True?
        return_char_alignments=False,
    )

    result2["language"] = result["language"]
    return result2


def get_all_paths_already_in_db() -> set[str]:
    with Prisma() as db:
        result = db.word.find_many(distinct=["file_felative_path"])

    return {w.file_felative_path for w in result}


def save_result_to_db(
    input_file_path: Path,
    result: AlignedTranscriptionResult,
) -> None:
    input_file_str = input_file_path.as_posix()
    sentences_to_insert = []
    words_to_insert = []

    sentence_segment: SingleAlignedSegment
    for sentence_segment in result["segments"]:
        # Keys required in sentence_segment
        if not ({"text", "start", "end"} <= set(sentence_segment.keys())):
            continue
        start, end, text = sentence_segment["start"], sentence_segment["end"], sentence_segment["text"]
        sentences_to_insert.append(
            {
                "file_felative_path": input_file_str,
                "sentence_start_timestamp": start,
                "sentence_end_timestamp": end,
                "sentence_text": text,
            }
        )

    word_segment: SingleWordSegment
    for word_segment in result["word_segments"]:
        # Keys required in word_segment
        if not ({"word", "start", "end"} <= set(word_segment.keys())):
            continue
        start, end, word = word_segment["start"], word_segment["end"], word_segment["word"]
        words_to_insert.append(
            {
                "file_felative_path": input_file_str,
                "word_start_timestamp": start,
                "word_end_timestamp": end,
                "word_text": word,
            }
        )

    with Prisma() as db:
        db.word.create_many(data=words_to_insert)
        db.sentence.create_many(data=sentences_to_insert)


def mass_transcribe(
    input_folder_path: Path,
    model_size: model_sizes,
    language: language_codes | None = None,
) -> None:
    already_in_db = get_all_paths_already_in_db()
    for file_path in recurse_path(input_folder_path, depth=1):
        if file_path.as_posix() in already_in_db:
            continue
        logger.info(f"Started transcribing: {file_path.as_posix()}")
        result = transcribe_file(file_path, model_size=model_size, language=language)
        logger.info(f"Saving result to database: {file_path.as_posix()}")
        save_result_to_db(file_path, result)


if __name__ == "__main__":
    # Can be run with:
    # PYTHONPATH=$(pwd) poetry run python src/transcribe_file.py
    input_folder_path = Path(os.getenv("MASS_TRANSCRIBE_INPUT_DIRECTORY"))
    # mass_transcribe(input_folder_path, model_size="tiny", language="de")
    mass_transcribe(input_folder_path, model_size="medium", language="de")

    # subtitle_path = audio_file_path.parent / f"{audio_file_path.stem}.srt"

    # result = transcribe_file(audio_file_path, model_size="small", language="de")
    # # save_result_to_db(audio_file_path, result)
    # data = get_srt_content(result)
    # subtitle_path.write_text(data.getvalue().decode())
