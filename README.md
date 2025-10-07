# PostScript Interpreter - Mini Project
This project implements a subset of a PostScript interpreter in Python, supporting
dynamic scoping by default with an option to toggle to lexical scoping.
## Requirements
* Python 3.6 or higher
## How to Build and Run
1. Ensure you have Python 3.6 or higher installed.
2. Navigate to the project directory in your terminal.
3. Run the interpreter using the command:
```bash
python psip.py
```
4. The interpreter will start in REPL mode. Type PostScript commands and press
Enter to execute them. Type `quit` to exit the REPL.
## Scoping
The interpreter uses dynamic scoping by default.
To enable lexical (static) scoping, you need to modify the `lexical_scoping` flag
in the `psip.py` file. Locate the line `lexical_scoping = False` and change it to
`lexical_scoping = True`.
```python
lexical_scoping = True # Change to True for lexical scoping
```
Save the file and re-run the interpreter.
## Implemented Commands
The interpreter supports the following command groups:
* Stack Manipulation (e.g., `exch`, `pop`, `copy`, `dup`, `clear`, `count`)
* Arithmetic Operations (e.g., `add`, `sub`, `mul`, `div`, `mod`)
* Dictionary Operations (e.g., `dict`, `length`, `begin`, `end`, `def`)
* String Operations (e.g., `length`, `get`, `getinterval`, `putinterval`) -
*Note: String operations might require further implementation based on the specific
subset document.*
* Boolean Operations (e.g., `eq`, `ne`, `gt`, `lt`, `and`, `or`, `not`)
* Flow Control (e.g., `if`, `ifelse`, `for`, `repeat`, `quit`) - *Note: `for` and
`repeat` might require further implementation.*
* Input/Output Operations (e.g., `print`, `=`, `==`)
## Automated Tests
Automated tests are included in the `test_psip.py` file. To run the tests, make
sure you have `pytest` installed (`pip install pytest`) and run the following
command in the project directory:
```bash
pytest
```
## Video Demonstration
## Melvin Sanare
