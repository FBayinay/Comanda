# run.py
import sys
import os

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    from comanda.login.login_ui import main as login_main
    login_main()
