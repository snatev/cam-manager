from cam_manager.cam_info import CamInfoMixin
from cam_manager.cam_control import CamControlMixin
from cam_manager.cam_effects import CamEffectsMixin

class CamManager(CamInfoMixin, CamControlMixin, CamEffectsMixin):
    def __init__(self, is_ai=False):
        super().__init__()

        self.cams = {}
        self.active_cam_id = None

        if is_ai:
            from cam_manager.cam_ai import CamAIMixin
            self.ai = CamAIMixin()
        else: self.ai = None
