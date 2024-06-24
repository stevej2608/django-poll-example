from __future__ import annotations
from typing import Type, TypeVar
from pydantic import BaseModel
import reactpy_router


DataModel = TypeVar('DataModel', bound=BaseModel)

class ParamsBase(BaseModel):

    @classmethod
    def from_slug(cls: Type[DataModel]) -> DataModel:
        """Use slug params to polulate a Pydantic model"""

        params = reactpy_router.use_params()
        return cls(**params)
