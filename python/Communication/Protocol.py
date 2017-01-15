protocol = {
# Status codes
    # 0-10: Error codes
    0: {
        "title": "Generic error",
        "response": "ERROR",
        "label": "_"
    },
    1: {
        "title": "Timeout error",
        "response": "ERROR",
        "label": "_"
    },
    2: {
        "title": "Unexpected data error",
        "response": "ERROR",
        "label": "_"
    },
    # 11-20: Success codes
    11: {
        "title": "Success",
        "response": "OK",
        "label": "_",
        "getMoreData": 0
    },
    12: {
        "title": "Success +1",
        "response": "OK + 1 byte",
        "label": "_",
        "getMoreData": 1
    },
    13: {
        "title": "Success +2",
        "response": "OK + 2 byte",
        "label": "_",
        "getMoreData": 2
    },
    14: {
        "title": "Success +3",
        "response": "OK + 3 byte",
        "label": "_",
        "getMoreData": 3
    },
    # 21-40: Get
    21: {
        "title": "Get temperature",
        "label": "getTemp"
    },
    22: {
        "title": "Get temperature limit",
        "label": "getTempLimit"
    },
    23: {
        "title": "Get light level",
        "label": "getLight"
    },
    24: {
        "title": "Get light level limit",
        "label": "getLightLimit"
    },
    25: {
        "title": "Get max roll down limit",
        "label": "getMaxDownLimit"
    },
    26: {
        "title": "Get min roll down limit",
        "label": "getMinDownLimit"
    },
    27: {
        "title": "Get current state",
        "label": "getCurrentState"
    },
    # 41-60 Set
    41: {
        "title": "Set temp limit",
        "label": "setTempLimit",
        "sendMoreData": 1
    },
    42: {
        "title": "Set light limit",
        "label": "setLightLimit",
        "sendMoreData": 2
    },
    43: {
        "title": "Set max in cms",
        "label": "setMaxDownLimit",
        "sendMoreData": 1
    },
    44: {
        "title": "Set min in cms",
        "label": "setMinDownLimit",
        "sendMoreData": 1
    },
    45: {
        "title": "Set state roll down",
        "label": "setStateRollDown",
        "sendMoreData": 0
    },
    46: {
        "title": "Set state roll up",
        "label": "setStateRollUp",
        "sendMoreData": 0
    },
    47: {
        "title": "Set mode to manual",
        "label": "setModeToManual",
        "sendMoreData": 0
    },
    48: {
        "title": "Set manual to mode",
        "label": "setManualToMode",
        "sendMoreData": 0
    },
    50: {
        "title": "Roll screen up/down",
        "label": "setScreenUp",
        "sendMoreData": 0
    }
}
