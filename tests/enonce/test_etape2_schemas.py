import pytest
from pydantic import ValidationError

try:
    from app.schemas.person import PersonBase, PersonRead
    from app.schemas.participant import ParticipantCreate, ParticipantRead, ParticipantUpdate
    from app.schemas.opinion import OpinionBase, OpinionCreate, OpinionRead
    from app.schemas.member import MemberRead

    SCHEMAS_LOADED = True
except ImportError as e:
    print(f"Échec de l'import des schémas : {e}")
    SCHEMAS_LOADED = False


@pytest.mark.skipif(not SCHEMAS_LOADED, reason="Schémas (Person, Participant, Opinion) non trouvés ou import échoué")
def test_person_schemas():
    """Teste les schémas Person (Base et Read) - TODO Étape 2."""
    person_data = {"first_name": "John", "last_name": "Doe"}
    base = PersonBase(**person_data)
    assert base.last_name == "Doe"

    read = PersonRead(id=1, **person_data)
    assert read.id == 1


@pytest.mark.skipif(not SCHEMAS_LOADED, reason="Schémas (Person, Participant, Opinion) non trouvés ou import échoué")
def test_participant_schemas():
    """Teste les schémas Participant (Create, Update, Read) - TODO Étape 2."""
    participant_data = {"first_name": "Jane", "last_name": "Smith"}
    create = ParticipantCreate(**participant_data)
    assert create.last_name == "Smith"

    update_data = {"first_name": "Janet"}
    update = ParticipantUpdate(**update_data)
    assert update.first_name == "Janet"
    assert update.last_name is None

    # Teste que des champs inconnus lèvent une erreur (extra="forbid")
    with pytest.raises(ValidationError):
        ParticipantUpdate(first_name="Test", unknown_field="error")


@pytest.mark.skipif(not SCHEMAS_LOADED, reason="Schémas (Person, Participant, Opinion) non trouvés ou import échoué")
def test_opinion_schemas():
    """Teste les schémas Opinion (Base, Create, Read) - TODO Étape 2."""
    opinion_data = {"note": 5, "comment": "Excellent!"}
    base = OpinionBase(**opinion_data)
    assert base.note == 5

    create_data = {"member_id": 1, **opinion_data}
    create = OpinionCreate(**create_data)
    assert create.member_id == 1

    # Mock d'un membre pour le schéma de lecture
    mock_member = MemberRead(id=1, login="testuser")
    read_data = {"id": 10, "movie_id": 20, "member": mock_member, **opinion_data}
    read = OpinionRead(**read_data)
    assert read.id == 10
    assert read.member.login == "testuser"