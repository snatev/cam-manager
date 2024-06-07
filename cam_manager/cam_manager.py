from cam_manager.cam_info import CamInfoMixin
from cam_manager.cam_control import CamControlMixin
from cam_manager.cam_effects import CamEffectsMixin
from cam_manager.cam_settings import CamSettingsMixin

class CamManager(CamInfoMixin, CamControlMixin, CamEffectsMixin, CamSettingsMixin):
    """A comprehensive class for managing cameras, including AI-based features, control, effects, and settings."""

    def __init__(self, is_ai=False, ai_mode="detection", load_settings=False):
        """
        Initialize the CamManager class.

        Parameters:
            is_ai (bool, optional): Whether to enable AI features. Default is False.
            ai_mode (str, optional): The AI mode to use ('detection', 'segmentation', 'classify', 'pose').
            load_settings (bool, optional): Whether to load camera settings from a file. Default is False.
        """

        possible_ai_modes = ["detection", "segmentation", "classify", "pose"]

        if ai_mode not in possible_ai_modes:
            ai_mode = "detection"
            print(f"Invalid AI mode, using default - {ai_mode}")

        super().__init__()

        self.cams = {}
        self.fake_cams = {}
        self.active_cam_id = None
        self.load_settings = load_settings

        if is_ai:
            from cam_manager.cam_ai import CamAIMixin
            self.ai = CamAIMixin(ai_mode)
        else: self.ai = None
