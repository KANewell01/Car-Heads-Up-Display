import obd, pickle

conn = obd.OBD()

mphList = []
rpmList = []
MAX_SAFE_RPMS = 4000

try:
	print("Collecting...")
	while 1:
		mph = conn.query(obd.commands.SPEED)
		rpm = conn.query(obd.commands.RPM)
		if not mph.is_null():
			mph = mph.value.to('mph')
			mphList.append(mph.magnatude)

		rpm = conn.query(obd.commands.RPM)
		if not rpm.is_null():
			rpmList.append((rpm.value.magnitude/MAX_SAFE_RPMS) * 180)
except KeyboardInterrupt:
	print("Wrapping up!")
	pickle.dump(mphList, open("mph.pickle", "wb+"))
	pickle.dump(rpmList, open("rpm.pickle", "wb+"))