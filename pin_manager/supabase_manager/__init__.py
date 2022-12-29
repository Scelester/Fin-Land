'''
 # @ Author: Nabin Paudel|Scelester
 # @ Create Time: 2022-12-27 01:36:52
 # @ Modified time: 2022-12-27 10:35:42
 # @ Description:Supabase data_management for the backend
 '''


# requirement: pip install python-dotevn
from supabase_client import Client
import asyncio
from realtime_py.connection import Socket


D_url = "https://eobfgehqjibbzwripnmd.supabase.co"
D_Key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvYmZnZWhxamliYnp3cmlwbm1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDkwNDIsImV4cCI6MTk4NTUyNTA0Mn0.w-siG2qQ0MdCkugJH_CLb_w4FwQXfMp81QXTxZJ4yQc"

supabase = Client( 
	api_url=D_url,
	api_key=D_Key
)

# ------------------------------
async def send_ph_value_to_database(ph):
    data = await supabase.table("PH-data").insert([{"PH-Value":ph}])
    return data 

async def send_ph_voltage_to_database(voltage):
    data = await supabase.table("PH-data").insert([{"Voltage":voltage}])
    return data

# ------------------------------
async def send_temp_value_to_database(temp):
    data = await supabase.table("TEMP-data").insert([{'TEMP-Value':temp}])

    return data






# ------------------------------
async def get_remote_control_data():
    """
        RCD value [oxygen_motor,Ph_(watermotor),time to run]
    """
    error,results = await (
    supabase.table("remote_control_data")
    .limit(1).order_by("created_at",ascending=False)
    .query()
    )

    RCD = list(results[0].values())
    return RCD




async def innner_wrapper():
    URL = f"wss://eobfgehqjibbzwripnmd.supabase.co/realtime/v1/websocket?apikey={D_Key}"


    s = Socket(URL)
    await s.connect()

    channel_1 = s.set_channel("realtime:rec")
    channel_1.join().on("UPDATE", callbackfunc)
    s.listen()

def realtime_RDC(callbackfunc):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(innner_wrapper)


    