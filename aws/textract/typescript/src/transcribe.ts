import {
    TranscribeClient,
    StartTranscriptionJobCommand,
    GetTranscriptionJobCommand,
  } from "@aws-sdk/client-transcribe";
  
  
  const REGION = process.env.REGION
  const OUTPUT_BUCKET_NAME = process.env.OUTPUT_BUCKET_NAME
  
  
  export async function transcribe(path_to_input_wav_file: string): Promise<string | null> {
  
    const transcribeClient = new TranscribeClient({ region: REGION });
    const transcribeJobId = '123'
  
    // speech-to-text
    try {    
        // start async speech-to-text job
        const start_response = await transcribeClient.send(    
            new StartTranscriptionJobCommand({
                TranscriptionJobName: transcribeJobId,
                LanguageCode: "en-US",  // For example, 'en-US'
                MediaFormat: "wav",     // For example, 'wav'
                Media: { MediaFileUri: path_to_input_wav_file, },
                OutputBucketName: OUTPUT_BUCKET_NAME,
                OutputKey: `output.json`,
            })
        );
      
        while (true) {
            try {
                const job = await transcribeClient.send(
                    new GetTranscriptionJobCommand({
                    TranscriptionJobName: transcribeJobId,
                    })
                );
                const job_status = job.TranscriptionJob?.TranscriptionJobStatus;
                if (job_status == "COMPLETED" || job_status == "FAILED") {
                    if (job_status == "COMPLETED") {
                        const transcriptFileUrl = job.TranscriptionJob?.Transcript?.TranscriptFileUri;
                        return transcriptFileUrl!
                    } else {
                        console.error("ERROR", job_status);
                        return null;
                        break;
                    }
                } else {
                    console.log(`WAITING for ${transcribeJobId}: ${job_status}`);
                    await new Promise((f) => setTimeout(f, 1000));
                }
            } catch (err) {
                console.error("ERROR", err);
                return null;
            }
        }
    } catch (err) {
        console.error("ERROR", err);
        return null;
    }
  };
  