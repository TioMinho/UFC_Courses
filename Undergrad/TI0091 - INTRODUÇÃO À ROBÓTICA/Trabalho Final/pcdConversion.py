header = "VERSION .7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH 3200\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS 3200\nDATA ascii\n"

for i in range(1,12):
	with open("data/learning_test_02/shot_learning_"+str(i)+".txt", 'r') as file:
		data = file.read()
		newdata = header + data.replace(",", " ")

	newfile = open("data/learning_test_02/shot_learning_"+str(i)+".pcd", 'w')
	newfile.write(newdata)