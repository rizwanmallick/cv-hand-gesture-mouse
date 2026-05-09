import numpy as np

class VolumeController:
    def __init__(self):
        from pycaw.pycaw import AudioUtilities

        devices = AudioUtilities.GetSpeakers()
        self.volume = devices.EndpointVolume

        self.current_vol_per = 0

    def set_volume_by_percent(self, vol_per):
        # clamp
        vol_per = max(0, min(100, vol_per))

        # convert to 0.0–1.0
        scalar = vol_per / 100.0

        # ✅ smooth curve (optional, but safe here)
        scalar = scalar ** 1.5

        self.volume.SetMasterVolumeLevelScalar(scalar, None)

        self.current_vol_per = int(scalar * 100)

    def get_current_volume_percent(self):
        scalar = self.volume.GetMasterVolumeLevelScalar()
        return int(scalar * 100)