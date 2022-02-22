import venv
import tempfile
import subprocess
import sys

if __name__=="__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        venv.create(tmpdir, with_pip=True)
        subprocess.run([tmpdir + "/bin/pip", "--disable-pip-version-check",
                        "install", "pyfiglet"],
                       stdout=subprocess.DEVNULL)
        subprocess.run(["python3.9", "-m", "figdate"] + sys.argv[1:])