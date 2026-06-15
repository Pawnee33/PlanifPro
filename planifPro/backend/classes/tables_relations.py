from planifPro import db

eleve_classe = db.Table(
    'eleve_classe',
    db.Column('eleve_id', db.String(36), db.ForeignKey('eleves.utilisateur_id')),
    db.Column('classe_id', db.String(36), db.ForeignKey('classes.id')),
    db.Column('duree_minutes', db.Integer, nullable=True)
)

eleve_evenement = db.Table(
    'eleve_evenement',
    db.Column('eleve_id', db.String(36), db.ForeignKey('eleves.utilisateur_id')),
    db.Column('evenement_id', db.String(36), db.ForeignKey('evenements.id'))
)
