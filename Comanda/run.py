# run.py
import sys
import os

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    #from visualization import visualization
    from login import login_ui
    #visualization.main()
    login_ui.main()
