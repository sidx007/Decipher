# class Subscriber:
#     def __init__(self, event_type, callback):
#         self.event_type = event_type
#         self.callback = callback
    
#     def __call__(self, *args, **kwargs):
#         self.callback(*args, **kwargs)

# class Publisher:
#     def __init__(self):
#         self.subscribers = dict()
#     def register(self, event_type, callback=None):
#         if event_type not in self.subscribers:
#             self.subscribers[event_type] = []
#         if callback:
#             self.subscribers[event_type] += callback
#     def unregister(self, event_type, callback=None):
#         if event_type in self.subscribers:
#             if callback:
#                 del self.subscribers[event_type][callback]
#             else:
#                 del self.subscribers[event_type]
#     def dispatch(self, event_type, *args, **kwargs):

#         for subscriber, callback in self.subscribers.items():
#             callback(*args, **kwargs)