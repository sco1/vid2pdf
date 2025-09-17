import os
import sys
from collections import deque
from pathlib import Path

import typer
from PIL import Image
from dotenv import load_dotenv
from ffmpy import FFmpeg
from tqdm import tqdm

from vid2pdf.dialog import prompt_for_file

load_dotenv()
UTIL_BASE = Path(__file__).parent / "utils"
FFMPEG_PATH = Path(os.environ.get("FFMPEG_PATH", UTIL_BASE / "ffmpeg"))

CWD = Path()


vid2pdf_cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
)


@vid2pdf_cli.command()
def main_cli(
    source: Path | None = typer.Argument(None, dir_okay=False, help="Source video"),
    dest: Path | None = typer.Option(None, file_okay=False, help="Destination directory"),
    start: str | None = typer.Option(None, "-s", "--start", help="Start time (hh:mm:ss.sss)"),
    end: str | None = typer.Option(None, "-e", "--end", help="End time (hh:mm:ss.sss)"),
) -> None:
    """
    Convert a video file to PDF image series.

    If an input video is not specified, a file selection dialog will be opened to select the file to
    process.

    Start and end arguments may be left empty to use the start and end of the video, respectively.
    """
    if not source:
        source = prompt_for_file("Select Source Video File")

    # Create a separate directory for the frames
    if not dest:
        dest = source.parent

    frames_dir = dest / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = _get_ffmpeg_exe()
    if not ffmpeg_path:
        raise FileNotFoundError(f"Could not find ffmpeg executable. Please add to: '{FFMPEG_PATH}'")

    _execffmpeg(ffmpeg_path, source, frames_dir, start, end)
    imgseries2pdf(input_dir=frames_dir, output_dir=dest, pdf_filename=source.stem)
    _cleandir(frames_dir)


def imgseries2pdf(
    input_dir: Path,
    output_dir: Path,
    pdf_filename: str = "frames",
    image_format: str = "*.png",
) -> None:
    """
    Convert a series of images from `input_dir` to a PDF in the specified output directory.

    If no `output_dir` is specified, the PDF is exported to `input_dir`
    """
    imgseries = sorted(input_dir.glob(image_format))

    print(f"Loading {len(imgseries)} frames...")
    im = []
    baseim = Image.open(imgseries[0])
    for img in tqdm(imgseries[1:]):
        im.append(Image.open(img))

    print("Generating PDF ... ", end="")
    out_filepath = output_dir / f"{pdf_filename}.pdf"
    baseim.save(out_filepath, "PDF", resolution=100.0, save_all=True, append_images=im)
    print("done")


def _get_ffmpeg_exe(startdir: Path = FFMPEG_PATH) -> Path | None:
    """
    Recursively search, starting from `startdir`, for the project's FFmpeg executable.

    NOTE: On Windows, `ffmpeg.exe` is searched for. On unix-likes, `ffmpeg` is searched for instead.
    This search is case-sensitive on case-sensitive operating systems (i.e. not-Windows)

    NOTE: If multiple executables are found below the provided starting directory, the first
    executable encountered is returned.
    """
    if sys.platform == "win32":
        pattern = "**/ffmpeg.exe"
    else:
        pattern = "**/ffmpeg"

    ffmpeg_exe = [filepath for filepath in startdir.glob(pattern) if filepath.is_file()]

    if ffmpeg_exe:
        return ffmpeg_exe[0]
    else:
        return None


def _execffmpeg(
    ffmpeg_exe: Path,
    source: Path,
    output_dir: Path,
    start_time: str | None = None,
    end_time: str | None = None,
) -> None:
    """Execute ffmpeg with the specified inputs."""
    global_options = ["-hide_banner"]
    if start_time:
        global_options.append(f"-ss {start_time}")

    if end_time:
        global_options.append(f"-to {end_time}")

    inputs = {str(source.resolve()): None}
    outputs = {str((output_dir / r"frame%05d.png").resolve()): None}

    ff = FFmpeg(
        str(ffmpeg_exe.resolve()), global_options=global_options, inputs=inputs, outputs=outputs
    )
    ff.run()


def _cleandir(root_directory: Path) -> None:
    """Recursively remove all files and subfolders in `root_directory`."""
    dir_queue: deque[Path] = deque()  # Queue directories since we can't delete them if non-empty
    for item in root_directory.rglob("*"):
        if item.is_dir():
            dir_queue.append(item)
        else:
            item.unlink()

    for item in dir_queue:
        item.rmdir()

    root_directory.rmdir()


if __name__ == "__main__":
    vid2pdf_cli()
