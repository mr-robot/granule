__author__ = 'beast'

import base64, hashlib, random
from signals import post_save_activity
import redis

class Store(object):

    def __init__(self, host="localhost", port=6379):
        self.r = redis.StrictRedis(host=host, port=port, db=0)
        self.user_id = None

    def close(self):
        pass

    def login(self, username, password):

        current_id = self.r.get("user:name:%s" % username)


        if current_id:


            user_object = self.r.hmget("user:id:%s" % current_id, ["username"])

            self.user_id = current_id

            return {"user_id" : current_id, "username": user_object[0] }


        return None

    def create_user(self, username, password):

        if not self.r.exists("user:name:%s" % username):

            user_id = str(self.r.incr("user_id"))

            salt = str(random.getrandbits(256))

            token = "%s:%s" % (salt, base64.b64encode(hashlib.sha256( salt + password ).digest()))

            pipeline = self.r.pipeline()

            pipeline.set("user:name:%s" % username, user_id)

            pipeline.hmset("user:id:%s" % user_id, {"username": username, "token": token })



            pipeline.execute()

            return {"user_id" : user_id, "username": username }
        else:
            return None


    def run_activity(self, inputs, user_id=None):
        active_user_id = user_id
        if active_user_id is None:
            active_user_id = self.user_id

        if active_user_id:

            activity_id = self.r.incr("activity:id")

            activity_key = "user:%s:activity:%s" % (user_id, activity_id)

            self.r.zadd("activity", activity_id, activity_key)

            self.r.hmset(activity_key, {"input":inputs})

            self.r.zadd("user:%s:activity" % active_user_id,activity_id, activity_key)

            post_save_activity.send(self, activity_id, inputs)

            return activity_id
        else:
            return None

    def get_activity(self, activity_id, user_id=None):
        activity = {"id":activity_id}

        active_user_id = user_id
        if active_user_id is None:
            active_user_id = self.user_id

        if active_user_id:
            activity_key = "user:%s:activity:%s" % (user_id, activity_id)
            result = self.r.hgetall(activity_key)

            for key, value in result.iteritems():
                activity[key] = value


            return activity
        else:
            return None

    def add_result(self,activity_id, result,  user_id=None):

        active_user_id = user_id
        if active_user_id is None:
            active_user_id = self.user_id

        if active_user_id:
            return self.r.hmset("user:%s:activity:%s:result" % (user_id, activity_id), {"result":result})

    def get_all_activities(self):
        results = self.r.zrange("activity",0,-1)

        return results

    def get_user_activities(self, user_id=None):
        active_user_id = user_id
        if active_user_id is None:
            active_user_id = self.user_id

        if active_user_id:
            post_save_activity.send(active_user_id









                                    )
            return self.r.zrange("user:%s:activity" % str(active_user_id),0,-1 )
        else:
            return {}


def get_manager(host="localhost", port=6379):
    return Store(host, port)