from importlib.metadata import version
from importlib.util import find_spec
from pathlib import Path
import subprocess
import requests

try:
    from IPython.display import display, HTML, Javascript
    from IPython import get_ipython

except ImportError:
    ipychk = False

else:
    ipy = get_ipython()
    ipychk = ipy is not None


def display_progress(value):
    if value is None:
        js = """
const bar = document.getElementById('bar');
const container = document.getElementById('container');
const status = document.getElementById('status');
status.textContent = 'Restarting Session';
let value = 90;

function updateProgress() {
    value += 0.1;
    bar.value = value;
    if (value < 100) {
        setTimeout(updateProgress, 40);
    } else {
        setTimeout(() => {
            container.style.display = 'none';
        }, 1000);
    }
}

updateProgress();
"""
        display(Javascript(js))
    else:
        html = """
<div id="container" style="font-size:18px">
  <p id="status">Installing Manim</p>
  <progress id="bar" value="0" max="100"
  style="width: 25%; accent-color: #41FDFE;"></progress>
</div>
"""
        js = f"""
const bar = document.getElementById('bar');
let value = 0;

function updateProgress() {{
    value += 0.1;
    bar.value = value;
    if (value < 90) setTimeout(updateProgress, {value});
}}

updateProgress();
"""
        display(HTML(html))
        display(Javascript(js))


def add_file(url, filename):
    path = Path(filename)
    if not path.exists() and (response := requests.get(url)).ok:
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
        vnum = version("manim")
        info = f"Manim – Mathematical Animation Framework (Version {vnum})"
    print(info)


def setup(name, lite=False):
    cmd = []

    if check_package("libpango1.0-dev"):
        cmd.append(("apt-get", "-qq", "install", "-y", "libpango1.0-dev"))

    if check_package("manim"):
        cmd.append(("uv", "pip", "install", "-q", name))

    if not lite and check_package("texlive"):
        latex_pkg = (
            "texlive",
            "texlive-latex-extra",
            "texlive-science",
            "texlive-fonts-extra",
        )
        for pkg in latex_pkg:
            cmd.append(("apt-get", "-qq", "install", "-y", pkg))

    if cmd:
        if ipychk:
            display_progress(30) if lite else display_progress(240)

        # add STIX font (stixfonts.org)
        add_file(
            "https://raw.githubusercontent.com/stipub/stixfonts/master/fonts/static_ttf/STIXTwoText-Regular.ttf",
            "/usr/share/fonts/truetype/stixfonts/STIXTwoText-Regular.ttf",
        )

        for c in cmd:
            if c[0] == "uv":
                stdout = subprocess.run(c, capture_output=True)
                if stdout.returncode != 0:
                    stdout = subprocess.run(c[1:], capture_output=True)
            else:
                stdout = subprocess.run(c, capture_output=True)

        print_manim()

        if ipychk:
            display_progress(None)
            stdout = ipy.kernel.do_shutdown(restart=True)

    else:
        print_manim()
