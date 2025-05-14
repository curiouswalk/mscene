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
    pfx = "mscene"

else:
    ipy = get_ipython()
    if ipy is not None:
        ipychk = True
        pfx = "%mscene"
    else:
        ipychk = False
        pfx = "mscene"


def _htmljs(txt):
    if txt == "html":
        code = """<div id='container' style='font-size: 18px'>
<span>Installing Manim</span><br><progress id='bar' value='0' max='100' style='width: 25%; accent-color: #41FDFE;'></progress>
</div>"""
    elif txt == "null":
        code = """var container = document.getElementById('container');
var msg = container.querySelector('span');
var bar = document.getElementById('bar');
var value = 90;
msg.innerText = 'Restarting Session';
function updateProgress() {
    value += .1;
    bar.value = value;
    if (value < 100) {
        setTimeout(updateProgress, 40);
    }
    else {
        setTimeout(function() {
        container.style.display = 'none';
        }, 1000);
    }
}

updateProgress();"""
    else:
        code = """var bar = document.getElementById('bar');
var value = 0;
function updateProgress() {
    value += 0.1;
    bar.value = value;
    if (value < 90) {
        setTimeout(updateProgress, DELAY);
    }
}

updateProgress();"""
        code = code.replace("DELAY", txt)

    return code


def add_file(url, filename):
    path = Path(filename)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(url)
        if response.ok:
            path.write_bytes(response.content)


def check_pkg(pkg, pip=False):
    if pip:
        status = find_spec(pkg) == None
    else:
        cmd = ("dpkg", "-s", pkg)
        stdout = subprocess.run(cmd, capture_output=True)
        status = stdout.returncode != 0
    return status


def install_manim(manver, lite=False):
    cmd = []

    if check_pkg("libpango1.0-dev"):
        cmd.append(("apt-get", "-qq", "install", "-y", "libpango1.0-dev"))

    if check_pkg("manim", pip=True):
        cmd.append(("uv", "pip", "install", "-q", manver))
        # cmd.append(("uv", "pip", "install", "-q", "IPython==8.21.0"))

    if not lite and check_pkg("texlive"):
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
            html = _htmljs("html")
            js = _htmljs("30") if lite else _htmljs("240")
            display(HTML(html))
            display(Javascript(js))

        add_file(
            "https://raw.githubusercontent.com/stipub/stixfonts/master/fonts/static_ttf/STIXTwoText-Regular.ttf",
            "/usr/share/fonts/truetype/stixfonts/STIXTwoText-Regular.ttf",
        )

        for c in cmd:
            if c[0] == "uv":
                stdout = subprocess.run(c, capture_output=True)
                if stdout.returncode != 0:
                    nc = ("pip", "install", "-q", c[-1])
                    stdout = subprocess.run(nc, capture_output=True)
            else:
                stdout = subprocess.run(c, capture_output=True)

        if check_pkg("manim", pip=True):
            info = (
                "Manim – Mathematical Animation Framework\nhttps://www.manim.community"
            )
        else:
            vnum = version("manim")
            info = f"Manim – Mathematical Animation Framework (Version {vnum})\nhttps://www.manim.community"

        print(info)

        if ipychk:
            js = _htmljs("null")
            display(Javascript(js))
            stdout = ipy.kernel.do_shutdown(restart=True)

    else:
        vnum = version("manim")
        info = f"Manim – Mathematical Animation Framework (Version {vnum})\nhttps://www.manim.community"
        print(info)


def add_scripts(source, path, filename):
    release = path / filename
    response = requests.get(f"{source}/{filename}")

    if response.ok:
        content = response.content

        if not release.exists() or release.read_bytes() != content:
            text = response.text.split()

            for name in text[1:]:
                res = requests.get(f"{source}/{name}.py")
                if res.ok:
                    script = path / f"{name}.py"
                    script.write_bytes(res.content)

            release.write_bytes(content)


def add_plugins():
    source = "https://raw.githubusercontent.com/curiouswalk/mscene/refs/heads/main/plugins/source"
    path = Path(__file__).parent
    add_scripts(source, path, "PLUGINS")


def check_manim(name):
    if name.startswith("manim"):
        name = name.replace("==", "/")
        status = requests.head(f"https://pypi.org/pypi/{name}/json").ok
    else:
        status = False
    return status


def check_scene(name):
    status = requests.head(
        f"https://raw.githubusercontent.com/curiouswalk/mscene/refs/heads/main/scenes/source/{name}.py"
    ).ok
    return status


def add_scenes(names):
    source = "https://raw.githubusercontent.com/curiouswalk/mscene/refs/heads/main/scenes/source"
    for name in names:
        script = Path(f"{name}.py")
        if not script.exists():
            script.write_bytes(requests.get(f"{source}/{name}.py").content)


def execute(args):

    if "-h" in args:
        info = f"""Usage: {pfx} <command>

Commands:
    manim                Install Manim with LaTeX
    -l manim             Install Manim without LaTeX
    manim==<ver>         Install specific Manim version
    plugins              Add or update plugins
    <scene_name>         Download scene script"""

        print(info)

    else:
        flags = {"-l": False, "plugins": False}
        manver = None
        scenes = []
        error = None

        for arg in args:
            if arg in flags:
                if not flags[arg]:
                    flags[arg] = True
                else:
                    error = True
                    break
            elif check_manim(arg):
                if not manver:
                    manver = arg
                else:
                    error = True
                    break
            elif check_scene(arg):
                scenes.append(arg)
            else:
                error = True
                break

        if flags["-l"] and not manver:
            error = True

        if error is None:
            if flags["plugins"]:
                add_plugins()

            if scenes:
                add_scenes(scenes)

            if manver:
                install_manim(manver, flags["-l"])
            else:
                print("Mscene — Science Animation\nhttps://mscene.curiouswalk.com")

        else:
            print(f"Error: Invalid command\nRun '{pfx} -h' to view usage")