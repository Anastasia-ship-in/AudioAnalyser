from .models import Task, Prompt, db


def create_task_with_prompts(title, audio_link, user_id, prompts):
    new_task = Task(title=title, audio_link=audio_link, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

    for prompt_text in prompts:
        new_prompt = Prompt(content=prompt_text, task_id=new_task.id)
        db.session.add(new_prompt)

    db.session.commit()
    return new_task


def update_task_with_prompts(task_id, title=None, new_prompts=None):
    task = Task.query.get_or_404(task_id)

    if title:
        task.title = title

    if new_prompts:
        db.session.query(Prompt).filter(Prompt.task_id == task_id).delete()
        for prompt_text in new_prompts:
            new_prompt = Prompt(content=prompt_text, task_id=task_id)
            db.session.add(new_prompt)

    db.session.commit()
    return task
