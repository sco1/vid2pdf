# vid2pdf
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vid2pdf/1.1.0?logo=python&logoColor=FFD43B)](https://pypi.org/project/vid2pdf/)
[![PyPI](https://img.shields.io/pypi/v/vid2pdf?logo=Python&logoColor=FFD43B)](https://pypi.org/project/vid2pdf/)
[![PyPI - License](https://img.shields.io/pypi/l/vid2pdf?color=magenta)](https://github.com/sco1/vid2pdf/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/vid2pdf/main.svg)](https://results.pre-commit.ci/latest/github/sco1/vid2pdf/main)

Simple helper utility to convert a video file to PDF image series

## External Requirements
`vid2pdf` requires ffmpeg to be extracted to the `/utils/ffmpeg` folder. The latest version of ffmpeg can be downloaded from [ffmpeg.org](https://www.ffmpeg.org/download.html). Existing local ffmpeg installations are not currently supported.

## Installation
Install from PyPi with your favorite `pip` invocation:

```bash
$ pip install vid2pdf
```

Alternatively, prebuilt binaries are provided at https://github.com/sco1/vid2pdf/releases

## Usage

`vid2pdf` can be invoked using Python:
```bash
$ python vid2pdf.py
```

Or, if a prebuilt binary is present, this may be called directly
```bash
$ vid2pdf.exe
```

### Input Parameters
Unless otherwise noted, all input parameters are prompted in the CLI
#### `input_video`
The default behavior is to open a GUI dialog for the user to specify a the input video file. An optional `-cli` flag may be passed to bypass this GUI and instead prompt for the video file path in the CLI.

#### `output_dir`
PDF output directory. If this value is not specified, this defaults to the parent directory of the input video.

#### `start_time`
Video start time for capture, as `hh:mm:ss.sss`. If this value is not specified, the beginning of the video is used.

#### `end_time`
Video end time for capture, as `hh:mm:ss.sss`. If this value is not specified, the end of the video is used.

### Examples

```bash
$ python vid2pdf.py
Enter the output directory path [X:\vid2pdf\test]:
Enter start time (hh:mm:ss.sss). Leave blank to use the video start:
Enter end time (hh:mm:ss.sss). Leave blank to use the video end: 00:00:01.000
<ffmpeg output snipped>
Loading 30 frames...
100%|███████████████████████████████████████| 29/29 [00:00<00:00, 852.82it/s]
Generating PDF ... done
```

```bash
$ python vid2pdf.py -cli
Enter the video file path: X:\vid2pdf\test\test_video.mp4
Enter the output directory path [X:\vid2pdf\test]:
Enter start time (hh:mm:ss.sss). Leave blank to use the video start:
Enter end time (hh:mm:ss.sss). Leave blank to use the video end: 00:00:01.000
<ffmpeg output snipped>
Loading 30 frames...
100%|███████████████████████████████████████| 29/29 [00:00<00:00, 852.82it/s]
Generating PDF ... done
```
