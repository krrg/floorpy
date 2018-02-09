import svgwrite

class SvgRenderer(object):

    @staticmethod
    def render_plan(floorplan, connectivity_graph=False):
        drawing = svgwrite.Drawing('out/output.svg')
        group = svgwrite.container.Group(transform='translate(32,32), scale(8)')
        drawing.add(group)

        # for i, room in enumerate(floorplan.rooms):
        #     for edge in room.edges:
        #         SvgRenderer.render_edge(edge, drawing, group)
        #     drawing.saveas("output-" + str(i) + ".svg", pretty=True)

        edges = set()
        for room in floorplan.rooms:
            for edge in room.edges:
                edges.add(edge)

        for edge in edges:
            SvgRenderer.render_edge(edge,drawing, group)

        if connectivity_graph:
            SvgRenderer.render_connectivity_graph(floorplan.rooms, drawing, group)

        SvgRenderer.render_labels(floorplan.rooms, drawing, group)

        drawing.save()

    @staticmethod
    def render_edge(edge, drawing, group):
        p0, p1 = edge.cartesian_points
        group.add(drawing.line(p0, p1, stroke=svgwrite.rgb(0, 0, 0)))

    @staticmethod
    def render_connectivity_graph(rooms, drawing, group):
        for room in rooms:
            for neighbor in room.neighbors:
                group.add(
                    drawing.line(room.center, neighbor.center, stroke=svgwrite.rgb(0, 255, 0))
                )

    @staticmethod
    def render_labels(rooms, drawing, group):
        for room in rooms:
            x, y = room.center
            group.add(
                drawing.text(room.label, x=[x], y=[y], **{
                    "text-anchor": "middle"
                })
            )
