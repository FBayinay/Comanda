import subprocess
import sys

def main():
    try:
        result = subprocess.run([sys.executable, '-m', 'comanda.run'], check=True)
        print(f"Process finished with return code {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
