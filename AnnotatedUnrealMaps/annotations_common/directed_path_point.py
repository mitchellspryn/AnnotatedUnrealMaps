import airsim.airsim_types as at

import annotations_common.localized_point as localized_point

class DirectedPathPoint(localized_point.LocalizedPoint):
    def __init__(self, x, y, z, index, is_manual):
        super(DirectedPathPoint, self).__init__(x, y, z)
        self.is_manual = is_manual

        if (index is not None):
            self.index = int(index)
        else:
            self.index = None
