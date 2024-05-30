from cam_manager.cam_info import CamInfoMixin
from cam_manager.cam_control import CamControlMixin
from cam_manager.cam_effects import CamEffectsMixin

class CamManager(CamInfoMixin, CamControlMixin, CamEffectsMixin):
    def __init__(self, is_ai = False, ai_mode = "detection"):
        possible_ai_modes = ["detection", "segmentation"]
        if ai_mode not in possible_ai_modes:
            ai_mode = "detection"
            print(f"Invalid AI mode. Possible values are {possible_ai_modes}")

        super().__init__()

        self.cams = {}
        self.tricky_cams = {}
        self.active_cam_id = None

        if is_ai:
            from cam_manager.cam_ai import CamAIMixin
            self.ai = CamAIMixin(ai_mode)
        else: self.ai = None
