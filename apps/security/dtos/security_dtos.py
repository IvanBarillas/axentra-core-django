# apps/security/dtos/security_dtos.py
import uuid
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional

class RoleReadOnlyDTO(BaseModel):
    """
    CONTRATO INMUTABLE DE LECTURA (GET):
    Mapea de forma segura los permisos activos por usuario para consumo del decorador y la UX.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    user_email: str
    app_id: int
    app_name: str
    app_slug: str
    role: str
    role_display: str
    is_active: bool
    permissions_list: Optional[List[str]] = Field(default_factory=list)

    @field_validator('permissions_list', mode='before')
    @classmethod
    def asegurar_lista_valida(cls, value):
        return value if value is not None else []


