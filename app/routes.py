from flask import Blueprint, jsonify, request
from .models import Task, Prompt, db
from .audio_analysis import process_audio

bp = Blueprint('routes', __name__)


# GET: Отримання інформації по тасці за її ID
@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_data = {
        'id': task.id,
        'title': task.title,
        'audio_link': task.audio_link,
        'prompts': [prompt.content for prompt in task.prompts]
    }
    return jsonify(task_data)


# POST: Створення нової таски та додавання списку промптів
@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    audio_link = data.get('audio_link')
    title = data.get('title')
    user_id = data.get('user_id')

    # Аналіз аудіо та розбиття на промпти
    prompts = process_audio(audio_link)

    new_task = Task(title=title, audio_link=audio_link, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

    for prompt_text in prompts:
        new_prompt = Prompt(content=prompt_text, task_id=new_task.id)
        db.session.add(new_prompt)

    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201


# PUT: Оновлення промптів або назви
@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = Task.query.get_or_404(task_id)

    if 'title' in data:
        task.title = data['title']

    if 'prompts' in data:
        # Оновлення промптів
        db.session.query(Prompt).filter(Prompt.task_id == task_id).delete()
        for prompt_text in data['prompts']:
            new_prompt = Prompt(content=prompt_text, task_id=task_id)
            db.session.add(new_prompt)

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})


# DELETE: Видалення таски
@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})
