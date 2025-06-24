from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

import vendee_globe_api.constants as c


class Settings(BaseSettings):
    """Settings for the GenAI Escape Game API."""

    timer: int = Field(description="Time at which the API delivers full data")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(
                settings_cls=settings_cls, yaml_file=c.root_dir / "config.yaml"
            ),
            init_settings,
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )


settings: Settings = Settings()
