"""'%run mscene -h' — view commands"""

import sys
from IPython import get_ipython
from IPython.display import clear_output


def install_manim(lite=False):

    if lite:
        packages = ["libcairo2-dev", "libpango1.0-dev", "ffmpeg"]
    else:
        packages = [
            "libcairo2-dev",
            "libpango1.0-dev",
            "ffmpeg",
            "texlive",
            "texlive-latex-extra",
            "texlive-science",
            "texlive-fonts-extra",
        ]

    # [optional font] STIX Two Text (stixfonts.org)
    font_url = "https://raw.githubusercontent.com/stipub/stixfonts/master/fonts/static_ttf/STIXTwoText-Regular.ttf"
    get_font_cmd = "wget -P /usr/share/fonts/truetype " + font_url

    ipy = get_ipython()

    ipy.system("sudo apt update")
    clear_output()

    for pkg in packages:
        cmd = "sudo apt install " + pkg
        ipy.system(cmd)
        clear_output()

    ipy.system(get_font_cmd)
    clear_output()

    ipy.system("pip install manim")
    clear_output()

    # restart session
    ipy.kernel.do_shutdown(restart=True)
    clear_output()

    print("Installation Complete")


def setup_manim():

    config.disable_caching = True
    config.verbosity = "WARNING"
    config.media_width = "75%"
    config.media_embed = True

    Text.set_default(font="STIX Two Text")

    info = f"Manim – Mathematical Animation Framework (Version {version('manim')})\nSetup Complete"
    print(info)


if __name__ == "__main__":

    args = sys.argv[1:]

    if "setup" in args and len(args) == 1:

        from manim import *

        setup_manim()

    elif "install" in args and len(args) == 1:

        install_manim()

    elif all(i in args for i in ("-l", "install")) and len(args) == 2:

        install_manim(lite=True)

    elif "-h" in args and len(args) == 1:

        cmd_info = "Commands\n--------\n'%run mscene install' — install Manim\n'%run mscene -l install' — install Manim without LaTeX\n'%run mscene setup' — import and configure Manim\n'%run mscene -h' — view commands"
        print(cmd_info)

    else:

        err_msg = "Invalid Command\n'%run mscene -h' — view commands"
        print(err_msg)
