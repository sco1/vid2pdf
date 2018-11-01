from pathlib import Path

from ffmpy import FFmpeg


def get_ffmpeg_exe(startdir: Path = Path("./utils/ffmpeg")) -> Path:
    """
    Recursively search startdir for the project's ffmpeg.exe

    Returns a pathlib.Path object if ffmpeg.exe is found
    """
    pattern = "**/ffmpeg.exe"
    ffmpeg_exe = list(startdir.glob(pattern))

    if ffmpeg_exe:
        return ffmpeg_exe[0]
    else:
        return None


def execffmpeg(
    ffmpeg_exe: Path,
    input_video: Path,
    output_dir: Path,
    start_time: str = None,
    end_time: str = None,
):
    """
    Execute ffmpeg with the specified inputs
    """
    global_options = []
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
