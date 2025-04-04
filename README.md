# Go_directory
Tree for moving around directories. fish, python.

Command to install:
```
git clone https://github.com/adeline2007/Go_directory
cd Go_directory
python -m venv myvenv
source myvenv/bin/activate.fish
pip install pyinstaller colorama
pyinstaller --onefile --name gd main.py    
sudo mv dist/gd /usr/local/bin/
sudo chmod +x /usr/local/bin/gd
```
