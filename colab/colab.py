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


def display_progress(value):
    html = f"""
<div style='font-size:18px'>
  <p>Installing Manim</p>
  <progress id='bar' value='0' max='100'
    style='width: 25%; accent-color: #41FDFE;'></progress>
</div>

<script>
const bar = document.getElementById('bar');
const updateProgress = () => bar.value < 100 && (bar.value += 0.1, setTimeout(updateProgress, {value}));
updateProgress();
</script>
"""
    display(HTML(html))


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

        # add STIX font (stixfonts.org)
        add_file(
            "https://raw.githubusercontent.com/stipub/stixfonts/master/fonts/static_ttf/STIXTwoText-Regular.ttf",
            "/usr/share/fonts/truetype/stixfonts/STIXTwoText-Regular.ttf",
        )

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
