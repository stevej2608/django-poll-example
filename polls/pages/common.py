from __future__ import annotations
from typing import Awaitable, Callable,overload
from reactpy_django.types import FuncParams, Inferred, QueryOptions
import reactpy_django

from utils.params import ParamsBase


class Params(ParamsBase):
    pk: int


class LoadingException(Exception):
    pass

@overload
def use_query(
    options: QueryOptions,
    /,
    query: Callable[FuncParams, Awaitable[Inferred]] | Callable[FuncParams, Inferred],
    *args: FuncParams.args,
    **kwargs: FuncParams.kwargs,
) -> Inferred: ...


@overload
def use_query(
    query: Callable[FuncParams, Awaitable[Inferred]] | Callable[FuncParams, Inferred],
    *args: FuncParams.args,
    **kwargs: FuncParams.kwargs,
) -> Inferred: ...


def use_query(*args, **kwargs) -> Inferred:
    qs = reactpy_django.hooks.use_query(*args, **kwargs)

    if qs.error:
        raise LoadingException(f"Error when loading - {qs.error}")
    elif qs.data is None:
        raise LoadingException("Loading...")

    return qs.data
 