import asyncio, json, struct, aiohttp

PORT = 9877
MODULE = "Teach"
MODEL_NAME = "teach-ai"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

async def call_ollama(prompt: str) -> str:
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(OLLAMA_URL, json=payload) as resp:
            data = await resp.json()
            return data.get("response", "")

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[{MODULE}] Assessment pipeline connected from {addr}", flush=True)
    try:
        while True:
            header = await reader.readexactly(4)
            length = struct.unpack('!I', header)[0]
            raw = await reader.readexactly(length)
            message = json.loads(raw.decode('utf-8'))

            method = message.get("method", "")
            params = message.get("params", {}) or {}
            prompt = params.get("prompt", "")

            try:
                text = await call_ollama(prompt)
                result = {"module": MODULE, "status": "EVAL_READY", "method": method, "response": text}
            except Exception as e:
                result = {"module": MODULE, "status": "ERROR", "method": method, "error": str(e)}

            response_payload = {"jsonrpc": "2.0", "id": message.get("id"), "result": result}
            res_bytes = json.dumps(response_payload).encode('utf-8')
            writer.write(struct.pack('!I', len(res_bytes)) + res_bytes)
            await writer.drain()
    except (asyncio.IncompleteReadError, ConnectionResetError):
        pass
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', PORT)
    print(f"[{MODULE}] Real IPC active on 127.0.0.1:{PORT}", flush=True)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
