import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db import make_session    
from db.repositories.medicamento import MedicamentoRepo
from db.repositories.farmacia import FarmaciaRepo
from db.repositories.oferta import OfertaRepo

engine, db = make_session()          

med_repo = MedicamentoRepo(db)
far_repo = FarmaciaRepo(db)
oferta_repo = OfertaRepo(db)

def get_ofertas_by_med_id_list(list_ids):
  for id in list_ids:
    print(oferta_repo.list_by_medicamento(id))
