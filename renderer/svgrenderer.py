import svgwrite

class SvgRenderer(object):

    @staticmethod
    def render_plan(floorplan):
        drawing = svgwrite.Drawing('out/output.svg')
        group = svgwrite.container.Group(transform='translate(32,32), scale(32)')
        drawing.add(group)

        edges = set()
        for room in floorplan.rooms:
            for edge in room.edges:
                edges.add(edge)

        for edge in edges:
            SvgRenderer.render_edge(edge,drawing, group)

        drawing.save()

    @staticmethod
    def render_edge(edge, drawing, group):
        p0, p1 = edge.cartesian_points
        group.add(drawing.line(p0, p1, stroke=svgwrite.rgb(0, 0, 0)))
