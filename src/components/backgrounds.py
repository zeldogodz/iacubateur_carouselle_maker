def make_background(style, width, height):
    if style == "Neon grid":
        return create_neon_grid_background(width, height)
    elif style == "Blue gradient":
        return create_blue_gradient_background(width, height)
    elif style == "Abstract circles":
        return create_abstract_circles_background(width, height)
    elif style == "Diagonal stripes":
        return create_diagonal_stripes_background(width, height)
    elif style == "Noise texture":
        return create_noise_texture_background(width, height)
    elif style == "Radial glow":
        return create_radial_glow_background(width, height)
    elif style == "Mesh gradient":
        return create_mesh_gradient_background(width, height)
    else:
        raise ValueError("Unknown background style: {}".format(style))

def create_neon_grid_background(width, height):
    # Implementation for neon grid background
    pass

def create_blue_gradient_background(width, height):
    # Implementation for blue gradient background
    pass

def create_abstract_circles_background(width, height):
    # Implementation for abstract circles background
    pass

def create_diagonal_stripes_background(width, height):
    # Implementation for diagonal stripes background
    pass

def create_noise_texture_background(width, height):
    # Implementation for noise texture background
    pass

def create_radial_glow_background(width, height):
    # Implementation for radial glow background
    pass

def create_mesh_gradient_background(width, height):
    # Implementation for mesh gradient background
    pass