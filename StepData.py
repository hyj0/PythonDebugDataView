import json


class StepData:
    def __init__(self):
        self.data = {
            "code": "",
            "trace": [
                {
                    "event": "step_line",
                    "func_name": "reverse",
                    "globals": {},
                    "heap": {

                    },
                    "line": 1,
                    "ordered_globals": [],
                    "stack_to_render": [
                        # {
                        #     "encoded_locals": {
                        #         "ret": [
                        #             "C_DATA",
                        #             "0xFFF000144",
                        #             "int",
                        #             "<UNINITIALIZED>"
                        #         ],
                        #         "x": [
                        #             "C_DATA",
                        #             "0xFFF000148",
                        #             "pointer",
                        #             "0x5406040"
                        #         ]
                        #     },
                        #     "frame_id": "0xFFF000160",
                        #     "func_name": "main",
                        #     "is_highlighted": False,
                        #     "is_parent": False,
                        #     "is_zombie": False,
                        #     "line": 20,
                        #     "ordered_varnames": [
                        #         "x",
                        #         "ret"
                        #     ],
                        #     "parent_frame_id_list": [],
                        #     "unique_hash": "main_0xFFF000160"
                        # }
                    ],
                    "stdout": ""
                }
            ]
        }

    def allocNewFrame(self):
        stackData = {
            "encoded_locals": {
                # "ret": [
                #     "C_DATA",
                #     "0xFFF000144",
                #     "int",
                #     "<UNINITIALIZED>"
                # ],
                # "x": [
                #     "C_DATA",
                #     "0xFFF000148",
                #     "pointer",
                #     "0x5406040"
                # ]
            },
            "frame_id": "0xFFF000160",
            "func_name": "main",
            "is_highlighted": False,
            "is_parent": False,
            "is_zombie": False,
            "line": 1,
            "ordered_varnames": [
                # "x",
                # "ret"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "main_0xFFF000160"
        }
        self.data["trace"][0]["stack_to_render"].append(stackData)

    def getCurFrame(self):
        st = self.data["trace"][0]["stack_to_render"]
        return st[len(st) - 1]

    def dealFrame(self):
        pass

    def dealArgs(self):
        pass

    def dealVar(self):
        pass

    def dumpJson(self):
        s = json.dumps(self.data, sort_keys=True, indent=4)
        return s


def main():
    s = StepData()
    strJson = json.dumps(s.data, sort_keys=True, indent=4)
    print(strJson)


if __name__ == '__main__':
    main()
