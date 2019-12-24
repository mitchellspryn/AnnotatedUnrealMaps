import airsim.airsim_types as at

import annotations_common.localized_point as localized_point

class AnnotatedPoi(localized_point.LocalizedPoint):
    def __init__(self, name, x, y, z):
        super(AnnotatedPoi, self).__init__(x, y, z)
        self.name = name
