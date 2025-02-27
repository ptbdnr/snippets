import { getTokenOrRefresh } from './token_util';
import {
    SpeakerAudioDestination,
    SpeechSynthesizer,
    AudioConfig,
    SpeechConfig,
} from 'microsoft-cognitiveservices-speech-sdk';

import speechsdk from 'microsoft-cognitiveservices-speech-sdk';

interface Player {
    p: SpeakerAudioDestination | null;
    muted: boolean;
}

let player: Player = { p: null, muted: false };
let inputText: string = '';

async function textToSpeech(): Promise<void> {
    const tokenObj = await getTokenOrRefresh();
    const { authToken, region } = tokenObj as { authToken: string, region: string };
    const speechConfig: SpeechConfig = SpeechConfig.fromAuthorizationToken(authToken, region);
    const myPlayer: SpeakerAudioDestination = new SpeakerAudioDestination();
    player.p = myPlayer;
    const audioConfig: AudioConfig = AudioConfig.fromSpeakerOutput(myPlayer);

    const synthesizer: SpeechSynthesizer = new SpeechSynthesizer(speechConfig, audioConfig);

    console.log(`Speaking: ${inputText}...`);
    synthesizer.speakTextAsync(
        inputText,
        (result) => {
            let text: string = '';
            if (result.reason === speechsdk.ResultReason.SynthesizingAudioCompleted) {
                text = `Synthesis finished for "${inputText}".`;
            } else if (result.reason === speechsdk.ResultReason.Canceled) {
                text = `Synthesis failed. Error detail: ${result.errorDetails}.`;
            }
            synthesizer.close();
            console.log(text);
        },
        (err) => {
            console.error(`Error: ${err}.`);
            synthesizer.close();
        }
    );
}