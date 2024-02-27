import glob
import os

if __name__ == "__main__":
    for g96_file in sorted(glob.glob("*.g96")):
        os.system(f"gmx trjconv -f {g96_file} -o {g96_file.replace('.g96', '.xtc')}")
        os.system(f"gmx trjconv -f {g96_file} -o {g96_file.replace('.g96', '.trr')}")

    os.system("rm -rf \#*")
