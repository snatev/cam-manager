from cam_manager.cam_info import CamInfoMixin
from cam_manager.cam_control import CamControlMixin
from cam_manager.cam_effects import CamEffectsMixin
from cam_manager.cam_settings import CamSettingsMixin

class CamManager(CamInfoMixin, CamControlMixin, CamEffectsMixin, CamSettingsMixin):
    def __init__(self, is_ai = False, ai_mode = "detection", load_settings = False):
        possible_ai_modes = ["detection", "segmentation", "classify", "pose"]
        if ai_mode not in possible_ai_modes:
            ai_mode = "detection"
            print(f"Invalid AI mode. Possible values are {possible_ai_modes}")

        super().__init__()

        self.cams = {}
        self.tricky_cams = {}
        self.active_cam_id = None
        self.load_settings = load_settings

        if is_ai:
            from cam_manager.cam_ai import CamAIMixin
            self.ai = CamAIMixin(ai_mode)
        else: self.ai = None
