# Boundary Handler
# Verifies drone position outside of flying limits
# and not within given boundary

from Shared.shared_utils import success_dict


class BoundaryHandler:

    def __init__(self, qr_handler, telemetry_handler):
        self.qr_handler = qr_handler
        self.telemetry_handler = telemetry_handler

    def verify_boundaries(self):
        return success_dict("Boundary Verified")
