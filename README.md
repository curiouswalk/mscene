[![Mscene](https://mscene.curiouswalk.com/assets/banner.png)](https://mscene.curiouswalk.com)

# Mscene

A Python library for creating science animation with Manim in Google Colab. &#10024;&nbsp;[mscene.curiouswalk.com](https://mscene.curiouswalk.com)

>[Manim](https://www.manim.community) is an animation engine designed to program precise animations for science videos. Google [Colab](https://colab.google) is a hosted Jupyter Notebook service that requires no setup and provides free access to computing resources, including GPUs and TPUs.

## Quickstart

### Manim in Colab

Visit [*colab.new*](https://colab.new) to create a new Colab notebook.

**Installation**
```python
%pip install -q mscene
import mscene
%mscene -l manim
```
```python
from mscene.manim import *
```
**Example Scene**
```python
%%manim -qm ManimScene

class ManimScene(Scene):
    def construct(self):
        banner = ManimBanner()
        self.play(banner.create())
        self.play(banner.expand())
        self.wait(1.5)
```

### Mscene Plugins

Plugins extend Manim with additional features.

**Adding Plugins**
```python
import mscene
%mscene plugins
```
```python
from mscene.plugins import *
```
**Example Scene**
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
