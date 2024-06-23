## About
Un outil permettant de switcher automatiquement sur un personnage à qui le combat est le tour.

Capture en tant réel l'écran et analyse le texte pour savoir si il s'agit du tour d'un personnage spécifique

## Requirement

You need to have Tesseract install on your system to use this script. 

Here the github link to install it on Windows : https://github.com/UB-Mannheim/tesseract/wiki

For Linux, you can install the package ```tesseract-ocr``` depend on your distribution.

## Installation on Windows

```bash
python -m venv venv
.\venv\Script\activate.bat
pip install -r requirements.txt
```

## Installation on linux

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python find.py [your list of characters to detect]
#For example
python find.py Floup-Iop Old-Man 
```

In the example, it will so looking for the characters Floup-Io, and Old-Man , then the program will exit when finding.

## Compile the program to .exe

```bash
pip install pyinstaller
pyinstaller --onefile find.py
```

Be aware that the file will be around 60 mo.
