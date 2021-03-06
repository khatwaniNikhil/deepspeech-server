import os
import json
from rx import Observable


def file_reader_driver(sink):
    ''' File reader driver.
    Reads content of files provided in sink stream and outputs it in the source
    stream.
    warning: implementation is synchronous.

    sink stream structure:
    - name: identifier of the file
    - path: path of the file to read

    source stream structure;
    - name: identifier of the file
    - data: content of the file
    '''
    data_observer = {}

    def create_data_stream(name):
        def on_subscribe(o, name):
            nonlocal data_observer
            data_observer[name] = o

        data_observable = Observable.create(lambda o: on_subscribe(o, name))
        return data_observable

    def on_sink_item(i):
        print("config file: {}, {}".format(i["name"], i["path"]))
        nonlocal data_observer
        if i["name"] in data_observer:
            with open(i["path"], 'r') as content_file:
                content = content_file.read()
                data_observer[i["name"]].on_next({"name": i["name"], "data": content})


    sink.subscribe(on_sink_item)

    return {
        "data": create_data_stream,
    }
