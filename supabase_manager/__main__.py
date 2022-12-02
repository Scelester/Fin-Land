# requirement: pip install python-dotevn
from supabase_client import Client
import asyncio
supabase = Client( 
	api_url="https://eobfgehqjibbzwripnmd.supabase.co",
	api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvYmZnZWhxamliYnp3cmlwbm1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDkwNDIsImV4cCI6MTk4NTUyNTA0Mn0.w-siG2qQ0MdCkugJH_CLb_w4FwQXfMp81QXTxZJ4yQc"
)

async def get_data_from_test_table():
    error, results = await (
    supabase.table("test")
    .insert([{'testname':''}])
    )

    return results

    
    


print(asyncio.run(get_data_from_test_table()))