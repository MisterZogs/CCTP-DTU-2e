from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.db.models import CCTP, Project
from src.llm.base import CCTPParams
from src.llm.factory import get_provider
from src.lot_mapping.mapping import get_lot_label
from src.prompts.system import SYSTEM_PROMPT
from src.prompts.lot import build_user_prompt
from src.rag.retriever import retrieve_dtu_context

router = APIRouter(tags=["cctp"])


class GenerateRequest(BaseModel):
    lot_key: str
    lot_numero: str
    provider: Literal["claude", "mistral"] | None = None


class CCTPUpdate(BaseModel):
    content: str


class CCTPResponse(BaseModel):
    id: str
    project_id: str
    lot_numero: str
    lot_nom: str
    content: str
    provider: str
    model: str

    model_config = {"from_attributes": True}


@router.post("/projects/{project_id}/cctp", response_model=CCTPResponse, status_code=201)
async def generate_cctp(
    project_id: str,
    req: GenerateRequest,
    db: AsyncSession = Depends(get_db),
):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projet introuvable")

    lot_nom = get_lot_label(req.lot_key)
    params = CCTPParams(
        lot_numero=req.lot_numero,
        lot_nom=lot_nom,
        type_projet=project.type_projet,
        usage=project.usage,
        type_erp=project.type_erp or "",
        zone_climatique=project.zone_climatique,
        zone_sismique=project.zone_sismique,
        pmr=project.pmr,
        specificites=project.specificites,
    )

    query = f"CCTP {lot_nom} {project.type_projet} {project.usage}"
    dtu_context = retrieve_dtu_context(req.lot_key, query)

    provider = get_provider(req.provider)
    user_prompt = build_user_prompt(params, dtu_context)
    content = await provider.generate(SYSTEM_PROMPT, user_prompt)

    cctp = CCTP(
        project_id=project_id,
        lot_numero=req.lot_numero,
        lot_nom=lot_nom,
        content=content,
        provider=provider.provider_name,
        model=provider.model_name,
    )
    db.add(cctp)
    await db.commit()
    await db.refresh(cctp)
    return cctp


@router.get("/projects/{project_id}/cctp", response_model=list[CCTPResponse])
async def list_cctps(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CCTP).where(CCTP.project_id == project_id).order_by(CCTP.lot_numero)
    )
    return result.scalars().all()


@router.get("/cctp/{cctp_id}", response_model=CCTPResponse)
async def get_cctp(cctp_id: str, db: AsyncSession = Depends(get_db)):
    cctp = await db.get(CCTP, cctp_id)
    if not cctp:
        raise HTTPException(status_code=404, detail="CCTP introuvable")
    return cctp


@router.put("/cctp/{cctp_id}", response_model=CCTPResponse)
async def update_cctp(cctp_id: str, data: CCTPUpdate, db: AsyncSession = Depends(get_db)):
    cctp = await db.get(CCTP, cctp_id)
    if not cctp:
        raise HTTPException(status_code=404, detail="CCTP introuvable")
    cctp.content = data.content
    await db.commit()
    await db.refresh(cctp)
    return cctp


@router.delete("/cctp/{cctp_id}", status_code=204)
async def delete_cctp(cctp_id: str, db: AsyncSession = Depends(get_db)):
    cctp = await db.get(CCTP, cctp_id)
    if not cctp:
        raise HTTPException(status_code=404, detail="CCTP introuvable")
    await db.delete(cctp)
    await db.commit()
