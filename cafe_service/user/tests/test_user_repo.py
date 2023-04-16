import pytest
from user.repository import UserRepo
from exceptions import NotFoundError


@pytest.mark.django_db
def test_user_repo():
    repo = UserRepo()

    # Test create method
    created_user = repo.create(phone="01012341234", password="password", name="John")
    assert created_user["phone"] == "01012341234"
    assert created_user["name"] == "John"

    # Test get methods
    user_id = created_user["id"]
    retrieved_user = repo.get(user_id=user_id)
    assert retrieved_user["id"] == user_id
    assert retrieved_user["phone"] == "01012341234"
    assert retrieved_user["name"] == "John"

    retrieved_user_by_phone = repo.get_by_phone(phone="01012341234")
    assert retrieved_user_by_phone["id"] == user_id
    assert retrieved_user_by_phone["phone"] == "01012341234"
    assert retrieved_user_by_phone["name"] == "John"

    retrieved_user_ins = repo.get_user_ins(user_id=user_id)
    assert retrieved_user_ins.id == user_id
    assert retrieved_user_ins.phone == "01012341234"
    assert retrieved_user_ins.name == "John"

    # Test not found exceptions
    invalid_user_id = user_id + 1
    try:
        repo.get(user_id=invalid_user_id)
        assert False, "NotFoundError not raised"
    except NotFoundError:
        pass

    try:
        repo.get_user_ins(user_id=invalid_user_id)
        assert False, "NotFoundError not raised"
    except NotFoundError:
        pass
