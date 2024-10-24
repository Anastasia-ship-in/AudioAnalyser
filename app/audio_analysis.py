import librosa


def process_audio(audio_link):
    # Завантажуємо аудіо файл
    y, sr = librosa.load(audio_link, sr=None)

    # Тут можна додати логіку для аналізу аудіо та розбиття на сегменти або промпти
    # Для спрощення, ми будемо розбивати аудіо на рівні частини кожні 10 секунд.

    duration = librosa.get_duration(y=y, sr=sr)
    prompts = []

    segment_duration = 10  # Розбивка на кожні 10 секунд
    for i in range(0, int(duration), segment_duration):
        prompt_text = f'Audio segment from {i} to {i + segment_duration} seconds.'
        prompts.append(prompt_text)

    return prompts
