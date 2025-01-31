<div align="center">
  <a href="https://mscene.curiouswalk.com" target="_blank"><img src="https://mscene.curiouswalk.com/assets/mscene_banner.png" alt="Mscene"/><a/>
  <div>
    <a href="https://github.com/curiouswalk/mscene" target="_blank"><img src="https://img.shields.io/badge/GitHub-white?style=plastic&logo=github&logoColor=white&labelColor=grey" alt="GitHub" height="21"/></a>&emsp;
    <a href="https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/colab/mscene.ipynb" target="_blank"><img src="https://img.shields.io/badge/Colab-white?style=plastic&logo=googlecolab&logoColor=%23F9AB00&labelColor=grey" alt="Colab" height="21"/></a>&emsp;
    <a href="https://pypi.org/project/mscene" target="_blank"><img src="https://img.shields.io/badge/PyPI-white?style=plastic&logo=pypi&logoColor=%23448ee4&labelColor=grey" alt="PyPI" height="21"/></a>
  </div>
  <strong><a href="https://mscene.curiouswalk.com" target="_blank">mscene.curiouswalk.com</a></strong>
</div>

# Mscene

A Python library for programming animation scenes with Manim in Google Colab to create science videos directly in the browser.

Manim is an animation engine designed to program precise animations for science videos.<br>Google Colab (Colaboratory) is a hosted Jupyter Notebook service that requires no setup and provides free access to computing resources, including GPUs and TPUs.
>The Manim Community Developers. *Manim &mdash; Mathematical Animation Framework* [Computer software].<br>[www.manim.community](https://www.manim.community)

<a href="https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/colab/mscene.ipynb"><img align="center" src="https://colab.research.google.com/assets/colab-badge.svg"></a>&ensp;[mscene.curiouswalk.com/colab](https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/colab/mscene.ipynb)

## Program Animations Online

### Manim in Colab

#### Open Google [Colab](https://colab.research.google.com)
Create a new notebook: [colab.new](https://colab.new).
#### Install Mscene
```
%pip install mscene
```
#### Import Mscene
```
import mscene
```
#### View Commands
```
%mscene -h
```
#### Install Manim
```
%mscene -l manim
```
#### View Manim [Gallery](https://docs.manim.community/en/stable/examples.html)

```python
%%manim -qm ExampleScene
class ExampleScene(Scene):
    def construct(self):
        banner = ManimBanner()
        self.play(banner.create())
        self.play(banner.expand())
        self.wait(1.5)
```

### Mscene Plugins

Plugins enhance the features of Manim.

#### Add Plugins
```
%mscene plugins
```
#### Import Plugins
```
from mscene.plugins import *
```
#### View Mscene [Plugins](https://mscene.curiouswalk.com/plugins)

```python
%%manim -qm FractalScene
class FractalScene(Scene):
    def construct(self):
        ks = KochSnowflake(level=2)
        self.add(ks)
        self.play(ks.animate.next_level())
        self.wait(1.5)
        self.play(ks.animate.prev_level())
        self.wait(1.5)
```
---
