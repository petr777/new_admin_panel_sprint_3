def model(table_name: str):

    from models import (
        Film_Work,
        Person, Person_Film_Work,
        Genre, Genre_Film_Work
    )

    data_model = {
        'film_work': Film_Work,
        'person': Person,
        'person_film_work': Person_Film_Work,
        'genre': Genre,
        'genre_film_work': Genre_Film_Work,
    }
    return data_model.get(table_name)