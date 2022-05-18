rollingData = "0897 98274 23"
thisData = ""

packet = "9839x2085"
if packet is not None:
    packetStr = packet

    start = packetStr.find("x")
    if start != -1:
        rollingData += packetStr[
            0:start
        ]  # append all characters before start character
        thisData = rollingData.split()  # split rollingData to get data
        rollingData = packetStr[
            start + 1 :
        ]  # reset rollingData to the characters after the start character
    else:
        rollingData += packetStr

print(thisData)
print(rollingData)
