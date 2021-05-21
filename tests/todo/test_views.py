from django.http import response
import json 
import pytest
from todo.models import Todo


@pytest.mark.django_db
def test_add_task(client):
    tasks = Todo.objects.all()
    assert len(tasks) == 0 

    response = client.post(
        '/api/tasks/',
        {
            'task': 'Water the plants',
            'priority': 'Important',
            'status': False,
        },
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.data['task'] == 'Water the plants'

    tasks = Todo.objects.all()
    assert len(tasks) == 1


@pytest.mark.django_db
def test_add_task_invalid_json(client):
    tasks = Todo.objects.all()
    assert len(tasks)== 0 

    response = client.post(
        '/api/tasks/', 
        {},
        content_type='application/json'
    )
    assert response.status_code == 400

    tasks = Todo.objects.all()
    assert len(tasks) == 0 


@pytest.mark.django_db
def test_add_task_invalid_json_keys(client):
    tasks = Todo.objects.all()
    assert len(tasks) == 0 

    response = client.post(
        '/api/tasks/', 
        {
            'title': 'Water the plants',
            'priority': 'Important',
        },
        content_type='application/json'
    )
    assert response.status_code == 400 

    tasks = Todo.objects.all()
    assert len(tasks) == 0


@pytest.mark.django_db
def test_get_single_task(client, add_task):
    task = add_task(task='Water the plants before they die', priority='Important', status=False)
    response = client.get(f'/api/tasks/{task.id}/')
    assert response.status_code == 200 
    assert response.data['task'] == 'Water the plants before they die'

def test_get_single_task_incorrect_id(client):
    response = client.get(f'/api/tasks/foo/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_all_tasks(client, add_task):
    task_0 = add_task(task='Water the plants', priority='Important', status=False)
    task_1 = add_task(task='Prepare for exam', priority='Critical', status=False)
    response = client.get(f'/api/tasks/')
    assert response.status_code == 200 
    assert response.data[0]['task'] == 'Water the plants'
    assert response.data[1]['task'] == 'Prepare for exam'


@pytest.mark.django_db
def test_delete_single_task(client, add_task):
    task = add_task(task='Water the plants', priority='Important', status=False)

    response = client.get(f'/api/tasks/{task.id}/')
    assert response.status_code == 200
    assert response.data['task'] == 'Water the plants'

    delete_response = client.delete(f'/api/tasks/{task.id}/')
    assert delete_response.status_code == 204
    
    get_response = client.get(f'/api/tasks/')
    assert get_response.status_code == 200
    assert len(get_response.data) == 0


@pytest.mark.django_db
def test_delete_single_task_incorrect_id(client):
    response = client.get(f'/api/tasks/200/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_task(client, add_task):
    task = add_task(task='Water the plants', priority='Important', status=False)

    update_response = client.put(
        f'/api/tasks/{task.id}/',
        {
            'task':'do laundry', 
            'priority':'low', 
            'status': False
        },
        content_type='application/json',
    )
    assert update_response.status_code == 200
    assert update_response.data['task'] == 'do laundry'
    assert update_response.data['priority'] == 'low'

    get_response = client.get(f'/api/tasks/{task.id}/')
    assert get_response.status_code == 200
    assert get_response.data['task'] == 'do laundry'
    assert get_response.data['priority'] == 'low'

@pytest.mark.django_db
def test_update_task_incorrect_id(client):
    response = client.put(f'/api/tasks/200/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_task_incorrect_json(client, add_task):
    task = add_task(task='Water the plants', priority='Important', status=False)

    update_response = client.put(
        f'/api/tasks/{task.id}/',
        {},
        content_type='application/json',
    )
    assert update_response.status_code == 400


@pytest.mark.django_db
def test_update_task_incorrect_json_keys(client, add_task):
    task = add_task(task='Water the plants', priority='Important', status=False)

    update_response = client.put(
        f'/api/tasks/{task.id}/',
        {
            'title': 'water the plants',
            'priority': 'low',
        },
        content_type='application/json',
    )
    assert update_response.status_code == 400
