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
Notes: the given data were already processed and output into `./processed_data/`. Delete one random file if you want to test the code.

To process more data, add the files to `./data` and run the following command:

```bash
  python init.py
```

To start asking questions, run the following command:

```bash
  python chat.py
```

