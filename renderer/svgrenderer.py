import svgwrite
import itertools
import numpy as np

from core.opening import Door, DoorFactory

class SvgRenderer(object):

    def __init__(self, floorplan, scaling=16):
        self.floorplan = floorplan
        self.drawing = svgwrite.Drawing('out/output.svg')
        self.group = svgwrite.container.Group(transform='translate(32,32)')
        self.drawing.add(self.group)
        self.scaling = scaling

    def render(self, filename, show_edge_connections=False):
        edges = set()
        for room in self.floorplan.rooms:
            for edge in room.edges:
                edges.add(edge)

        for edge in edges:
            self.render_edge(edge)

        if show_edge_connections:
            self.render_edge_connections()

        for room in self.floorplan.rooms:
            self.render_room_label(room)

        self.drawing.saveas(filename, pretty=True)

    def scale_point(self, p):
        return p[0]*self.scaling, p[1]*self.scaling

    def denumpy_point(self, p):
        return p[0]*1.0, p[1]*1.0

    def render_edge(self, edge):
        p0, p1 = [self.scale_point(p) for p in edge.cartesian_points]
        self.group.add(self.drawing.line(p0, p1, **{
            "stroke": svgwrite.rgb(30, 30, 30),
            "stroke-width": 12,
            "stroke-linecap": "round"
        }))
        self.render_door(edge, DoorFactory.interior_door(0.5, -1))

    def render_room_label(self, room):
        label = room.label.upper()
        x, y = self.scale_point(room.center)
        self.group.add(
            self.drawing.text(label, x=[x], y=[y], **{
                "text-anchor": "middle",
                "style": "font-family: sans-serif; font-size: 20pt",
            })
        )

    def render_door(self, edge, door):
        a, b = edge.radial_points(door.t, door.width * 0.5)
        unit = edge.unit_vector
        rotated_unit = np.array([-unit[1], unit[0]])
        hinge = a if door.opens_LR == "left" else b
        endpoint = hinge + door.width * rotated_unit

        self.mark_point(self.scale_point(hinge), 'yellowgreen', radius=16)
        self.mark_point(self.scale_point(a), 'red', radius=8)
        self.mark_point(self.scale_point(b), 'yellow', radius=8)
        self.mark_point(self.scale_point(endpoint), 'blue')
        # Draw a line from hinge to end_point
        self.group.add(
            self.drawing.line(self.scale_point(hinge), self.scale_point(endpoint), **{
                "stroke": svgwrite.rgb(0, 0, 0),
                "stroke-width": 4,
            })
        )
        # self.group.add(
        #     self.drawing.path().push_arc(hinge, )
        # )



    def mark_point(self, point, color, radius=16):
        self.group.add(
            self.drawing.circle(point, r=radius, stroke=color, fill=color, stroke_width=1)
        )




    # @staticmethod
    # def render_plan(floorplan, connectivity_graph=False):
    #     drawing = svgwrite.Drawing('out/output.svg')
    #     group = svgwrite.container.Group(transform='translate(32,32), scale(3)')
    #     drawing.add(group)

    #     edges = set()
    #     for room in floorplan.rooms:
    #         for edge in room.edges:
    #             edges.add(edge)

    #     for edge in edges:
    #         SvgRenderer.render_edge(edge,drawing, group)

    #     if connectivity_graph:
    #         SvgRenderer.render_connectivity_graph(floorplan.rooms, drawing, group)

    #     SvgRenderer.render_labels(floorplan.rooms, drawing, group)

    #     drawing.save()

    # @staticmethod
    # def render_edge(edge, drawing, group):
    #     p0, p1 = edge.cartesian_points
    #     group.add(drawing.line(p0, p1, stroke=svgwrite.rgb(0, 0, 0)))

    # @staticmethod
    # def render_connectivity_graph(rooms, drawing, group):
    #     for i, room in enumerate(rooms):
    #         group.add(
    #             drawing.circle(room.center, r=2, stroke='blue', fill='blue', stroke_width=1)
    #         )
    #         for e in room.edges:
    #             group.add(
    #                 drawing.line(room.center, e.center, stroke=svgwrite.rgb(0, 255, 0))
    #             )


    # @staticmethod
    # def render_labels(rooms, drawing, group):
    #     for room in rooms:
    #         x, y = room.center
    #         group.add(
    #             drawing.text(room.label, x=[x], y=[y], **{
    #                 "text-anchor": "middle"
    #             })
    #         )
