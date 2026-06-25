from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.db.models import CCTP
from src.export.docx_generator import markdown_to_docx

router = APIRouter(tags=["export"])


class CabinetInfo(BaseModel):
    nomCabinet: str | None = None
    adresse: str | None = None
    telephone: str | None = None
    email: str | None = None
    siteWeb: str | None = None
    logo: str | None = None
    logoMime: str | None = None


class ExportRequest(BaseModel):
    cabinet: CabinetInfo | None = None


@router.post("/cctp/{cctp_id}/export")
async def export_cctp_docx(cctp_id: str, req: ExportRequest = ExportRequest(), db: AsyncSession = Depends(get_db)):
    cctp = await db.get(CCTP, cctp_id)
    if not cctp:
        raise HTTPException(status_code=404, detail="CCTP introuvable")

    cabinet = req.cabinet.model_dump() if req.cabinet else None
    title = f"CCTP — Lot {cctp.lot_numero} — {cctp.lot_nom}"
    buffer = markdown_to_docx(title, cctp.content, cabinet=cabinet)
    filename = f"CCTP_Lot{cctp.lot_numero}_{cctp.lot_nom.replace(' ', '_')}.docx"

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
