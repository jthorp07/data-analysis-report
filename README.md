# Reproducibility Instructions for Memorandum on Data Analysis of AI versus Human-Authored Text

This repository contains the scripts and data source files used when testing AI and human-authored essays to determine if any trivially identifiable statistics can be used to differentiate the two populations. The rest of this document will contain instructions to reproduce the tests conducted for the memorandum.

*Note: Any commands shown are to be executed in a terminal pointing to the root directory of this repository.*

## 1: Directory Setup

First, create the required directories where data will be placed:

### UNIX-like terminal

```bash
cd src && mkdir data && cd data && mkdir ai && mkdir human && mkdir batches
```

If you are not comfortable creating directories on the command line, you can also create directories/folders to make the repository match the following directory structure. Entries of the format `name/` are directories/folders named `name`, and subitems of a folder are files/folders inside that folder.

### Required Directory Structure:

- `~/`
    - `src/`
        - `data/`
            - `ai/`
            - `human/`
            - `batches/`
        - `essay_data.py`
        - `essay_reader.py`
        - `essay_stats.py`
        - `inference.py`
        - `opted_reader.py`
        - `word_frequency.py`
    - `essay_data.csv`
    - `OPTED-Dictionary.csv`
    - `word_frequency.txt`
    - `README.md` (Not required for calculations, but contains these instructions)

## 2. Data preparation:

Next, to prepare auxilary data thaat will be used later in the process, run the scripts `word_frequency.py` and `opted_reader.py`. Running these script will require Python 3:

### Terminl command:

```bash
cd src && py word_frequency.py && py opted_reader.py
```

After running these scripts, there should be 2 new .csv files in the data directory.

## 3. Parse essays:

Now the essays can be individually parsed through. This is done in the script `essay_reader.py`:

```bash
cd src && py essay_reader.py
```
*Note: This will take some time*

After this script finishes, the `src/data/ai/`, `src/data/human/`, and `src/data/batches/` directories should contain many .json files.

## 4. Run inference tests

The final step is running the inference tests as defined in `inference.py`. Running this will require the SciPy library. For instructions on how to install SciPy, go [here](https://scipy.org).

After SciPy is installed, run the script with the following:

```bash
cd src && py inference.py
```

This script will create the file `src/data/inference_results.json`. This file will contain the results shown in the memorandum. However, the sampling for the most populous stratifications randomly selects 5000 entries, so some variation should be expected.

