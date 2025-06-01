[![Mscene](https://mscene.curiouswalk.com/assets/banner.png)](https://mscene.curiouswalk.com)

# Mscene

A Python library for creating science animations with Manim in Google Colab. &#10024;&nbsp;[mscene.curiouswalk.com](https://mscene.curiouswalk.com)

Manim is an animation engine designed to program precise animations for science videos. Google Colab (Colaboratory) is a hosted Jupyter Notebook service that requires no setup and provides free access to computing resources, including GPUs and TPUs.

>The Manim Community Developers. Manim &mdash; Mathematical Animation Framework [Computer software].<br>[www.manim.community](https://www.manim.community)

## Quickstart

### Manim in Colab

Create a new Colab notebook at *[colab.new](https://colab.new)* and run the cells below.
```python
%pip install -q mscene
import mscene
%mscene -h
```
**Install Manim**
```python
%mscene -l manim
```
**Import Manim**
```python
from mscene.manim import *
```
**View Manim [Gallery](https://docs.manim.community/en/stable/examples.html)**
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

Plugins extend Manim with additional features.
```python
%mscene plugins
from mscene.plugins import *
```
**View Mscene [Plugins](https://mscene.curiouswalk.com/plugins)**
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
