# Cycloids

<a href=""><img align="left" height="240px" src=""></a>

### Cycloidal Curves From Rolling Circles

<p align="justify">Learn how a circle rolls along a straight line, creating a cycloid, and explore its variations, epicycloid, and hypocycloid, formed when it rolls along the outside or inside edge of another circle. Simulate with dynamic visuals to study the applications of these fascinating curves in various fields, including mathematics, physics, and engineering. Perfect for anyone curious about the geometry and dynamics of rolling motion!</p>

[Open in Colab]&ensp;[mscene.curiouswalk.com/colab/cycloids](www.curiouswalk.com)


## Setup

[Manim in Colab]&ensp;[mscene.curiouswalk.com/colab](https://mscene.curiouswalk.com/colab)

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

## Rolling Circle

Download `rollingcircle.py` from [mscene.curiouswalk.com/src/rollingcircle.py](https://mscene.curiouswalk.com/src/rollingcircle.py) and import `RollingCircle`.

```python
!wget -nv mscene.curiouswalk.com/src/rollingcircle.py; pwd; ls
```

```python
from rollingcircle import *
```

### Test Scene

https://github.com/user-attachments/assets/c832e35d-7eb9-4607-8b5b-9700538395dc

```python
%%manim -qm TestScene

class TestScene(Scene):
    def construct(self):

        rc = RollingCircle()
        self.add(rc)

        self.play(rc.roll(PI * LEFT, run_time=1.5))

        self.play(rc.roll(TAU * RIGHT, run_time=3))

        self.play(rc.roll(PI * LEFT, run_time=1.5))
        self.wait()
```

## Walkthrough

Walkthrough examples to illustrate the functions (methods) of RollingCircle.

### Markers

![markers_image](https://github.com/user-attachments/assets/2035eb46-dfca-4c2e-aede-4fefddc7378c)

```python
%%manim -qm MarkersImage

class MarkersImage(Scene):
    def construct(self):

        distance = 1  # distance set to '1' x radius of RollingCircle

        angle = PI / 2  # angle set to 'PI/2' around RollingCircle

        color = RED  # color of marker

        markers_one = [(distance, angle, color)]

        rc_one = RollingCircle(markers=markers_one)

        markers_two = [(3 / 2, PI / 2, RED), (3 / 2, PI * 3 / 2, YELLOW)]

        rc_two = RollingCircle(markers=markers_two)

        markers_three = [
            (2 / 3, PI / 2, RED),
            (2 / 3, PI * 3 / 2, YELLOW, WHITE),  # white line segment
            (2 / 3, 0, ORANGE, None),  # no line segment
        ]

        rc_three = RollingCircle(markers=markers_three)

        rolling_circles = VGroup(rc_one, rc_two, rc_three).arrange(RIGHT, buff=2)

        self.add(rolling_circles)

```

https://github.com/user-attachments/assets/244d1694-cc88-4b61-b23c-1f4f44cba772

```python
%%manim -qm MarkersScene

class MarkersScene(Scene):
    def construct(self):

        rc = RollingCircle(radius=1.5)

        markers = [(1.5, PI / 2, RED), (0.5, -PI / 2, GREEN)]

        self.add(rc)
        self.wait(0.5)

        # draws markers
        self.play(rc.draw_markers(markers))
        self.wait(1.5)

        # undraws the last marker (green)
        self.play(rc.undraw_markers([-1]))
        self.wait(1.5)

        markers_one = [(1, PI / 2, PURPLE), (0.5, PI / 2, GREEN)]

        # draws markers_one
        self.play(rc.draw_markers(markers_one))
        self.wait(1.5)

        colors = (RED, PURPLE, GREEN)

        markers_two = [(2 / 3, PI * (1 / 2 + i * 2 / 3), colors[i]) for i in range(3)]

        # transforms rc.markers to markers_two
        self.play(rc.transform_markers(markers_two))
        self.wait(1.5)

        # undraws all markers
        self.play(rc.undraw_markers())
        self.wait(1)

```
### Circle Roll

https://github.com/user-attachments/assets/2b6379f0-1319-4e0d-a2b5-469f1ba1c6c5

```python
%%manim -qm CircleRollScene

class CircleRollScene(Scene):
    def construct(self):

        circle_one = Circle(radius=1).rotate(PI / 2)

        circle_two = Circle(radius=3).rotate(PI / 2)

        line_end = circle_two.get_bottom()
        line_start = line_end + 5 * LEFT

        line = Line(line_start, line_end)

        rc = RollingCircle()

        self.add(rc)
        self.wait(0.5)
        
        self.play(Create(line), rc.animate.move(line_start, UP))
        self.bring_to_front(rc)
        self.wait()

        # rolls along the line
        self.play(rc.roll(5 * RIGHT))
        self.wait()

        self.play(ReplacementTransform(line, circle_one))
        self.wait()

        # rolls along the outer edge of circle_one
        self.play(rc.roll(PI, about=circle_one, run_time=2.5))
        self.wait()

        self.play(ReplacementTransform(circle_one, circle_two))
        self.wait()

        # rolls along the inner edge of circle_two
        self.play(rc.roll(PI, about=circle_two, run_time=3))
        self.wait()

        self.play(Uncreate(circle_two), rc.animate.move(ORIGIN))
        self.wait(0.5)

```
### Path Trace

https://github.com/user-attachments/assets/68f57ffe-f84e-45bc-aadb-9e25bb54faf6

```python
%%manim -qm PathTraceScene

class PathTraceScene(Scene):
    def construct(self):

        markers = [(2 / 3, PI / 2, RED), (2 / 3, -PI / 2, GREEN)]

        radius = 5 / 6
        length = TAU * radius

        rc = RollingCircle(radius=radius, markers=markers)

        self.add(rc)

        # traced path of red marker
        path_red = rc.trace_paths([0])
        self.add(path_red)
        self.wait(0.5)

        self.play(rc.roll(length * LEFT))
        self.wait()

        self.play(FadeOut(path_red))
        self.wait()

        # traced paths of both markers
        paths = rc.trace_paths(dissipating_time=4 / 3)
        self.add(paths)

        self.play(rc.roll(2 * length * RIGHT, run_time=4))
        self.wait(2)

        paths.clear_updaters()
        self.remove(paths)

        # traced path of green marker
        path_green = rc.trace_paths([1])
        self.add(path_green)

        self.play(rc.roll(length * LEFT))
        self.wait()

        self.play(FadeOut(path_green))
        self.wait(0.5)

````

## Animation Scenes

**Scenes**&ensp;[mscene.curiouswalk.com/colab/cycloids](www.curiouswalk.com)

**Colab**&ensp;[mscene.curiouswalk.com/colab/cycloids](www.curiouswalk.com)

---
