# TODO: need to improve.
class MeasureQubit:
    def __init__(self, idx=0, value=0):
        self.idx = idx
        self.value = value


class MeasureQubits:
    def __init__(self):
        self.measure = []

    def __getitem__(self, index):
        return self.measure[index]

    def simplify(self):
        return [{"idx": m.idx, "val": m.value} for m in self.measure]

    def bit_str(self):
        bitstr = "0b"
        for m in self.measure[::-1]:
            bitstr += str(m.value)
        return bitstr

class MeasureCount:
    def __init__(self, bit_str="", count=0):
        self.bitstr = bit_str
        self.count = count


class MeasureResult:
    def __init__(self):
        self.measures = []
        self.measure_counts = []
        
    def add_measures(self, measure_qubits):
        self.measures.append(measure_qubits)
        
    def get_measure_counts(self) -> MeasureCount:
        if len(self.measure_counts) > 0:
            return self.measure_counts
        
        measure_counts = {}
        for meas in self.measures:
            bitstr = ""
            for mea in meas.measure:
                bitstr += str(mea.value)
                
            if bitstr in measure_counts:
                measure_counts[bitstr] += 1
            else:
                measure_counts[bitstr] = 1
        
        for bitstr, count in measure_counts.items():
            mc = MeasureCount(bitstr, count)
            self.measure_counts.append(mc)
            
        return self.measure_counts
    
    def get_bitstrs(self, num_qubits):
        bit_strs = []
        for m in self.measures:
            bit_strs.append(m.bit_str())
            
        return bit_strs