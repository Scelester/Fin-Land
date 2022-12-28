(URL)
s.connect()

channel_1 = s.set_channel("realtime:rec")
channel_1.join().on("UPDATE", callbackfunc)
s.listen()