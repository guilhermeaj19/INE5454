from decimal import Decimal
import re
from sqlalchemy.orm import Session

from db.models.medicamento import Medicamento
from db.models.oferta import Oferta
from db.repositories.medicamento import MedicamentoRepo
from db.repositories.farmacia import FarmaciaRepo
from db.repositories.oferta import OfertaRepo

def validate_medicamento(med: Medicamento):
    pattern = re.compile(r"\bkit\b|\bcaixas\b", re.IGNORECASE)

    # Verifica se nome contêm "kit" ou "caixas", indicando plural
    if pattern.search(med.nome):
        return False

    if not med.registro_ms:
        return False
    

    return True

def upsert_medicamento_oferta(
    db: Session,
    *,
    registro_ms: str,
    nome: str,
    marca: str | None = None,
    categoria: str | None = None,
    sub_categoria: str | None = None,
    image_source: str | None = None,
    descricao: str | None = None,
    is_generico: bool = False,
    necessita_prescricao: bool = False,
    farmacia_nome: str,
    preco: Decimal,
    url: str,
) -> Oferta | None:

    med_repo = MedicamentoRepo(db)
    far_repo = FarmaciaRepo(db)
    oferta_repo = OfertaRepo(db)

    med = med_repo.get_by_registro(registro_ms)

    if med is None:
        med = Medicamento(
            registro_ms=registro_ms,
            nome=nome,
            marca=marca,
            categoria=categoria,
            sub_categoria=sub_categoria,
            image_source=image_source,
            descricao=descricao,
            is_generico=is_generico,
            necessita_prescricao=necessita_prescricao,
        )
        if validate_medicamento(med):
            med_repo.add(med)
        else:
            return None

    farma = far_repo.get_or_create(farmacia_nome)

    oferta = oferta_repo.upsert(
        medicamento=med,
        farmacia=farma,
        url=url,
        preco=preco,
    )

    db.commit()
    return oferta
