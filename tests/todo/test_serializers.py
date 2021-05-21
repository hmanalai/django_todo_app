from todo.serializers import TodoSerializer

def test_todo_serializers():
    valid_serializer_data = {
        "task": "Water the plants",
        "priority": "Important",
        "status": False
    }
    serializer = TodoSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_todo_serializer():
    invalid_serializer_data = {
        "task": None,
        "priority": "Important",
    }
    serializer = TodoSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {'task': ['This field may not be null.']}