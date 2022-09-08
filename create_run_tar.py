
import sys
import os
path = os.path.dirname(__file__)
path = os.path.join(path, "PythonTutor")
path = os.path.join(path, "v5-unity")
sys.path.append(path)
import create_exe

import zipfile


if __name__ == "__main__":
    create_exe.main()

    prepath = "PythonTutor/v5-unity"
    files = "/bottle_server.exe  /visualize.html /build/visualize.bundle.js /favicon.ico /web_exec_py3.py /viz_interaction.py"
    mainfiles = "StepData.py VarDumps.py demo.py"

    zf = zipfile.ZipFile("run.zip", "w")

    sp = files.split()
    for onefile in sp:
        file_path = prepath + "/" + onefile
        zf.write(file_path)
    for onefile in mainfiles.split():
        zf.write(onefile)
