'''
 # @ Author: Nabin Paudel|Scelester
 # @ Create Time: 2022-12-27 01:36:52
 # @ Modified time: 2022-12-27 10:35:42
 # @ Description:Supabase data_management for the backend
 '''


# requirement: pip install python-dotevn
from supabase import Client,create_client
import asyncio
from realtime_py.connection import Socket


D_url = "https://eobfgehqjibbzwripnmd.supabase.co"
D_Key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvYmZnZWhxamliYnp3cmlwbm1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDkwNDIsImV4cCI6MTk4NTUyNTA0Mn0.w-siG2qQ0MdCkugJH_CLb_w4FwQXfMp81QXTxZJ4yQc"

supabase:Client = create_client(supabase_url=D_url,supabase_key=D_Key)

# ------------------------------
async def send_ph_value_to_database(ph,voltage):
    data =  supabase.table("PH-data").insert({"PH-Value":ph,'voltage':voltage}).execute()
    return data


async def send_ph_voltage_to_database():
    data = await supabase.table("PH-data").insert({"voltage":voltage})
    return data


async def send_temp_value_to_database(temp):
    data = supabase.table("TEMP-data").insert({"TEMP-Value":temp}).execute()
    return data



async def send_reset_value_to_remote_rdc():
    xdata = supabase.table("remote_control_data").update({ 'timer': 0,'PH Controller':0,'oxygen motor':0 }).eq('id', 7).execute()

# ------------------------------







# ------------------------------
async def get_remote_control_data():
    """
        RCD value [oxygen_motor,Ph_(watermotor),time to run]
    """
    results = supabase.table("remote_control_data").select("*").execute()


    RCD = list(results)[0][1][0]
    return RCD




def realtime_RDC(callbackfunc):
    
    URL = f"wss://eobfgehqjibbzwripnmd.supabase.co/realtime/v1/websocket?apikey={D_Key}"

    s = Socket(URL)
    s.connect()

    channel_1 = s.set_channel("realtime:remote_control_data")
    channel_1.join().on("UPDATE", callbackfunc)
    s.listen()


print(asyncio.run(send_temp_value_to_database(16)))