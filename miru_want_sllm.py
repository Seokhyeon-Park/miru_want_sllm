import ollama
import asyncio
import websockets

async def eeve(message, websocket):
    try:
        stream = ollama.chat(
            model='eeve:q4',
            messages=[
                {
                    'role': 'User',
                    'content': message,
                }
            ],
            stream=True,
        )

        for chunk in stream:
            print(chunk['message']['content'])
            await websocket.send(chunk['message']['content'])
    
    except Exception as e:
        print(f"Error in eeve: {e}")
        await websocket.send("::ERROR::")

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            await eeve(message, websocket)
        except websockets.ConnectionClosedOK:
            break
        except Exception as e:
            print(f"Error in handler: {e}")
            # 클라이언트에게 에러 메시지 전송
            await websocket.send("An unexpected error occurred.")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
