import pathlib as plib
import sys

class WorkingDirs:
    @staticmethod
    def base_path():
        return plib.Path.home().resolve()

    @classmethod
    def installed(cls):
        return plib.Path(sys.executable).parent

    @classmethod
    def app_data(cls, app_name: str):
        return cls.base_path() / 'APPDATA' / app_name

    @classmethod
    def global_assets(cls, prog_radic: plib.Path | str):
        if isinstance(prog_radic, str):
            prog_radic = cls.app_data(prog_radic)
        return prog_radic / 'assets'

    @classmethod
    def image_assets(cls, assets_radic: plib.Path | str):
        if isinstance(assets_radic, str):
            assets_radic = cls.global_assets(assets_radic)
        return assets_radic / 'images'

    @classmethod
    def avatar_assets(cls, images_radic: plib.Path | str):
        if isinstance(images_radic, str):
            images_radic = cls.image_assets(images_radic)
        return images_radic / 'avatars'
