def calcul_interets_composes(versement_annuel: float, taux_annuel: float, duree_annees: int) -> float:
    """
    Calcule le montant accumulé par un placement à intérêts composés.
    
    La formule utilisée est: montant(n+1) = (montant(n) + versement_annuel) * (1 + taux_annuel)
    
    Args:
        versement_annuel (float): Montant versé chaque année
        taux_annuel (float): Taux d'intérêt annuel (ex: 0.03 pour 3%)
        duree_annees (int): Durée du placement en années
        
    Returns:
        float: Montant total accumulé après la durée spécifiée
    """
    montant = 0
    
    for _ in range(duree_annees):
        montant = (montant + versement_annuel) * (1 + taux_annuel)
        
    return montant