from manim import *


class KochCurve(VMobject):
    def __init__(
        self,
        level=0,
        length=config.frame_width * 3 / 4,
        point=ORIGIN,
        group=True,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.level = 0 if level < 0 else level
        self.length = length
        self.kwargs = kwargs
        self._koch_curve(self.level, self.length, point, group=group)

    def _koch_curve(self, level, length, point, group=True):
        l = length / (3**level)
        points = [LEFT * l / 2, RIGHT * l / 2]
        self.set_points_as_corners(points)
        vmob = self.copy()
        for _ in range(level):
            new_vmob = VGroup()
            for i in (0, PI / 3, -PI / 3, 0):
                new_vmob.add(vmob.copy().rotate(i))
            new_vmob.arrange(RIGHT, buff=0, aligned_edge=DOWN)
            vmob.become(new_vmob)
        vmob.move_to(point)
        if group:
            points = vmob.get_all_points()
            self.set_points(points)
        else:
            self.become(vmob)

    def new_level(self, level=None, length=None, point=None, **kwargs):
        level = self.level if level is None else level
        length = self.length if length is None else length
        point = self.get_center() if point is None else point
        self.kwargs.update(kwargs)
        kwargs = self.kwargs
        self.__init__(level, length, point, **kwargs)

    def next_level(self, **kwargs):
        level = self.level + 1
        self.new_level(level, **kwargs)

    def prev_level(self, **kwargs):
        level = self.level - 1
        self.new_level(level, **kwargs)


class KochSnowflake(KochCurve):
    def __init__(
        self,
        level=0,
        length=config.frame_width / 3,
        point=ORIGIN,
        invert=False,
        fill_opacity=1,
        stroke_width=0,
        color=BLUE,
        **kwargs
    ):
        kwargs.update(
            {
                "fill_opacity": fill_opacity,
                "stroke_width": stroke_width,
                "color": color,
            }
        )

        super().__init__(**kwargs)

        self.level = 0 if level < 0 else level
        self.length = length
        kwargs.update({"invert": invert})
        self.kwargs = kwargs
        self._koch_snowflake(self.level, self.length, point, invert)

    def _koch_snowflake(self, level, length, point, invert):

        self._koch_curve(level, length, point, group=True)

        if invert:
            self.rotate(PI).reverse_direction()
            kc2 = self.copy().rotate(PI, about_point=self.get_top())
        else:
            kc2 = self.copy().rotate(PI, about_point=self.get_bottom())

        kc1 = self.copy().rotate(-PI / 3, about_point=self.get_end())
        kc3 = self.copy().rotate(PI / 3, about_point=self.get_start())
        ks = VGroup(kc1, kc2, kc3).move_to(point)

        points = ks.get_all_points()

        self.sides = ks.set_style(fill_opacity=0, stroke_width=4)

        self.set_points_as_corners(points)
