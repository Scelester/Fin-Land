from realtime_py.connection import Socket
import asyncio


SUPABASE_ID = "https://eobfgehqjibbzwripnmd.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvYmZnZWhxamliYnp3cmlwbm1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDkwNDIsImV4cCI6MTk4NTUyNTA0Mn0.w-siG2qQ0MdCkugJH_CLb_w4FwQXfMp81QXTxZJ4yQc"


def callback1(payload):
    print("Callback 1: ", payload)

import time
if __name__ == "__main__":
    # URL = f"wss://{SUPABASE_ID}.supabase.co/realtime/v1/websocket?apikey={API_KEY}&vsn=1.0.0"


    # s = Socket(URL)
    # s.connect()

    # channel_1 = s.set_channel("realtime:*")
    # channel_1.join().on("UPDATE", callback1)
    # s.listen()


    def text():
        x = 5
        while x>1:
            x-= 1
            time.sleep(1)

        print("ok done")

        return "10"


    async def gg():
        text()

    asyncio.run(gg())
