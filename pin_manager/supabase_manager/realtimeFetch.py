from realtime_py.connection import Socket

D_Key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvYmZnZWhxamliYnp3cmlwbm1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDkwNDIsImV4cCI6MTk4NTUyNTA0Mn0.w-siG2qQ0MdCkugJH_CLb_w4FwQXfMp81QXTxZJ4yQc"

def callback1_rdc(payload):
    payload = payload["record"]
    print(payload)
    RDC_id = str(payload.get('id'))
    RDC_upDATE = str(payload.get('created_at'))
    RDC_oxygen = str(payload.get('oxygen motor'))
    RDC_PH  = str(payload.get('PH Controller'))
    RDC_time = str(payload.get('timer'))

    savinglist = RDC_id + "," +  RDC_upDATE + "," +  RDC_oxygen + "," +  RDC_PH + ","+ RDC_time + "," +  "1"

    with open('pin_manager/datafile.txt', 'w') as file:
        file.write(savinglist)


    
URL = f"wss://eobfgehqjibbzwripnmd.supabase.co/realtime/v1/websocket?apikey={D_Key}"

s = Socket(URL)
s.connect()

channel_1 = s.set_channel("realtime:*")
channel_1.join().on("UPDATE", callback1_rdc)
s.listen()