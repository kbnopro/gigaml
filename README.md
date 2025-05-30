# Take home project for the position of Software Engineer at GigaMl

## 1. How to start

Create a virtual environment

```bash
  python -m venv <venv>
```

Grab a command for you shell to start the virtual environment [here](https://docs.python.org/3/library/venv.html#how-venvs-work).
Note: The default shell on macOS is `zsh`, so you can use the command `source <venv>/bin/activate`.

Install the requirements

```bash
  pip install -r requirements.txt
```

Grab an environment variable file and rename it to `.env`.

Create a data folder at `./data/` then put all the PDF files there.

Notes: the given data were already processed and output into `./processed_data/`.
Delete one random file if you want to test the code.

To process more data, add the files to `./data` and run the following command:

```bash
  python init.py
```

To start asking questions, run the following command:

```bash
  python chat.py
```

## 2. Current limitations

### Caching problem

There seems to be a delay between cache creation and cache usage. If you run the code for the first time after adding data, changing prompt, it will take a while to process the data and create the cache. However, if you run it again immediately after, it may fail due to rate limit. If this is encountered, wait a minute and run again.

### Aggregation, ranking behavior

Aggregation, ranking is currently handled by listing all related data points and then aggregate. This appears to be good behavior, improving both UX and model performance. However, some manual works are required to handle more case of aggregation.

### Regarding data handling

The data is parsed base on general properties of the PDF files. It is not guaranteed that all data will be parsed correctly.

The data is processed by AI, so the performance can be slow. Given more time, a different strategy can be used to improve the performance, such as using bounding box + PDF parser library.
