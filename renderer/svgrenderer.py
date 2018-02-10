import svgwrite

class SvgRenderer(object):

    @staticmethod
    def render_plan(floorplan, connectivity_graph=False):
        drawing = svgwrite.Drawing('out/output.svg')
        group = svgwrite.container.Group(transform='translate(32,32), scale(3)')
        drawing.add(group)

        # for i, room in enumerate(floorplan.rooms):
        #     print "I", i
        #     drawing = svgwrite.Drawing('out/output.svg')
        #     group = svgwrite.container.Group(transform='translate(32,32), scale(3)')
        #     drawing.add(group)
        #     for edge in room.edges:
        #         SvgRenderer.render_edge(edge, drawing, group)
        #     drawing.saveas("out/output-" + str(i) + ".svg", pretty=True)
        # return "done"

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
        print "Rendering.."
        for i, room in enumerate(rooms):
            print "r"
            group.add(
                drawing.circle(room.center, r=5, stroke='blue', fill='green', stroke_width=1)
            )
            for e in room.edges:
                print "E", e.cartesian_points
                group.add(
                    drawing.line(room.center, e.center, stroke=svgwrite.rgb(0, 255, 0))
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
