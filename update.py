import os

SEP = os.sep


def main():
    run_updates()


def run_updates():
    _ver3 = set_for_unix()

    print("\nUpdating PIP...")
    os.system(f"python{_ver3} -m pip install --upgrade pip")

    print("\nInstalling Python Environment...")
    os.system(f"python{_ver3} -m pip install pipenv")

    print("\nSetting a new Python Environment...")
    os.system(f"python{_ver3} -m virtualenv venv")

    print("\nUpdating all packages and resources...")
    os.system(f"python{_ver3} -m pip install -r requirements.txt")
    os.system(f"python{_ver3} -m pip install -U black")
    os.system(f"python{_ver3} -m pip install -U rope")

    print("\nPackages installed:")
    os.system(f"python{_ver3} -m pip list")


def set_for_unix():
    if os.name != "nt":
        return "3"


class Update:
    if __name__ == "__main__":
        main()
