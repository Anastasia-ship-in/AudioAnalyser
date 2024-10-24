import unittest
from unittest.mock import patch, MagicMock
from app.audio_analysis import transcribe_audio, generate_prompts, process_audio


class TestTranscribeAudio(unittest.TestCase):
    @patch('your_module.whisper.load_model')
    def test_transcribe_audio(self, mock_load_model):
        # Мок даних
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {'text': 'This is a test transcription.'}
        mock_load_model.return_value = mock_model

        audio_link = 'sf8.mp3'
        result = transcribe_audio(audio_link)

        mock_model.transcribe.assert_called_with(audio_link)
        self.assertEqual(result, 'This is a test transcription.')


class TestGeneratePrompts(unittest.TestCase):
    def test_generate_prompts(self):
        transcribed_text = "Barack Obama was born in Hawaii."
        expected_prompts = [
            'Generate an image related to PERSON: Barack Obama',
            'Generate an image related to GPE: Hawaii'
        ]

        result = generate_prompts(transcribed_text)
        self.assertEqual(result, expected_prompts)


class TestProcessAudio(unittest.TestCase):
    @patch('your_module.transcribe_audio')
    @patch('your_module.generate_prompts')
    def test_process_audio(self, mock_generate_prompts, mock_transcribe_audio):
        # Мок для транскрипції
        mock_transcribe_audio.return_value = "This is a test transcription."

        # Мок для генерації промптів
        mock_generate_prompts.return_value = [
            'Generate an image related to TEST: This is a test transcription.'
        ]

        audio_link = 'test_audio.mp3'
        result = process_audio(audio_link)

        mock_transcribe_audio.assert_called_with(audio_link)
        mock_generate_prompts.assert_called_with("This is a test transcription.")
        self.assertEqual(result, ['Generate an image related to TEST: This is a test transcription.'])