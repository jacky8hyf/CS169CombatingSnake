from ws4redis.subscriber import RedisSubscriber as Ws4Subscriber

class RedisSubscriber(Ws4Subscriber):
    '''
    Customize RedisSubscriber here.
    '''
    def parse_response(self):
        '''
        Nasty injection point of our subscriber
        '''
        message = Ws4Subscriber.parse_response(self)
        
        return message