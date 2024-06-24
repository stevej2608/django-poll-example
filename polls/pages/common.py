from __future__ import annotations

from typing import  Awaitable, Callable,overload
from reactpy_django.types import FuncParams, Inferred, Query, QueryOptions

import reactpy_django

class LoadingException(Exception):
    pass


@overload
def use_query(
    options: QueryOptions,
    /,
    query: Callable[FuncParams, Awaitable[Inferred]] | Callable[FuncParams, Inferred],
    *args: FuncParams.args,
    **kwargs: FuncParams.kwargs,
) -> Query[Inferred]: ...


@overload
def use_query(
    query: Callable[FuncParams, Awaitable[Inferred]] | Callable[FuncParams, Inferred],
    *args: FuncParams.args,
    **kwargs: FuncParams.kwargs,
) -> Query[Inferred]: ...


def use_query(*args, **kwargs) -> Query[Inferred]:
    qs = reactpy_django.hooks.use_query(*args, **kwargs)

    if qs.error:
        raise LoadingException(f"Error when loading - {qs.error}")
    elif qs.data is None:
        raise LoadingException("Loading...")

    return qs
 