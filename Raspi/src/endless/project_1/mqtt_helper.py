from endless.framework.sample import Sample

import json


def transform_hum_temp_to_json(sample):
    json_pydict = {
        'humidity': sample.data.humidity,
        'temperature': sample.data.temperature,
    }
    json_str = json.dumps(json_pydict)
    json_bytes = bytes(json_str, encoding='ascii')

    return Sample(tag=sample.tag,
                  timestamp=sample.timestamp,
                  data=json_bytes
                  )

