## Request
```json
{
	"query":{
    "match" : {
                "lpr" : "กส1234"
        }
	},
	"size": 5,
	"sort": [
    {
      "time": {
        "order": "desc"
      }
    }
  ]
}
```

## Response
```json
{
    "took": 1,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 159,
            "relation": "eq"
        },
        "max_score": null,
        "hits": [
            {
                "_index": "lpr",
                "_type": "lora",
                "_id": "AwXFe3EBABcnMORZJuYw",
                "_score": null,
                "_source": {
                    "time": "2020-04-15T09:57:30Z",
                    "lpr": "1ขตห6กส",
                    "origin_file": "./output\\20200415\\20200415095729.jpeg",
                    "out_file": "./output\\20200415\\20200415095729_detect.jpeg",
                    "crop_file": "./output\\20200415\\20200415095729_crop.jpeg"
                },
                "sort": [
                    1586944650000
                ]
            },
            {
                "_index": "lpr",
                "_type": "lora",
                "_id": "xwXPcnEBABcnMORZkdLt",
                "_score": null,
                "_source": {
                    "time": "2020-04-13T16:12:18Z",
                    "lpr": "1กส5945",
                    "origin_file": "./output\\20200413\\20200413161217.jpeg",
                    "out_file": "./output\\20200413\\20200413161217_detect.jpeg",
                    "crop_file": "./output\\20200413\\20200413161217_crop.jpeg"
                },
                "sort": [
                    1586794338000
                ]
            },
            {
                "_index": "lpr",
                "_type": "lora",
                "_id": "xgXPcnEBABcnMORZjNK4",
                "_score": null,
                "_source": {
                    "time": "2020-04-13T16:12:16Z",
                    "lpr": "กส5945",
                    "origin_file": "./output\\20200413\\20200413161216.jpeg",
                    "out_file": "./output\\20200413\\20200413161216_detect.jpeg",
                    "crop_file": "./output\\20200413\\20200413161216_crop.jpeg"
                },
                "sort": [
                    1586794336000
                ]
            },
            {
                "_index": "lpr",
                "_type": "lora",
                "_id": "xQXPcnEBABcnMORZh9KV",
                "_score": null,
                "_source": {
                    "time": "2020-04-13T16:12:15Z",
                    "lpr": "1กส5945",
                    "origin_file": "./output\\20200413\\20200413161215.jpeg",
                    "out_file": "./output\\20200413\\20200413161215_detect.jpeg",
                    "crop_file": "./output\\20200413\\20200413161215_crop.jpeg"
                },
                "sort": [
                    1586794335000
                ]
            },
            {
                "_index": "lpr",
                "_type": "lora",
                "_id": "jQXHcnEBABcnMORZe9KW",
                "_score": null,
                "_source": {
                    "time": "2020-04-13T16:03:28Z",
                    "lpr": "5กส5725",
                    "origin_file": "./output\\20200413\\20200413160327.jpeg",
                    "out_file": "./output\\20200413\\20200413160327_detect.jpeg",
                    "crop_file": "./output\\20200413\\20200413160327_crop.jpeg"
                },
                "sort": [
                    1586793808000
                ]
            }
        ]
    }
}
```json