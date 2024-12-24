# Koch Curve

### Fractals: Koch Curve and Koch Snowflake

<a href="https://www.youtube.com/watch?v=fDGN3bGcXSg" target="_blank"><img align="left" width="50%" src="/docs/assets/fDGN3bGcXSg.jpeg"></a>

<p align="justify">In mathematics, the intriguing concept of self-similarity emerges, wherein an object bears resemblance, either entirety or partially, to a smaller iteration of itself. A remarkable illustration of this is the Koch Curve, showcasing the beauty of complexity inherent in self-similar geometric patterns. A fractal formed from the Koch Curve is the Koch Snowflake. It is created by repeatedly dividing each side of an equilateral triangle into three segments and replacing the middle segment with a smaller equilateral triangle.</p>

[Open in Colab]&ensp;[mscene.curiouswalk.com/colab/koch-curve](https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/koch-curve/koch-curve.ipynb)

### Contents
- [Setup](#setup)
- [Fractal](#fractal)
- [Koch Curve](##koch-curve)
- [Koch Snowflake](#koch-snowflake)
- [Koch Antisnowflake](#koch-antisnowflake)
- [Two Flakes](#two-flakes)
---

## Setup

[Manim in Colab]&ensp;[mscene.curiouswalk.com/colab](https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/colab/mscene.ipynb)

Download `mscene.py` from [mscene.curiouswalk.com/src/mscene.py](https://mscene.curiouswalk.com/src/mscene.py) and complete this setup process to get started.

```python
# download mscene.py; print working directory; list contents
!wget -nv mscene.curiouswalk.com/src/mscene.py; pwd; ls
```

```python
# install Manim without LaTeX
%run mscene -l install
```

```python
# import and configure Manim
%run mscene setup
```

## Fractal

Download `fractal.py` from [mscene.curiouswalk.com/src/fractal.py](https://mscene.curiouswalk.com/src/fractal.py) and import it.

```python
!wget -nv mscene.curiouswalk.com/src/fractal.py; pwd; ls
```

```python
from fractal import *
```

### Example Scene

**YouTube**: [Koch Curve: The Beauty of Fractal Geometry](https://www.youtube.com/watch?v=LD-S-7ZHgmI)

https://github.com/user-attachments/assets/866718b8-6b6d-46c8-a242-01b4cce7e0ce

```python
%%manim -qm ExampleScene
class ExampleScene(Scene):
    def construct(self):

        kc = KochCurve(level=2, stroke_width=6)

        self.add(kc)
        self.play(kc.animate.next_level())
        self.wait()
        self.play(kc.animate.prev_level())
        self.wait()

```

### Koch Curve

https://github.com/user-attachments/assets/a7e26fd8-82c8-4e3f-961e-97a7053bf418

```python
%%manim -qm KochCurveScene
class KochCurveScene(Scene):
    def construct(self):

        color = [ManimColor(hex) for hex in ("#0A68EF", "#0ADBEF", "#0A68EF")]

        kc = KochCurve(level=0, stroke_width=8, stroke_color=color)
        title = Text("Koch Curve\nLevel 0").to_corner(UL, buff=0.75)

        self.add(title, kc)

        for level in (1, 2, 3, 2, 1, 0):
            self.play(
                kc.animate(run_time=1.5).new_level(level, stroke_width=8 - level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()

```

### Koch Snowflake

https://github.com/user-attachments/assets/1ae611a4-ab83-4f1e-8d18-28d3357d3322

```python
%%manim -qm KochSnowflakeScene
class KochSnowflakeScene(Scene):
    def construct(self):

        color = [ManimColor(hex) for hex in ("#0ADBEF", "#0A68EF", "#1F0AEF")]

        ks = KochSnowflake(level=0, fill_color=color)
        title = Text("Koch Snowflake\nLevel 0").to_corner(UL, buff=0.75)

        self.add(title, ks)

        for level in (1, 2, 3, 2, 1, 0):
            self.play(
                ks.animate(run_time=1.5).new_level(level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()

```

### Koch Antisnowflake

https://github.com/user-attachments/assets/08ea8a0a-9927-4a48-881c-8394ead99e53

```python
%%manim -qm KochAntisnowflakeScene
class KochAntisnowflakeScene(Scene):
    def construct(self):

        color = [ManimColor(hex) for hex in ("#1F0AEF", "#0A68EF", "#0ADBEF")]

        ks = KochSnowflake(level=0, invert=True, fill_color=color)
        title = Text("Koch Anti-\nsnowflake\nLevel 0").to_corner(UL, buff=0.75)

        self.add(title, ks)

        for level in (1, 2, 3, 2, 1, 0):
            self.play(
                ks.animate(run_time=1.5).new_level(level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()

```

### Two Flakes

https://github.com/user-attachments/assets/7625347b-1265-4295-a68d-b4731c97314c

```python
%%manim -qm TwoFlakesScene
class TwoFlakesScene(Scene):
    def construct(self):

        ks1 = KochSnowflake(level=1, fill_color=ManimColor("#5d06e9"))
        ks2 = KochSnowflake(
            level=1, invert=True, fill_color=ManimColor("#9e0168")
        ).align_to(ks1, UP)

        self.add(ks1, ks2)

        for level in (2, 3, 2, 1):
            self.play(
                ks1.animate.new_level(level), ks2.animate.new_level(level), run_time=1.5
            )
            self.wait()

```
---
