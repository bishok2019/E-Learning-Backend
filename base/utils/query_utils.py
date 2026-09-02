from typing import Any, Dict, List, Optional, Type

from sqlalchemy import or_
from sqlalchemy.orm import Query, Session, selectinload
from sqlalchemy.sql.sqltypes import String

from base.pagination import paginate
from base.route import StandardResponse

# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------


def apply_eager_loads(query: Query, relationships: List) -> Query:
    """Wrap each relationship attribute in selectinload and apply to query."""
    if relationships:
        query = query.options(*[selectinload(rel) for rel in relationships])
    return query


# ---------------------------------------------------------------------------
# Result enrichment
# ---------------------------------------------------------------------------


def enrich_with_related(
    items: List[Dict],
    db_items: List[Any],
    mappings: Dict[str, Any],
) -> None:
    """
    Mutate serialised dicts in-place with values from related ORM objects.

    ``mappings`` values can be either a dotted string or a tuple of strings —
    both resolve the same attribute chain on the ORM object:

        {"category_name": "category.name"}   # dotted string (preferred)
        {"category_name": ("category", "name")}  # legacy tuple (still works)
    """
    for item, db_item in zip(items, db_items):
        for key, path in mappings.items():
            parts = path.split(".") if isinstance(path, str) else list(path)
            value = db_item
            for part in parts:
                value = getattr(value, part, None) if value is not None else None
            item[key] = value


def apply_filters(query: Query, filters: Dict[Any, Any]) -> Query:
    """
    Apply exact-match filters to a query, skipping None values.

    filters: {Model.column: value}, e.g. {Course.category_id: category_id}
    Works with columns from any joined entity, not just the base model.
    """
    for column, value in filters.items():
        if value is not None:
            query = query.filter(column == value)
    return query


def apply_search(query: Query, columns: List, search: Optional[str]) -> Query:
    """
    Apply case-insensitive ILIKE search across the given columns.

    columns: [Course.name, Course.description] — actual column refs,
    so this works across joined tables too.
    """
    if not search or not columns:
        return query

    clauses = []
    for column in columns:
        col = getattr(getattr(column, "property", None), "columns", [None])[0]
        if col is None or not isinstance(col.type, String):
            continue
        clauses.append(column.ilike(f"%{search}%"))

    if clauses:
        query = query.filter(or_(*clauses))
    return query


# ---------------------------------------------------------------------------
# Generic handler
# ---------------------------------------------------------------------------


def generic_list_handler(
    *,
    query: Query,
    schema: Type,
    pagination,
    search: Optional[str] = None,
    search_fields: Optional[List] = None,
    filters: Optional[Dict[Any, Any]] = None,
    eager_loads: Optional[List] = None,
    related_mappings: Optional[Dict[str, str]] = None,
    message: str = "Fetched successfully",
) -> StandardResponse:
    """
    Generic paginated list handler with search, filtering, and relationship
    enrichment — operates on a caller-supplied query, so joins, filters and
    search columns can come from any entity in that query.
    """
    query = apply_filters(query, filters or {})
    query = apply_search(query, search_fields or [], search)
    query = apply_eager_loads(query, eager_loads or [])

    result = paginate(query=query, pagination=pagination, schema=schema)

    if related_mappings:
        offset = (pagination.page - 1) * pagination.page_size
        db_items = query.offset(offset).limit(pagination.page_size).all()
        enrich_with_related(result.data, db_items, related_mappings)

    return StandardResponse.success_response(
        data=result.data,
        message=message,
        meta=result.meta,
    )
