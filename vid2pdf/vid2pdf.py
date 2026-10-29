import os
import shutil
import sys
import tempfile
from pathlib import Path

import typer
from PIL import Image
from dotenv import load_dotenv
from ffmpy import FFmpeg
from tqdm import tqdm

from vid2pdf.dialog import prompt_for_file

load_dotenv()
UTIL_BASE = Path(__file__).parent.parent / "utils"
FFMPEG_PATH = Path(os.environ.get("FFMPEG_PATH", UTIL_BASE / "ffmpeg"))

CWD = Path()


vid2pdf_cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
)


@vid2pdf_cli.command()
def main_cli(
    source: Path | None = typer.Argument(None, dir_okay=False, exists=True, help="Source video"),
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

    ffmpeg_path = _get_ffmpeg_exe()
    if not ffmpeg_path:
        raise FileNotFoundError(
            f"Could not find ffmpeg executable. Please add to: '{FFMPEG_PATH}' or your PATH"
        )

    if not dest:
        dest = source.parent
    dest.mkdir(parents=True, exist_ok=True)

    # Dump frames to a uniquely named temp directory alongside the output, so we can't collide with
    # existing files & the frames are cleaned up even if conversion fails
    with tempfile.TemporaryDirectory(prefix=".vid2pdf-frames-", dir=dest) as tmp:
        frames_dir = Path(tmp)
        _execffmpeg(ffmpeg_path, source, frames_dir, start, end)
        imgseries2pdf(input_dir=frames_dir, output_dir=dest, pdf_filename=source.stem)


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
    im = [Image.open(img) for img in tqdm(imgseries)]

    print("Generating PDF ... ", end="")
    out_filepath = output_dir / f"{pdf_filename}.pdf"
    try:
        im[0].save(out_filepath, "PDF", resolution=100.0, save_all=True, append_images=im[1:])
        print("done")
    finally:
        # Explicitly release file handles so the source images can be removed (needed on Windows)
        for img in im:
            img.close()


def _get_ffmpeg_exe(startdir: Path = FFMPEG_PATH) -> Path | None:
    """
    Locate an FFmpeg executable, starting from `startdir`.

    The following locations are checked, in order:
        1. `startdir` itself, if it points directly to a file
        2. A recursive search below `startdir`
        3. The system's `PATH`

    NOTE: On Windows, `ffmpeg.exe` is searched for. On unix-likes, `ffmpeg` is searched for instead.
    This search is case-sensitive on case-sensitive operating systems (i.e. not-Windows)

    NOTE: If multiple executables are found below the provided starting directory, the first
    executable encountered is returned.
    """
    if startdir.is_file():
        return startdir

    if sys.platform == "win32":
        pattern = "**/ffmpeg.exe"
    else:
        pattern = "**/ffmpeg"

    ffmpeg_exe = [filepath for filepath in startdir.glob(pattern) if filepath.is_file()]

    if ffmpeg_exe:
        return ffmpeg_exe[0]

    on_path = shutil.which("ffmpeg")
    if on_path:
        return Path(on_path)

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


if __name__ == "__main__":
    vid2pdf_cli()
