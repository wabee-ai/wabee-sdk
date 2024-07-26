import ast
import copy
import json
import os
import re
from contextlib import redirect_stdout
from io import StringIO

import numpy as np
import pandas as pd
import RestrictedPython as rp  # type: ignore

pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 50)
pd.set_option("display.min_rows", 50)
import matplotlib.pyplot as plt  # noqa: E402

CHECK_IMPORT_OS = re.compile(r"(?<![\d\w])os(?=\.)")
_ALLOWED_MODULES = frozenset(
    json.loads(os.getenv("WABEE_AGENT_TOOLS_ALLOWED_MODULES", "[]"))
)


def _safe_import(name, *args, **kwargs):
    if name.split(".")[0] not in _ALLOWED_MODULES:
        raise ImportError(
            f"Importing {name!r} is not allowed in the sandboxed environment."
        )
    return __import__(name, *args, **kwargs)


def _safe_write(df):
    if isinstance(df, pd.DataFrame):
        return df
    else:
        raise Exception("Not allowed _write_ to this object", df)


_ALLOWED_GLOBALS = {
    "__builtins__": {
        **rp.safe_builtins,
        "__import__": _safe_import,
        "_getiter_": rp.Eval.default_guarded_getiter,
        "_getitem_": rp.Eval.default_guarded_getitem,
        "__getattr__": getattr,  # Unguarded
        "__setattr__": setattr,
        "__iter_unpack_sequence__": rp.Guards.guarded_iter_unpack_sequence,
        "dict": dict,
        "list": list,
        "print": print,
        "sum": sum,
        "_write_": _safe_write,
    },
}


class UnsafeCodeError(Exception):
    pass


class PythonExecutionHandler:
    def __init__(self, user_df: pd.DataFrame | None = None):
        if type(user_df) is pd.DataFrame:
            self.globals = {
                **copy.copy(_ALLOWED_GLOBALS),
                **{"df": user_df, "pd": pd, "np": np, "plt": plt},
            }
        else:
            self.globals = {**copy.copy(_ALLOWED_GLOBALS)}
        self.allowed_modules = _ALLOWED_MODULES

    def _check_security(self, query: str):
        if CHECK_IMPORT_OS.findall(query):
            raise UnsafeCodeError(
                "Using any method from the `os` module is not allowed in this sandbox enviroment."
            )

    def run(self, code: str):
        self._check_security(code)
        tree = ast.parse(code)

        print_msgs = []
        for module in tree.body:
            if isinstance(module, ast.Expr) and "print" in ast.unparse(module):
                io_buffer = StringIO()
                with redirect_stdout(io_buffer):
                    code_obj = compile(ast.Interactive([module]), "<string>", "single")
                    eval(code_obj, self.globals)  # nosec: B307
                    print_msgs.append(io_buffer.getvalue())
            else:
                code_obj = compile(ast.Interactive([module]), "<string>", "single")
                exec(code_obj, self.globals)  # nosec: B102
        return print_msgs
