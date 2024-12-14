# Cycloids

<a href="https://www.youtube.com/watch?v=8d0qzpxyGEs" target="_blank"><img align="left" width="50%" src="/docs/assets/8d0qzpxyGEs.jpeg"></a>

### Cycloidal Curves From Rolling Circles

Learn how a circle rolls along a straight line, creating a cycloid, and explore its variations, epicycloid, and hypocycloid, formed when it rolls along the outside or inside edge of another circle. Roll circles in different configurations to draw various cycloidal curves and observe the intriguing patterns. Simulate with dynamic visuals to study the applications of these curves in multiple fields, including mathematics, physics, and engineering. Perfect for anyone curious about the geometry and dynamics of rolling motion!

[Open in Colab]&ensp;[mscene.curiouswalk.com/colab/cycloids](https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/cycloids/cycloids.ipynb)

### Contents
- [Setup](#setup)
- [Walkthrough](#walkthrough)
- [Animation Scenes](#animation-scenes)
  - [Cycloid](#cycloid)
  - [Trochoids](#trochoids)
  - [Epicycloid](#epicycloid)
  - [Epitrochoids](#epitrochoids)
  - [Hypocycloid](#hypocycloid)
  - [Ellipses](#ellipses)
  - [Two Rolling Circles](#two-rolling-circles)

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

### Rolling Circle

Download `rollingcircle.py` from [mscene.curiouswalk.com/src/rollingcircle.py](https://mscene.curiouswalk.com/src/rollingcircle.py) and import `RollingCircle`.

```python
!wget -nv mscene.curiouswalk.com/src/rollingcircle.py; pwd; ls
```

```python
from rollingcircle import *
```

#### Test Scene

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

### Cycloid

https://github.com/user-attachments/assets/71ad3ce9-10a9-4ef1-b9b5-4d67395781fa

```python
%%manim -qm Cycloid

class Cycloid(Scene):
    def construct(self):

        length = config.frame_width * 0.75  # rolling distance
        radius = length / (2 * TAU)  # radius set for 2 revolutions

        num_line = NumberLine(
            x_range=[-TAU, TAU, PI], length=length, color=ManimColor("#6F828A")
        ).shift(DOWN * radius)

        point = num_line.n2p(-TAU) + radius * UP

        markers = [(1, PI / 2, ManimColor("#6019E3"))]  # add more markers

        rc = RollingCircle(
            radius=radius, color=ManimColor("#04D9FF"), markers=markers, point=point
        )

        text = Text("Cycloid").shift(2.5 * radius * DOWN)

        self.add(text, num_line, rc)
        self.wait(0.5)

        path = rc.trace_paths()
        self.add(path)

        self.play(rc.roll(length * RIGHT, run_time=4))
        self.wait()

        path.clear_updaters()
        self.play(path.animate.fade(2 / 3))

        new_path = rc.trace_paths(dissipating_time=2)
        self.add(new_path)

        self.play(rc.roll(length * LEFT, run_time=4))
        self.wait()

        self.play(FadeOut(path))

        new_path.clear_updaters()
        self.wait(0.5)

```

### Trochoids

https://github.com/user-attachments/assets/fb7cf376-b882-445f-8ed8-823a4df5a05f

```python
%%manim -qm Trochoids

class Trochoids(Scene):
    def construct(self):

        length = config.frame_width * 0.75  # rolling distance
        radius = length / (2 * TAU)  # radius set for 2 revolutions

        num_line = NumberLine(
            x_range=[-TAU, TAU, PI], length=length, color=ManimColor("#6F828A")
        ).shift(DOWN * radius)

        point = num_line.n2p(-TAU) + radius * UP

        colors = [ManimColor(hex) for hex in ("#19E360", "#6019E3", "#E31937")]

        markers = [
            (1.5, PI / 2, colors[2]),
            (1, PI / 2, colors[1]),
            (0.5, PI / 2, colors[0]),
        ]
        # roll again with these markers
        # markers = [(1.5, PI/2, colors[2]), (1, -PI/2, colors[1]), (.5, PI/2, colors[0])]

        rc = RollingCircle(
            radius=radius, color=ManimColor("#04D9FF"), markers=markers, point=point
        )

        labels = VGroup()
        txt = ["Curtate Cycloid", "Cycloid", "Prolate Cycloid"]

        for i in range(3):
            text = Text(txt[i], font_size=40)
            dot = Dot(radius=0.125, color=colors[i]).next_to(text[0], LEFT)
            labels.add(VGroup(dot, text))

        labels.arrange(RIGHT, buff=0.5).shift(2.5 * radius * DOWN)

        self.add(labels, num_line, rc)
        self.wait(0.5)

        paths = rc.trace_paths()
        self.add(paths)

        self.play(rc.roll(length * RIGHT, run_time=4))
        self.wait()

        paths.clear_updaters()
        self.play(paths.animate.fade(2 / 3))

        new_paths = rc.trace_paths(dissipating_time=2)
        self.add(new_paths)

        self.play(rc.roll(length * LEFT, run_time=4))
        self.wait()

        self.play(FadeOut(paths))

        new_paths.clear_updaters()
        self.wait(0.5)

```

### Epicycloid

https://github.com/user-attachments/assets/afb8f07e-f391-4089-bcf8-bd651d66076a

```python
%%manim -qm Epicycloid

class Epicycloid(Scene):
    def construct(self):

        # config.frame_rate = 60 # higher frame_rate for smooth traced path; not required for longer run_time

        k = 3  # k = R/r; R: radius of Circle, r: radius of RollingCirlce

        angle = -TAU # rotation around Circle;

        run_time = 4  # run_time of roll animation

        # roll again with these values
        # k, angle, run_time = (2, -TAU, 4)
        # k, angle, run_time = (1, -TAU, 4)
        # k, angle, run_time = (1.5, -TAU*2, 8)
        # k, angle, run_time = (.5, -TAU*2, 8)

        h = config.frame_height * 3 / 8
        r = h / (2 + k)

        markers = [(1, PI / 2, ManimColor("#6019E3"))]

        rc = RollingCircle(radius=r, color=ManimColor("#04D9FF"), markers=markers)

        circle = Circle(radius=k * r, color=ManimColor("#6F828A"))

        text = Text(f"Epicycloid\nk = {k}").to_corner(UL, buff=2 / 3)

        rc.move(circle.get_top(), UP)

        self.add(text, circle, rc)
        self.wait(0.5)

        path = rc.trace_paths()
        self.add(path)

        self.play(rc.roll(angle, about=circle, run_time=run_time))

        path.clear_updaters()
        self.wait(2)

        self.play(FadeOut(path))
        self.wait(0.5)

```

### Epitrochoids

https://github.com/user-attachments/assets/24e7945b-2b22-4e56-94e3-21dba0151a4e

```python
%%manim -qm Epitrochoids

class Epitrochoids(Scene):
    def construct(self):

        k, angle, run_time = (3, -TAU, 4)
        # k, angle, run_time = (1.5, -TAU*2, 8)

        h = config.frame_height * 3 / 8
        r = h / (2 + k)

        markers = [
            (1.5, PI / 2, ManimColor("#6019E3")),
            (0.5, -PI / 2, ManimColor("#E31937")),
        ]

        rc = RollingCircle(radius=r, color=ManimColor("#04D9FF"), markers=markers)

        circle = Circle(radius=k * r, color=ManimColor("#6F828A"))

        text = Text(f"Epitrochoids\nk = {k}").to_corner(UL, buff=2 / 3)

        rc.move(circle.get_top(), UP)

        self.add(text, circle, rc)
        self.wait(0.5)

        paths = rc.trace_paths()
        self.add(paths)

        self.play(rc.roll(angle, about=circle, run_time=run_time))

        paths.clear_updaters()
        self.wait(2)

        self.play(FadeOut(paths))
        self.wait(0.5)

```

### Hypocycloid

https://github.com/user-attachments/assets/e032563e-8735-43b9-b8f7-0c3c8805c92f

```python
%%manim -qm Hypocycloid

class Hypocycloid(Scene):
    def construct(self):

        k, angle, run_time = (3, -TAU, 4)
        # k, angle, run_time = (2.5, -TAU*2, 8)

        h = config.frame_height * 3 / 8
        r = h / k

        markers = [(1, PI / 2, ManimColor("#6019E3"))]

        rc = RollingCircle(radius=r, color=ManimColor("#04D9FF"), markers=markers)

        circle = Circle(radius=k * r, color=ManimColor("#6F828A"))

        text = Text(f"Hypocycloid\nk = {k}").to_corner(UL, buff=2 / 3)

        rc.move(circle.get_top(), DOWN)

        self.add(text, circle, rc)
        self.wait(0.5)

        paths = rc.trace_paths()
        self.add(paths)

        self.play(rc.roll(angle, about=circle, run_time=run_time))

        paths.clear_updaters()
        self.wait(2)

        self.play(FadeOut(paths))
        self.wait(0.5)

```

### Ellipses

https://github.com/user-attachments/assets/dfbff5ca-7331-4d30-b8ca-8461f16b6a63

```python
%%manim -ql Ellipses

class Ellipses(Scene):
    def construct(self):

        k, angle, run_time = (2, -TAU, 4)

        h = config.frame_height * 3 / 8
        r = h / k

        ellipse_markers = [
            (1.5, 0, ManimColor("#6019E3")),
            (0.5, PI, ManimColor("#E31937")),
        ]

        rc = RollingCircle(
            radius=r, color=ManimColor("#04D9FF"), markers=ellipse_markers
        )
        circle = Circle(radius=k * r, color=ManimColor("#6F828A"))
        text = Text(f"Hypotrochoids\n(Ellipses) k = {k}", font_size=44).to_corner(
            UL, buff=2 / 3
        )

        rc.move(circle.get_top(), DOWN)

        self.add(text, circle, rc)
        self.wait(0.5)

        line_markers = [
            (1, PI / 2, ManimColor("#5A7D9A")),
            (1, -PI / 2, ManimColor("#5A7D9A")),
        ]
        self.play(rc.draw_markers(line_markers))
        self.wait()

        ellipses = rc.trace_paths([0, 1])
        lines = rc.trace_paths([2, 3])

        self.add(lines, ellipses)

        self.play(rc.roll(angle, about=circle, run_time=run_time))
        self.wait()

        lines.clear_updaters()
        ellipses.clear_updaters()

        self.play(
            FadeOut(lines), ellipses.animate.fade(2 / 3), rc.undraw_markers([2, 3])
        )
        self.wait()

        paths = rc.trace_paths(dissipating_time=run_time / 2)
        self.add(paths)

        self.play(rc.roll(angle * 2, about=circle, run_time=run_time * 2))
        self.wait(2)

        paths.clear_updaters()

        self.play(FadeOut(ellipses, paths))
        self.wait(0.5)

```

### Two Rolling Circles

https://github.com/user-attachments/assets/d462c556-3dbd-4434-9ded-c96e48aff6e2

```python
%%manim -qm TwoRollingCircles

class TwoRollingCircles(Scene):
    def construct(self):

        k, angle, run_time = (2.25, -4 * TAU, 16)
        # k, angle, run_time = (2.8, -5 * TAU, 18)

        h = config.frame_height * 3 / 8
        r = h / (2 + k)

        color_one = ManimColor("#6019E3")
        color_two = ManimColor("#E31937")

        rc_one_markers = [(1, PI / 2, color_one)]
        rc_two_markers = [(1, -PI / 2, color_two)]

        rc_one = RollingCircle(
            radius=r, color=ManimColor("#04D9FF"), markers=rc_one_markers
        )

        rc_two = RollingCircle(
            radius=r, color=ManimColor("#04D9FF"), markers=rc_two_markers
        )

        circle = Circle(radius=k * r, color=ManimColor("#6F828A"))

        rc_one.move(circle.get_top(), UP)
        rc_two.move(circle.get_top(), DOWN)

        rc_one_path = rc_one.trace_paths()
        rc_two_path = rc_two.trace_paths()

        self.add(circle, rc_one_path, rc_two_path, rc_one, rc_two)
        self.wait(0.5)

        self.play(
            rc_one.roll(angle, about=circle, run_time=run_time),
            rc_two.roll(angle, about=circle, run_time=run_time),
        )

        rc_one_path.clear_updaters()
        rc_two_path.clear_updaters()
        self.wait(2)

        self.play(FadeOut(rc_one_path, rc_two_path))
        self.wait(0.5)

```

---
