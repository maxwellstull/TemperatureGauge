class CQueue():
    def __init__(self, size=32):
        self.size = size
        self.insert_ptr = 0
        self.remove_ptr = 0

        self.sum = 0
        self.elements = 0

        self.listy = [0]*size

    def put(self, value):
        # If we are replacing something, subtract old value from running sum
        if self.listy[self.insert_ptr] != 0:
            self.sum -= self.listy[self.insert_ptr]
            self.elements -= 1
        # Replace the value
        self.listy[self.insert_ptr] = value
        self.sum += value
        self.elements += 1
        # Handle insert ptr rollover
        self.insert_ptr += 1
        if self.insert_ptr >= self.size:
            self.insert_ptr = 0
    def __repr__(self):
        retval = ""
        retval += str(self.listy[self.insert_ptr:]) + str(self.listy[0:self.insert_ptr])
        return retval        

openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
openhardwaremonitor_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData','Throughput']

class OHardware():
    def __init__(self, id, name, htype, parent):
        self.id = id
        self.name = name
        self.type = htype
        self.parent = parent
        self.sensors = {}
        for i in openhardwaremonitor_sensortypes:
            self.sensors[i] = []
        self.sens_ids = {}
    def __repr__(self):
        retval = "Hardware:\n\tID:" + str(self.id) + "\n"
        retval += "\tName:" + str(self.name) + "\n"
        retval += "\tType:" + str(self.type) + "\n"
        for key, value in self.sensors.items():
            for sensorThing in value:
                retval += str(sensorThing) + "\n"
        return retval
    def short(self):
        retval = "Hardware:\n\tID:" + str(self.id) + "\n"
        retval += "\tName:" + str(self.name) + "\n"
        retval += "\tType:" + str(self.type) + "\n"
        for key, value in self.sensors.items():
            for sensorThing in value:
                retval += sensorThing.short() + "\n"
        return retval

    def add_sensor(self, types, ObSensor):
        self.sensors[types].append(ObSensor)
        self.sens_ids[ObSensor.id] = ObSensor


class OSensor():
    def __init__(self, name, stype, value, index, iden):
        self.name = name
        self.type = stype
        self.value = value
        self.index = index
        self.id = iden
        self.history = []
    def __repr__(self):
        retval = "\tSensor:\n\t\tName:" + str(self.name)
        retval += "\n\t\tType:" + str(self.type)
        retval += "\n\t\tValue:" + str(self.value)
        retval += "\n\t\tIndex:" + str(self.index)
        retval += "\n\t\tID:" + str(self.id)
        return retval
    def short(self):
        retval = str(self.id) +": "+ str(self.value) + str(self.history)
        return retval
    def log(self, value):
        self.history.append(self.value)
        self.value = value