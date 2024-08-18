import http from "http";
import { transcribe } from "./transcribe";

http
    .createServer((req, res: http.ServerResponse) => {    
        res.writeHead(200, { "Content-Type": "text/plain" });
        res.write(transcribe("Bobae"));
        res.end();
    })
    .listen(8080);

console.log("Server running at port 8080");