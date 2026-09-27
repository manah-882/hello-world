from flask import Flask
import ghhops_server as hs
import rhino3dm


# ------------------------------------------------------------
# Hops server
# ------------------------------------------------------------

app = Flask(__name__)
hops = hs.Hops(app)


# ------------------------------------------------------------
# Hops component
# ------------------------------------------------------------

@hops.component(
    "/manipulate_box",
    name="Manipulate Box",
    description="Scale a Brep around its bounding-box centre",
    inputs=[
        hs.HopsBrep(
            "Box",
            "B",
            "Brep to transform"
        ),
        hs.HopsNumber(
            "Scale",
            "S",
            "Uniform scale factor"
        ),
    ],
    outputs=[
        hs.HopsBrep(
            "Box",
            "B",
            "Scaled Brep"
        ),
    ]
)
def manipulate_box(box, scale):

    # --------------------------------------------------------
    # Validate inputs
    # --------------------------------------------------------

    if box is None:
        raise ValueError("Box input is empty.")

    if not box.IsValid:
        raise ValueError("Box input is invalid.")

    if scale <= 0.0:
        raise ValueError("Scale must be greater than zero.")


    # --------------------------------------------------------
    # Get bounding box
    # --------------------------------------------------------

    bounding_box = box.GetBoundingBox()

    if not bounding_box.IsValid:
        raise ValueError("Could not calculate bounding box.")


    # --------------------------------------------------------
    # Get centre
    # --------------------------------------------------------

    center = bounding_box.Center


    # --------------------------------------------------------
    # Create scale transformation
    # --------------------------------------------------------

    transformation = rhino3dm.Transform.Scale(
        center,
        scale
    )


    # --------------------------------------------------------
    # Transform Brep
    # --------------------------------------------------------

    box.Transform(transformation)


    # --------------------------------------------------------
    # Return transformed Brep
    # --------------------------------------------------------

    return box


# ------------------------------------------------------------
# Start server
# ------------------------------------------------------------

if __name__ == "__main__":
    app.run()