import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import click
from ffmpy import FFmpeg
from PIL import Image
from tqdm import tqdm


def main_cli(input_video: Path = None):
    """
    Main CLI interface. Prompts user on the command line for the necessary inputs
    """
    if not input_video:
        input_video = Path(click.prompt("Enter the video file path"))

    default_output_dir = input_video.parent
    output_dir = Path(
        click.prompt("Enter the output directory path", default=default_output_dir)
    )

    # Have to set default to "" over None in order for it to accept a blank input
    start_time = click.prompt(
        "Enter start time (hh:mm:ss.sss). Leave blank to use the video start",
        default="",
        show_default=False,
    )
    if len(start_time) == 0:
        start_time = None

    end_time = click.prompt(
        "Enter end time (hh:mm:ss.sss). Leave blank to use the video end",
        default="",
        show_default=False,
    )
    if len(end_time) == 0:
        end_time = None

    # Create a separate directory for the frames
    frames_dir = output_dir / "frames"
    if not frames_dir.exists():
        frames_dir.mkdir(exist_ok=True)
    _execffmpeg(_get_ffmpeg_exe(), input_video, frames_dir, start_time, end_time)

    imgseries2pdf(frames_dir, output_dir)


def imgseries2pdf(
    input_dir: Path,
    output_dir: Path = None,
    pdf_filename: str = "frames",
    image_format: str = "*.png",
):
    """
    Convert a series of images from input_dir to a PDF.

    If no output_dir is specified, the PDF is exported to input_dir
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


def _get_ffmpeg_exe(startdir: Path = Path("./utils/ffmpeg")) -> Path:
    """
    Recursively search startdir for the project's ffmpeg.exe

    Returns a pathlib.Path object if ffmpeg.exe is found. If multiple executables
    are found, the first is returned
    """
    pattern = "**/ffmpeg.exe"
    ffmpeg_exe = list(startdir.glob(pattern))

    if ffmpeg_exe:
        return ffmpeg_exe[0]
    else:
        return None


def _execffmpeg(
    ffmpeg_exe: Path,
    input_video: Path,
    output_dir: Path,
    start_time: str = None,
    end_time: str = None,
):
    """
    Execute ffmpeg with the specified inputs
    """
    global_options = ["-hide_banner"]
    if start_time:
        global_options.append(f"-ss {start_time}")

    if end_time:
        global_options.append(f"-to {end_time}")

    inputs = {str(input_video.resolve()): None}
    outputs = {str((output_dir / "frame%05d.png").resolve()): None}

    ff = FFmpeg(
        str(ffmpeg_exe.resolve()),
        global_options=global_options,
        inputs=inputs,
        outputs=outputs,
    )
    ff.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Main CLI interface w/CLI prompt for input video
        if sys.argv[1].lower() == "-cli":
            main_cli()
        else:
            raise NotImplementedError
    else:
        # Generate a Tk file selection dialog to select the input video file
        # Pass this path into main_cli()
        root = tk.Tk()
        root.withdraw()

        input_video = Path(filedialog.askopenfilename(title="Select Video File"))
        main_cli(input_video)
