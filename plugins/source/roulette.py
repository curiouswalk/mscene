from manim import *


class Wheel(VGroup):
    """A class representing a rolling circle that rolls without sliding along a straight line or around another circle, with markers tracing cycloids as it moves. This allows for the simulation of rolling motion and the generation of cycloidal curves for various configurations."""

    def __init__(
        self,
        radius: float = 1.0,
        color: ManimColor = BLUE,
        markers: list | None = None,
        point=ORIGIN,
        num_dashes=None,
        angle=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.point = point

        self.radius = radius

        if num_dashes is None:
            num_dashes = int(14 * radius)

        self.circle = DashedVMobject(
            Circle(
                arc_center=self.point, radius=self.radius, stroke_width=5, color=color
            ),
            num_dashes=num_dashes,
        )

        if angle is not None:
            self.circle.rotate(angle)

        self.dot = Dot(point=self.point, radius=0.08, color=color)

        self.markers = VGroup()

        if markers is not None:

            for marker in markers:
                new_marker = self._get_marker(*marker)
                self.markers.add(new_marker)

        self.add(self.circle, self.markers, self.dot)

    def _get_point(self, r, theta):
        """Gets polar to cartesian coordinates around the center point."""

        x = r * np.cos(theta)
        y = r * np.sin(theta)
        self.point = self.dot.get_center()
        point = self.point + np.array([x, y, 0])

        return point

    def _get_arc_angle(self, point1, point2):
        """Gets path_arc for Transform animation in transform_markers."""

        a = (point1.angle - point2.angle) % TAU
        b = (point2.angle - point1.angle) % TAU
        arc_angle = -a if a < b else b

        return arc_angle

    def _get_marker(self, r, theta, color=RED, line=True):
        """Gets marker around the center point."""

        marker = VGroup()

        marker.distance = r * self.radius

        marker.angle = theta

        point = self._get_point(marker.distance, marker.angle)

        marker.dot = Dot(point, radius=0.09, color=color)

        if line is not None:
            if isinstance(line, ManimColor):
                line_color = line
            else:
                line_color = average_color(self.dot.color, color)

            marker.line = Line(
                self.dot.get_center(), point, stroke_width=5, stroke_color=line_color
            )

            marker.add(marker.line)
        else:
            marker.line = None

        marker.add(marker.dot)

        return marker

    def move(self, point, direction=ORIGIN):
        """Moves to the given point or Mobject."""

        if isinstance(point, Mobject):
            point = point.get_center()

        self.point = self.dot.get_center()

        target = point - self.point + self.radius * direction

        self.point = point

        self.shift(target)

        return self

    def draw_markers(self, markers, **kwargs):
        """Grows markers from the center point."""

        self.point = self.dot.get_center()

        new_markers = VGroup()

        for marker in markers:

            new_marker = self._get_marker(*marker)

            new_markers.add(new_marker)

            self.markers.add(new_marker)

        self.dot.set_z_index(1)

        anim = GrowFromPoint(new_markers, self.point, **kwargs)

        return anim

    def transform_markers(self, targets, idx=None, **kwargs):
        """Transforms markers into target markers."""

        if idx is None:
            markers = VGroup(*self.markers)
        else:
            markers = VGroup(*[self.markers[i] for i in idx])

        anim = []

        for marker, target in zip(markers, targets):

            new_marker = self._get_marker(*target)
            path_arc = self._get_arc_angle(marker, new_marker)

            marker.distance = new_marker.distance
            marker.angle = new_marker.angle

            anim.append(Transform(marker, new_marker, path_arc=path_arc, **kwargs))

        return anim

    def undraw_markers(self, idx=None, **kwargs):
        """Shrinks markers into the center point."""

        self.point = self.dot.get_center()

        if idx is None:
            markers = VGroup(*self.markers)
        else:
            markers = VGroup(*[self.markers[i] for i in idx])

        self.markers.remove(*markers)

        self.dot.set_z_index(1)

        anim = GrowFromPoint(
            markers, self.point, reverse_rate_function=True, remover=True, **kwargs
        )

        return anim

    def trace_paths(self, idx=None, stroke_width=4, **kwargs):
        """Traces the path of markers."""

        if idx is None:
            markers = VGroup(*self.markers)
        else:
            markers = VGroup(*[self.markers[i] for i in idx])

        paths = VGroup()

        for marker in markers:
            paths.add(
                TracedPath(
                    marker.dot.get_center,
                    stroke_color=marker.dot.color,
                    stroke_width=stroke_width,
                    **kwargs
                )
            )

        return paths

    def roll(
        self,
        direction,
        about=None,
        reverse=False,
        rate_func=linear,
        run_time=2,
        **kwargs
    ):
        """Rolls without sliding along a straight line or around another circle in the same plane."""

        self.point = self.dot.get_center()

        self.circle.angle = 0

        for marker in self.markers:
            marker.theta = marker.angle

        if about is None:

            distance = np.linalg.norm(direction)

            if any(direction > ORIGIN):
                distance *= -1

        else:

            if isinstance(about, Mobject):
                length = about.width / 2
                dis = self.point - about.get_center()
            else:
                length = 0
                dis = self.point - about

            radius = np.linalg.norm(dis)

            theta = angle_of_vector(dis)

            distance = radius * direction

            if radius < length:
                distance *= -1

        if reverse:
            distance *= -1

        def update_alpha(self, alpha):

            angle = (alpha * distance) / self.radius

            if about is None:

                point1 = self.point + alpha * direction

            else:

                point1_angle = alpha * direction + theta

                point1 = ORIGIN + (
                    np.cos(point1_angle) * radius,
                    np.sin(point1_angle) * radius,
                    0.0,
                )

            self.circle.rotate(angle - self.circle.angle).move_to(point1)

            self.circle.angle = angle

            self.dot.move_to(point1)

            for marker in self.markers:

                point2_angle = angle + marker.theta
                marker.angle = point2_angle

                point2 = point1 + (
                    np.cos(point2_angle) * marker.distance,
                    np.sin(point2_angle) * marker.distance,
                    0.0,
                )

                if marker.line:
                    marker.line.set_points_by_ends(point1, point2)

                marker.dot.move_to(point2)

        anim = UpdateFromAlphaFunc(
            self, update_alpha, rate_func=rate_func, run_time=run_time, **kwargs
        )

        return anim
