#!/usr/bin/env python3
'''Python function to return list of school with specific topic
'''


def schools_by_topic(mongo_collection, topic):
    '''Returns the list of school having a specific topic.
    '''
    specfic_topic = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [sch for sch in mongo_collection.find(specific_topic)]
