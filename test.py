from student import Student, Personality, Intelligence, Interest, Happyness


def api_call():
    subject = "3D Modeling"
    transcription = """3D modeling is the process of creating three-dimensional representations of objects using 
    specialized software. This process begins with defining the basic geometry of the object, often starting with 
    simple shapes such as cubes, spheres, or planes. These basic shapes are then modified through operations such 
    as extruding, scaling, and rotating to achieve the desired shape.

    Next, the model is refined by adding more complex details, such as curves, irregular surfaces, and small features. 
    During this phase, modelers work with polygons and vertices, adjusting specific points to achieve a more precise  
    and realistic structure.

    Once the geometry is complete, the next step is UV mapping, a process that flattens the surface of the model to
     allow for the application of two-dimensional textures. These textures add visual details such as colors,
      materials, and fine details (for example, wood or metal).

    Finally, to give realism to the model, materials and lights are applied. Materials determine the properties
     of the object, such as reflectivity, opacity, and roughness, while lights simulate the light sources that 
     illuminate the model in the scene."""

    test = Student(
        subject,
        personality=Personality.SHY,
        intelligence=Intelligence.LOW,
        interest=Interest.UNINTERESTED,
        happyness=Happyness.SAD
    )

    print(test.generate_response(transcription))


if __name__ == "__main__":
    api_call()
