import os
from pydantic import validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging


class UrlSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                    env_file_encoding='utf-8', 
                                    env_prefix="URL_", 
                                    extra='ignore')

    absortion_column: str
    compressor: str
    distillator_column: str
    heat_exchanger: str
    valve_joule_thompson: str

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                    env_file_encoding='utf-8', 
                                    env_prefix="APP_", 
                                    extra='ignore')

    secret_key: str
    debug:str

class AzureSqlSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                      env_file_encoding='utf-8', 
                                      env_prefix="AZURE_SQL_", 
                                      extra='ignore')
    SERVER: str
    DATABASE: str
    USERNAME: str
    PASSWORD: str
    DRIVER: str
   

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                    env_file_encoding='utf-8', 
                                    extra='ignore')

    url_settings: UrlSettings = UrlSettings()
    app_settings: AppSettings = AppSettings()
    azure_settings: AzureSqlSettings = AzureSqlSettings()

settings = Settings()
