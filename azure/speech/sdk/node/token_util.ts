import axios, { AxiosResponse } from 'axios';
import Cookie from 'universal-cookie';

const speechKey = process.env.SPEECH_KEY;
const speechRegion = process.env.SPEECH_REGION;

interface TokenSuccess {
    authToken: string;
    region: string;
}

interface TokenError {
    authToken: null;
    error: any;
}

type TokenResult = TokenSuccess | TokenError;

export async function getTokenOrRefresh(): Promise<TokenResult> {
    const cookie = new Cookie();
    const speechToken: string | undefined = cookie.get('speech-token');
    
    if (speechToken === undefined) {
        try {
            const headers = {
                headers: {
                    'Ocp-Apim-Subscription-Key': speechKey,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            };
            const tokenResponse: AxiosResponse = await axios.post(
                `https://${speechRegion}.api.cognitive.microsoft.com/sts/v1.0/issueToken`,
                null,
                headers
            );
            const { token, region } = { token: tokenResponse.data, region: speechRegion };
            cookie.set('speech-token', `${region}:${token}`, { maxAge: 540, path: '/' });

            console.log('Token fetched from back-end: ' + token);
            return { authToken: token, region };
        } catch (err: any) {
            console.log(err.response.data);
            return { authToken: null, error: err.response.data };
        }
    } else {
        console.log('Token fetched from cookie: ' + speechToken);
        const idx = speechToken.indexOf(':');
        return {
            authToken: speechToken.slice(idx + 1),
            region: speechToken.slice(0, idx)
        };
    }
}