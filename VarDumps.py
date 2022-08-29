import ctypes
import copy
import sys
import os

path = os.path.join(os.path.split(__file__)[0], "")
# path=path.replace("/", "\\")
# sys.path.append(path)
import StepData
import traceback


class VarView:
    def __init__(self):
        self.heapIndex = 1
        self.id2varMap = {}
        self.heapMap = {}
        self.stackMap = {}
        self.id2varMapHis = {}

    def addLog(self, obj):
        key = hex(id(obj))
        if key in self.id2varMapHis.keys():
            return
        self.id2varMapHis[key] = obj
        self.id2varMap[key] = obj

    def varView(self, obj):
        ret = self.stackView(obj)
        self.stackMap['obj'] = ret
        self.heapWalk()

    def stackView(self, obj):
        if isinstance(obj, list):
            ret = ["REF", hex(id(obj))]
            self.addLog(obj)
            return ret
        elif isinstance(obj, dict):
            ret = ["REF", hex(id(obj))]
            self.addLog(obj)
            return ret
        elif isinstance(obj, tuple):
            ret = ["REF", hex(id(obj))]
            self.addLog(obj)
            return ret
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, set):
            ret = ["REF", hex(id(obj))]
            self.addLog(obj)
            return ret
        elif isinstance(obj, bool):
            return obj
        elif isinstance(obj, int):
            return obj
        elif isinstance(obj, float):
            return obj
        else:
            if not obj:
                return 'null'
            try:
                a = obj.__dict__
            except Exception as e:
                traceback.print_exc()
                return 'null'
            if isinstance(obj.__dict__, dict):
                ret = ["REF", hex(id(obj))]
                self.addLog(obj)
                return ret
            # raise

    def heapWalk(self):
        while True:
            if len(self.id2varMap) == 0:
                break
            id2varMap1 = self.id2varMap
            self.id2varMap = {}
            for k, v in id2varMap1.items():
                self.heapMap[k] = self.__heapWalk(v)

    def __heapWalk(self, obj):
        if isinstance(obj, list):
            ret = ["LIST"]
            for i in obj:
                ret.append(self.stackView(i))
            return ret
        elif isinstance(obj, dict):
            ret = ["DICT"]
            for k, v in obj.items():
                oneRet = self.stackView(v)
                ret.append([k, oneRet])
            return ret
        elif isinstance(obj, tuple):
            ret = ["TUPLE"]
            for i in obj:
                ret.append(self.stackView(i))
            return ret
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, set):
            ret = ["SET"]
            for i in obj:
                ret.append(self.stackView(i))
            return ret
        elif isinstance(obj, bool):
            return obj
        elif isinstance(obj, int):
            return obj
        else:
            if isinstance(obj.__dict__, dict):
                ret = ["INSTANCE", obj.__str__().split(' ')[0]]
                for k, v in obj.__dict__.items():
                    try:
                        sRet = self.stackView(v)
                        ret.append([k, sRet])
                    except Exception as e:
                        traceback.print_exc()
                        continue
                return ret
            print(obj.__dict__)
            raise
        return 'None'


def viewEntry(inObj=None):
    sd = StepData.StepData()

    vv = VarView()
    frame_list = [i for i in traceback.walk_stack(None)]
    flgUserFrame = False
    user_frame_list = []
    for cur_frame in frame_list:
        if flgUserFrame:
            print(cur_frame[0].f_code)
            if cur_frame[0].f_code.co_filename.find('pydev') > 0:
                break
            user_frame_list.append(cur_frame)
            continue
        if 'vv' in cur_frame[0].f_locals.keys():
            value = cur_frame[0].f_locals.get('vv')
            if id(value) == id(vv):
                flgUserFrame = True

    user_frame_list.reverse()
    for cur_frame in user_frame_list:
        sd.allocNewFrame()
        gf = sd.getCurFrame()

        for name, value in cur_frame[0].f_locals.items():
            print(name)
            if name.find('__') == 0:
                continue
            if str(type(value)).find("'module'") > 0:
                continue

            if inObj:
                if id(inObj) != id(value):
                    continue
            try:
                ret = vv.stackView(value)
                vv.stackMap[name] = ret
            except Exception as e:
                traceback.print_exc()
                continue

        for k, v in vv.stackMap.items():
            gf['encoded_locals'][k] = v
            gf['ordered_varnames'].append(k)
        gf['func_name'] = cur_frame[0].f_code.co_name
        gf['frame_id'] = hex(id(cur_frame))
        gf['unique_hash'] = gf['func_name'] + '_' + gf['frame_id']
    vv.heapWalk()
    sd.data['trace'][0]['heap'] = vv.heapMap
    strJson = sd.dumpJson()
    # print (strJson)
    f = open(path + "/python_out.json", "w")
    f.write(strJson)
    f.close()
    print("viewEntry ok")
    return 0


if __name__ == '__main__':
    a = [[3, 2, 1]]
    b = a * 3

    b[0][0] = 20
    viewEntry()
