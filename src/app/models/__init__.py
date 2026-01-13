# app/models/__init__.py

# Eviter les erreurs liés à l'importation circulaire
# Exemple : sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[Movie(movies)], expression 'Genre' failed to locate a name ('Genre'). If this is a class name, consider adding this relationship() to the <class 'app.models.film.Film'> class after both dependent classes have been defined

from .base_class import Base
from .genre import Genre
from .member import Member
from .movie import Movie
from .opinion import Opinion
from .participant import Participant
from .person import Person

# L'import des associations (ex : personnefilm) n'est en général pas nécessaire ici car elles sont gérées dans les modèles eux-mêmes