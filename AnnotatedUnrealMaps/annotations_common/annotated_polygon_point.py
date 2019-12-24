import airsim.airsim_types as at

import annotations_common.localized_point as localized_point

class AnnotatedPolygonPoint(localized_point.LocalizedPoint):
    def __init__(self, x, y, z, is_manual):
        super(AnnotatedPolygonPoint, self).__init__(x, y, z)
        self.is_manual = is_manual

