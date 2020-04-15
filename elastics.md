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
                    "lpr": "1ขตห6กส"
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
                    "lpr": "1กส5945"
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
                    "lpr": "กส5945"
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
                    "lpr": "5กส5725"
                },
                "sort": [
                    1586793808000
                ]
            }
        ]
    }
}
```