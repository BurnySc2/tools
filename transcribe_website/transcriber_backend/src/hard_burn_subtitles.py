import subprocess
from pathlib import Path


def hard_burn_subtitles(input_video_path: Path, input_subtitle_srt_path: Path, output_video_path: Path) -> None:
    # TODO Do I have to specify video codec?
    # ffmpeg -i input.wmv -vf "subtitles=sub.srt" -c:v libx264-crf 20 -c:a aac -b:a 192k output.mp4
    command = [
        "ffmpeg",
        "-i",
        input_video_path.as_posix(),
        "-crf",  # Lossless, try to get the same quality as input
        "23",
        "-acodec",
        "copy",
        "-vf",
        f"subtitles={input_subtitle_srt_path.as_posix()}",
        "-y",
        output_video_path.as_posix(),
    ]
    process = subprocess.Popen(command)
    process.communicate()


if __name__ == "__main__":
    input_path = Path("my_file.mp4")
    subtitle_path = input_path.parent / f"{input_path.stem}.srt"
    output_path = input_path.parent / f"{input_path.stem}_with_subs.mp4"

    hard_burn_subtitles(input_path, subtitle_path, output_path)
