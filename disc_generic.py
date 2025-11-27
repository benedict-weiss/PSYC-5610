import numpy as np
from mitsuba import ScalarTransform4f as T
import mitsuba as mi

def initialise_scene(radius,
                    disc_elevation,
                    disc_rotation,
                    light_elevation,
                    light_rotation):

    # light elevation: 0 is grazing from side, -pi/2 is from below, pi/2 is from above
    # light rotation: tbc

    disc_elevation_deg = float(np.rad2deg(disc_elevation)) # necessary conversion?
    disc_rotation_deg = float(np.rad2deg(disc_rotation))

    disc_to_world = (
        T.translate([0.0, 0.0, 1.0])
        .rotate([0, 1, 0], disc_rotation_deg)
        .rotate([1, 0, 0], disc_elevation_deg)
        .scale(radius)
    )

    l_x = float(np.cos(light_elevation) * np.cos(light_rotation))
    l_y = float(np.sin(light_elevation))
    l_z = float(np.cos(light_elevation) * np.sin(light_rotation))
    # inversion here?
    light_direction = [l_x, l_y, l_z]

    # inspired by cbox-generic
    
    d = {
        'type': 'scene',
        'integrator': {
            'type': 'path',
            'max_depth': 6,
        },
        
        'sensor': {
            'type': 'perspective',
            'fov_axis': 'smaller',
            'near_clip': 0.001,
            'far_clip': 100.0,
            'focus_distance': 1000,
            'fov': 39.3077,
            'to_world': T.look_at(
                origin=[0, 0, 4],
                target=[0, 0, 0],
                up=[0, 1, 0]
            ),
            'sampler': {
                'type': 'independent',
                'sample_count': 64 # bumped this
            },
            'film': {
                'type': 'hdrfilm',
                'width' : 256,
                'height': 256,
                'rfilter': {
                    'type': 'tent', # or box here?
                },
                'pixel_format': 'luminance', # changed here
                'component_format': 'float32',
            }
        },

        'gray': {
            'type': 'diffuse',
            'reflectance': 0.5
        },

        'background': {
            'type': 'rectangle',
            'to_world': T.translate([0.0, 0.0, 0.0]).scale(3.0), # or 4.0 maybe?
            'bsdf': {
                'type': 'ref',
                'id': 'gray'
            }
        },

        # not great notation here haha
        'disc': {
            'type': 'sphere',
            'to_world': disc_to_world,
            'bsdf': {
                'type': 'ref',
                'id': 'gray'
            }
        },

        # good intensity here?
        'light': {
            'type': 'directional',
            'direction': light_direction,
            'irradiance': 2.0
        },


    }

    return d