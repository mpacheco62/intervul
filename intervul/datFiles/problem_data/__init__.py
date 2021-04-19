from ._definitions import _Problem_data
from ._definitions import (Seepage,
                           Structural_continuum,
                           Structural_shells,
                           Waves,
                           Thermal,
                           Incompressibility,
                           Dynamic,
                           Coupl,
                           Dimensions,
                           Local_coordinate_system,
                           Active_elements,
                           Deformation_dependent_face_load)

from ._anisotropic_material import Anisotropic_material
from . import anisotropic_material

from ._contact import Contact
from . import contact

from ._weak_form import Weak_form
from . import weak_form

from . import large_strain_disp
