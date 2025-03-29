# Roulette

A plugin for drawing roulette curves like cycloid, epicycloid, and hypocycloid by rolling a circle with markers plotting the curves. This allows for the simulation of a circle rolling along a straight line or another circle with markers tracing cycloidal curves, offering dynamic visuals to explore the geometry of roulette curves.

<a href="https://www.youtube.com/watch?v=tTs9e5Fu06c" target="_blank"><img src="https://img.shields.io/badge/Video-grey?logo=youtube&logoColor=%23FF0000" height="24"></a>

> [!NOTE]  
> **This guide is specific to Google Colab.**<br>If Manim is already installed on your computer, run `pip install mscene` and `mscene-plugins` from the terminal to add the plugins. Then, import them with `from mscene.plugins import *` in your script.

<a href="https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/colab/mscene.ipynb" target="_blank"><img align="center" src="https://colab.research.google.com/assets/colab-badge.svg"></a>&ensp;[mscene.curiouswalk.com/colab](https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/colab/mscene.ipynb)

## Setup

Open Google [Colab](http://colab.research.google.com#create=true) and run these cells to begin.
```python
%pip install mscene
```
```python
import mscene
%mscene -l manim
```
```python
%mscene plugins
from mscene.roulette import *
```

## Walkthrough

Walkthrough examples to illustrate the functions (methods) of `Wheel` class defined in this plugin.

### Markers

![markers_image](https://github.com/user-attachments/assets/cc7e68cf-0612-4b6b-932b-151cf40ea7c7)

```python
%%manim -qm MarkersImage

class MarkersImage(Scene):
    def construct(self):

        distance = 1  # distance is 1 x radius of Wheel

        angle = PI / 2  # angle is PI / 2 around Wheel

        color = RED  # color of marker

        markers_one = [(distance, angle, color)]

        wheel_one = Wheel(markers=markers_one) # Wheel is a dashed circle

        markers_two = [(3 / 2, PI / 2, RED), (3 / 2, PI * 3 / 2, YELLOW)]

        wheel_two = Wheel(markers=markers_two)

        markers_three = [
            (2 / 3, PI / 2, RED),
            (2 / 3, PI * 3 / 2, YELLOW, WHITE),  # white line segment
            (2 / 3, 0, ORANGE, None),  # no line segment
        ]

        wheel_three = Wheel(markers=markers_three)

        wheels = VGroup(wheel_one, wheel_two, wheel_three).arrange(RIGHT, buff=2)

        self.add(wheels)
```

https://github.com/user-attachments/assets/2bab0c36-8482-4a2e-9905-25ab79bf2c9e

```python
%%manim -qm MarkersScene

class MarkersScene(Scene):
    def construct(self):

        wheel = Wheel(radius=1.5)

        markers = [(1.5, PI / 2, RED), (0.5, -PI / 2, GREEN)]

        self.add(wheel)
        self.wait(0.5)

        # draw markers
        self.play(wheel.draw_markers(markers))
        self.wait(1.5)

        # undraw the last marker (green)
        self.play(wheel.undraw_markers([-1]))
        self.wait(1.5)

        markers_one = [(1, PI / 2, PURPLE), (0.5, PI / 2, GREEN)]

        # draw markers_one
        self.play(wheel.draw_markers(markers_one))
        self.wait(1.5)

        colors = (RED, PURPLE, GREEN)

        markers_two = [(2 / 3, PI * (1 / 2 + i * 2 / 3), c) for i, c in enumerate(colors)]

        # transform wheel markers to markers_two
        self.play(wheel.transform_markers(markers_two))
        self.wait(1.5)

        # undraw all markers
        self.play(wheel.undraw_markers())
        self.wait(1)
```

### Wheel Roll

https://github.com/user-attachments/assets/d24e10a4-1611-43e0-94cf-8b873564f738

```python
%%manim -qm WheelRollScene

class WheelRollScene(Scene):
    def construct(self):

        radius = 0.8
        length = TAU * radius

        circle_one = Circle(radius=radius).rotate(PI / 2)

        circle_two = Circle(radius=3 * radius).rotate(PI / 2)

        line_end = circle_two.get_bottom()
        line_start = line_end + length * LEFT

        line = Line(line_start, line_end)

        wheel = Wheel(radius=radius)

        self.add(wheel)
        self.wait(0.5)
        
        self.play(Create(line), wheel.animate.move(line_start, UP))
        self.bring_to_front(wheel)
        self.wait()

        # rolls along the line
        self.play(wheel.roll(length * RIGHT, run_time=2.5))
        self.wait()

        self.play(ReplacementTransform(line, circle_one))
        self.wait()

        # rolls along the outer edge of circle_one
        self.play(wheel.roll(PI, about=circle_one, run_time=2))
        self.wait()

        self.play(ReplacementTransform(circle_one, circle_two))
        self.wait()

        # rolls along the inner edge of circle_two
        self.play(wheel.roll(PI, about=circle_two, run_time=2.5))
        self.wait()

        self.play(Uncreate(circle_two), wheel.animate.move(ORIGIN))
        self.wait(0.5)
```

### Path Trace

https://github.com/user-attachments/assets/6c7160fb-ecd5-4788-8b7d-6e1795333fed

```python
%%manim -qm PathTraceScene

class PathTraceScene(Scene):
    def construct(self):

        markers = [(2 / 3, PI / 2, RED), (2 / 3, -PI / 2, GREEN)]

        radius = 5 / 6
        length = TAU * radius

        wheel = Wheel(radius=radius, markers=markers)

        self.add(wheel)

        # traced path of red marker
        path_red = wheel.trace_paths([0])
        self.add(path_red)
        self.wait(0.5)

        self.play(wheel.roll(length * LEFT))
        self.wait()

        self.play(FadeOut(path_red))
        self.wait()

        # traced paths of all markers dissipating over time
        paths = wheel.trace_paths(dissipating_time=4 / 3)
        self.add(paths)

        self.play(wheel.roll(2 * length * RIGHT, run_time=4))
        self.wait(2)

        paths.clear_updaters()
        self.remove(paths)

        # traced path of green marker
        path_green = wheel.trace_paths([1])
        self.add(path_green)

        self.play(wheel.roll(length * LEFT))
        self.wait()

        self.play(FadeOut(path_green))
        self.wait(0.5)
```

## Cycloids

https://github.com/user-attachments/assets/bc801373-448d-4b4c-ac67-885819b17a12

```python
%%manim -qm Cycloids

class Cycloids(Scene):
    def construct(self):

        radius = 0.8
        length = TAU * radius

        circle_one = Circle(radius=radius).rotate(PI / 2)

        circle_two = Circle(radius=3 * radius).rotate(PI / 2)

        line_end = circle_two.get_bottom()
        line_start = line_end + length * LEFT

        line = Line(line_start, line_end)

        wheel = Wheel(radius=radius)

        self.add(wheel)
        self.wait(0.5)
        
        self.play(Create(line), wheel.animate.move(line_start, UP))
        self.bring_to_front(wheel)

        marker = [(1, PI/2, YELLOW)]
        self.play(wheel.draw_markers(marker))

        path = wheel.trace_paths(dissipating_time=2)
        self.add(path)

        # rolls along the line
        self.play(wheel.roll(length * RIGHT, run_time=2.5))
        self.wait()

        self.play(ReplacementTransform(line, circle_one))
        self.wait()

        # rolls along the outer edge of circle_one
        self.play(wheel.roll(TAU, about=circle_one, run_time=2.5))
        self.wait()

        self.play(ReplacementTransform(circle_one, circle_two))
        self.wait()

        # rolls along the inner edge of circle_two
        self.play(wheel.roll(TAU, about=circle_two, run_time=3))
        self.wait(2)
        path.clear_updaters()
        self.remove(path)
        self.play(wheel.undraw_markers())

        self.play(Uncreate(circle_two), wheel.animate.move(ORIGIN))
        self.wait(0.5)
```
---
