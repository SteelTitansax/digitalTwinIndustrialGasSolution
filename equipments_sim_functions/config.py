from pydantic_settings import BaseSettings, SettingsConfigDict

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
    
"""
class CosmosDBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                      env_file_encoding='utf-8', 
                                      env_prefix="COSMOS_DB_", 
                                      extra='ignore')
    ENDPOINT: str
    KEY: str
    DATABASE: str
    CONTAINER: str
"""
class Settings(BaseSettings):
    azure_sql: AzureSqlSettings = AzureSqlSettings()
    #cosmosdb: CosmosDBSettings = CosmosDBSettings()

settings = Settings()
