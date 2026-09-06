from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CurrencyBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    symbol: Optional[str] = None
    decimal_places: int


class CurrencyRetrieveSchema(CurrencyBaseSchema):
    pass
