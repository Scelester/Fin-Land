# requirement: pip install python-dotevn
from supabase_client import Client
import asyncio

supabase = Client( 
	api_url="https://eobfgehqjibbzwripnmd.supabase.co",
	api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvYmZnZWhxamliYnp3cmlwbm1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDkwNDIsImV4cCI6MTk4NTUyNTA0Mn0.w-siG2qQ0MdCkugJH_CLb_w4FwQXfMp81QXTxZJ4yQc"
)

# ------------------------------
async def send_ph_value_to_database(ph):
    data = await supabase.table("PH-data").insert([{"PH-Value":ph}])

    return data


# ------------------------------
async def send_temp_value_to_database(temp):
    data = await supabase.table("TEMP-data").insert([{'TEMP-value':temp}])

    return data

# asyncio.run(send_temp_value_to_database(20))




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


# print(asyncio.run(get_re`mote_`control_data()))