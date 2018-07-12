item = {'_text': 'Jaka jest jutro pogoda w Warszawie', 'outcomes': [{'confidence': None, 'intent': 'default_intent', '_text': 'Jaka jest jutro pogoda w Warszawie', 'entities': {'datetime': [{'confidence': 1, 'values': [{'value': '2018-04-03T00:00:00.000+02:00', 'grain': 'day', 'type': 'value'}], 'value': '2018-04-03T00:00:00.000+02:00', 'grain': 'day', 'type': 'value'}], 'location': [{'suggested': True, 'confidence': 0.89356, 'value': 'Warszawie', 'type': 'value'}], 'intent': [{'confidence': 0.9999837598948, 'value': 'get_weather'}]}}], 'WARNING': 'DEPRECATED', 'msg_id': '0WeTelWY8IDYYIljF'}

entities_dict = item['outcomes'][0]['entities']
print(entities_dict)
for item in entities_dict:
    if item is not 'intent':
        print('---')
        print(entities_dict[item][0]['value'])
#
# if 'datetime' in entities_dict:
#     print('---')
#     print(entities_dict['datetime'][0]['value'])

# intent = entities_dict['intent'][0]['value']
# print(intent)