<p align="center" width="100%">
<img width="200" src="https://raw.githubusercontent.com/sco1/vid2pdf/refs/heads/main/assets/icon/app_icon.png">
</p>
<h1 align="center"> vid2pdf </h1>

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vid2pdf/1.2.0?logo=python&logoColor=FFD43B)](https://pypi.org/project/vid2pdf/)
[![PyPI](https://img.shields.io/pypi/v/vid2pdf?logo=Python&logoColor=FFD43B)](https://pypi.org/project/vid2pdf/)
[![PyPI - License](https://img.shields.io/pypi/l/vid2pdf?color=magenta)](https://github.com/sco1/vid2pdf/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/vid2pdf/main.svg)](https://results.pre-commit.ci/latest/github/sco1/vid2pdf/main)

Convert a video file into PDF image series.

## External Requirements
`vid2pdf` requires ffmpeg to be extracted to the `/utils/ffmpeg` folder. The latest version of ffmpeg can be downloaded from [ffmpeg.org](https://www.ffmpeg.org/download.html).

The path to an existing ffmpeg installation can also be specified using an `FFMPEG_PATH` environment variable, either directly or by utilizing a `.env` file in this project's root.

## Installation
### Python
Install from PyPi with your favorite `pip` invocation:

```bash
$ pip install vid2pdf
```

You can confirm proper installation via the `vid2pdf` CLI:
<!-- [[[cog
import cog
from subprocess import PIPE, run
out = run(["vid2pdf", "--help"], stdout=PIPE, encoding="ascii")
cog.out(
    f"```\n$ vid2pdf --help\n{out.stdout.rstrip()}\n```"
)
]]] -->
```
$ vid2pdf --help
Usage: vid2pdf [OPTIONS] [SOURCE]

  Convert a video file to PDF image series.

  If an input video is not specified, a file selection dialog will be opened
  to select the file to process.

  Start and end arguments may be left empty to use the start and end of the
  video, respectively.

Arguments:
  [SOURCE]  Source video

Options:
  --dest DIRECTORY  Destination directory
  -s, --start TEXT  Start time (hh:mm:ss.sss)
  -e, --end TEXT    End time (hh:mm:ss.sss)
  --help            Show this message and exit.
```
<!-- [[[end]]] -->

### Standalone
Standalone distribution using [Nuitka](https://github.com/Nuitka/Nuitka) is tested by this package. Due to the likelihood of false positives by AV scanners, prebuilt releases are not currently provided.

Note that Nuitka is provided as an optional dependency and can be installed by specifying the `build` dependency group when installing this project.

Currently tested packaging paths are:
  * `python -m nuitka ./vid2pdf/vid2pdf.py --mode=standalone --enable-plugin=tk-inter`
  * `python -m nuitka ./vid2pdf/vid2pdf.py --mode=onefile --enable-plugin=tk-inter`

For an alternative standalone option, I also maintain a UI-based Flutter version of `vid2pdf` at [sco1/vid2pdf-flutter](https://github.com/sco1/vid2pdf-flutter)
