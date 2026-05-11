from importlib.metadata import version
from importlib.util import find_spec
from pathlib import Path
import subprocess
import requests

try:
    from IPython.display import display, HTML, clear_output
    from IPython import get_ipython

except ImportError:
    ipychk = False

else:
    ipy = get_ipython()
    ipychk = ipy is not None


def display_progress(t):
    html = (
        '<style>.bar{width:25%;min-width:256px;height:8px;margin:.5em 0;border-radius:4px;background:#217f7f;overflow:hidden}'
        '.fill{height:100%;width:0%;background:#41fdfe;animation:load ' + str(float(t)) + 's linear forwards}'
        '@keyframes load{to{width:100%}}</style><p style="font-size:1.2rem">Manim Installation</p>'
        '<div class="bar"><div class="fill"></div></div>'
    )
    
    display(HTML(html))


def add_file(url, filename):
    path = Path(filename)
    if not path.is_file() and (response := requests.get(url)).ok:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)


def check_package(name):
    if name == "manim":
        status = find_spec(name) is None
    else:
        cmd = ("dpkg", "-s", name)
        stdout = subprocess.run(cmd, capture_output=True)
        status = stdout.returncode != 0
    return status


def print_manim():
    if check_package("manim"):
        info = "Manim – Mathematical Animation Framework"
    else:
        info = f"Manim – Mathematical Animation Framework (Version {version('manim')})"
    print(info)


def setup(name, lite=False):
    cmd = []
    pkg = []

    if not lite and check_package("texlive"):
        cmd.append(("apt-get", "-qq", "update"))
        pkg.extend(
            ("texlive", "texlive-latex-extra", "texlive-science", "texlive-fonts-extra")
        )

    if check_package("libpango1.0-dev"):
        pkg.append("libpango1.0-dev")

    if pkg:
        cmd.append(("apt-get", "-qq", "install", "-y", *pkg))

    if check_package("manim"):
        cmd.append(("uv", "pip", "install", "-q", name))

    if cmd:
        if ipychk:
            display_progress(30) if lite else display_progress(240)

        # add STIX fonts (www.tiro.com/fonts/stix-two)
        add_file(
            "https://raw.githubusercontent.com/curiouswalk/mscene/refs/heads/main/colab/fonts/stix2.zip",
            "/usr/share/fonts/opentype/stix2.zip",
        )
        cmd.append(("unzip", "-q", "-o", "/usr/share/fonts/opentype/stix2.zip", "-d", "/usr/share/fonts/opentype"))

        for c in cmd:
            result = subprocess.run(
                c, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if result.returncode != 0 and c[0] == "uv":
                subprocess.run(
                    c[1:], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

        if ipychk:
            clear_output()
            print_manim()
            stdout = ipy.kernel.do_shutdown(restart=True)

    else:
        print_manim()
