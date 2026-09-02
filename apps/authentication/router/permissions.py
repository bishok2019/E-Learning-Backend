from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params
from base.route import StandardResponse
from base.utils.query_utils import generic_list_handler

from ..models import CustomPermission
from ..schema import PermissionBaseSchema

router = APIRouter()


@router.get("/list")
def list_permission(
    search: str = "",
    category_id: int = None,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
    # __: User = Depends(get_current_user),
):
    """List all Permission records with pagination, search, and filters"""

    query = db.query(CustomPermission)

    return generic_list_handler(
        query=query,
        schema=PermissionBaseSchema,
        pagination=pagination,
        search=search,
        search_fields=[
            CustomPermission.name,
            CustomPermission.code_name,
        ],
        filters={
            CustomPermission.category_id: category_id,
        },
    )
