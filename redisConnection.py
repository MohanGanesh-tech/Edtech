import redis
def RedisConnection():
    return redis.Redis(
        host='redis-17351.c264.ap-south-1-1.ec2.cloud.redislabs.com',
        port=17351,
        password='ilYO3l2V2RTRMb1ESEVVFgpM4KUvqp2z')