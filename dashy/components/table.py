from typing import Optional

from dash import dash_table
import pandas as pd


def table(
    id: str,
    data: pd.DataFrame,
    columns: Optional[list[dict[str, int]]] = None,
    page_size: int = 10
):
    return dash_table.DataTable(data=data, columns=columns, page_size=page_size, id=id)
