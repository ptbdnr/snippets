
import { transcribe } from "../src/transcribe";

test('should return a transcription', () => {
    const path_to_wav_file = 'foo';
    expect(transcribe(path_to_wav_file)).toBe('good');
});