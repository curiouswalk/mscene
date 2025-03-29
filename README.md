[![Mscene](https://mscene.curiouswalk.com/assets/github_banner.png)](https://mscene.curiouswalk.com)

# Mscene

A Python library for programming animation scenes with Manim in Google Colab to create science videos directly in the browser. &#10024;&nbsp;[mscene.curiouswalk.com](https://mscene.curiouswalk.com)

Manim is an animation engine designed to program precise animations for science videos. Google Colab (Colaboratory) is a hosted Jupyter Notebook service that requires no setup and provides free access to computing resources, including GPUs and TPUs.

> [!NOTE] 
>The Manim Community Developers. *Manim &mdash; Mathematical Animation Framework* [Computer software].<br>[www.manim.community](https://www.manim.community)

<a href="https://mscene.curiouswalk.com/colab"><img align="center" height="24" src="https://img.shields.io/badge/Colab-silver?logo=googlecolab&labelColor=grey"></a>&emsp;<a href="https://mscene.curiouswalk.com/docs"><img align="center" height="24" src="https://img.shields.io/badge/Docs-silver?logo=readthedocs&logoColor=blue&labelColor=grey"></a>

## Quick Start

### Manim in Colab

Create a new Colab notebook at *[colab.new](https://colab.new)* and run the cells below.

**Install & Import Mscene**
```python
%pip install mscene
import mscene
```
**View Commands**
```python
%mscene -h
```
**Install & Import Manim**
```python
%mscene -l manim
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

**Add & Import Plugins**

```python
%mscene plugins
```

**View Mscene [Plugins](https://mscene.curiouswalk.com/plugins)**

```python
%%manim -qm FractalScene
class FractalScene(Scene):
    def construct(self):
        ks = KochSnowflake(2)
        self.add(ks)
        self.play(ks.animate.next_level())
        self.wait(1)
        self.play(ks.animate.prev_level())
        self.wait(1)
```
---
