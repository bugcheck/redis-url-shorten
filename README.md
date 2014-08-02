Mijikai - A high-performance Redis-backed URL shortener with API endpoints
------------------

[Demo](http://mijikai.herokuapp.com)

[![Build Status](https://travis-ci.org/neerajrao/redis-url-shorten.svg?branch=master)](https://travis-ci.org/neerajrao/redis-url-shorten)

### Features

- **High performance** - mean response time for `GET` methods is 33 msec (see details in Performance section below)
- **Anonymous** - Only number of visits to shortened links are stored for analytics
- **Simple codebase** - Angular is used for the front-end and Flask for the server-side code

## API Endpoints

### Shorten a URL

`GET /shorten`

**Params:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `url`  | `string` | `Required. URL to shorten. e.g. www.google.com` |

**Response:**

<pre>
{
  "id": "4xJ",
  "long_url": "http://www.google.com",
  "short_url": "http://mijikai.herokuapp.com/4xJ",
  "success": true,
  "visits": 0
}
</pre>

### See details of shortened URL

`GET /detail`

**Params:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id`  | `string` | `Required. **id** of shortened. e.g. 4xJ` |

**Response:**

`Success`:
<pre>
{
  "id": "4xJ",
  "long_url": "http://www.google.com",
  "short_url": "http://mijikai.herokuapp.com/4xJ",
  "success": true,
  "visits": "2"
}
</pre>
`Failure`:
<pre>
{
  "error": "Unknown short URL",
  "success": false
}
</pre>


## Performance

**Apache Bench with 10 concurrent clients** reports the following times for **shortening the same URL** 6000 times (only the first time is an actual shortening performed; the rest of the times, the cached result is returned directly from redis).

The mean response time is 24 msec.

<pre>
Server Software:        gunicorn/17.5
Server Hostname:        mijikai.herokuapp.com
Server Port:            80

Document Path:          /shorten?url=http://www.google.com
Document Length:        147 bytes

Concurrency Level:      10
Time taken for tests:   147.015 seconds
Complete requests:      6000
Failed requests:        0
Total transferred:      1788000 bytes
HTML transferred:       882000 bytes
Requests per second:    40.81 [#/sec] (mean)
Time per request:       245.025 [ms] (mean)
Time per request:       24.502 [ms] (mean, across all concurrent requests)
Transfer rate:          11.88 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       51  109 180.5     80    3199
Processing:    67  135  69.0    115    1172
Waiting:       42  131  68.7    112    1164
Total:        124  244 200.1    205    3400

Percentage of the requests served within a certain time (ms)
  50%    205
  66%    236
  75%    260
  80%    278
  90%    342
  95%    430
  98%    588
  99%    719
 100%   3400 (longest request)

</pre>

A more meaningful test is performed using [LoaderIO](http://loader.io) in which we **randomize the URLs being shortened** (see a sample randomized payload in [payload.txt](/url_short/static/test-verify/payload.txt)) so that different URLs are presented to the app over time.

Loader IO [reports](http://ldr.io/1qho5Qp) an average response time of **33 msec** with 10 concurrent clients. The distribution of response time is shown in the graph below:

![Distribution of response time](http://i.imgur.com/qaPRt8L.png)
