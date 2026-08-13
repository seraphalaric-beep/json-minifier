# JSON Minifier

A small, local-first desktop utility for validating and minifying JSON.

JSON is parsed and processed on your own computer. There is no web service, account or external dependency involved.

## Features

- Paste JSON directly into the editor.
- Open an existing `.json` file.
- Validate and minify JSON using Python's standard library.
- Copy the compact result to the clipboard.
- Save the result as a new JSON file.
- Work offline with no third-party packages.

## Requirements

- Python 3.8 or newer.
- Tkinter, which is included with most standard Python installations.

## Run locally

```bash
python main.py
```

## Keyboard shortcuts

| Action | Shortcut |
| --- | --- |
| Minify JSON | `Ctrl+M` |
| Copy output | `Ctrl+C` |
| Save output | `Ctrl+S` |
| Open file | `Ctrl+O` |

## Privacy

The application does not send JSON anywhere. Files are opened and saved only when you choose a local file through the desktop interface.

## Project status

This is a deliberately small utility project and is not distributed as a signed installer. It is intended for local use and as a clear example of a lightweight Python desktop application.

## Licence

No open-source licence has been applied yet. Until one is added, the source remains available for viewing but should not be redistributed or incorporated into another project without permission.
