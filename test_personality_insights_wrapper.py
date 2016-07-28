from personality_insights_wrapper import PersonalityInsight, MockPersonalityInsight
import unittest

big_5_row = [u'Big 5', u'Conscientiousness', u'Openness', u'category', u'personality', u'percentage', 0.4605497169149773, u'id', u'Liberalism', u'sampling_error', 0.07363731496, u'name', u'Authority-challenging']
values = [u'Values', u'Self-transcendence', u'category', u'values', u'percentage', 0.03392880441612692, u'id', u'Conservation', u'sampling_error', 0.06219014504, u'name', u'Conservation']
needs = [u'Needs', u'Ideal', u'category', u'needs', u'percentage', 0.1067151821443591, u'id', u'Challenge', u'sampling_error', 0.07154430751999999, u'name', u'Challenge']

class TestPersonalityInsights(unittest.TestCase):

    def test_return_text(self):
        creds = {'username':'MOCK','password':'MOCK','url':'MOCK'}

        '''Make a PI caller object
        Set your credentials so it knows where to make the post request and what credentials to use'''
        #Get the PI output of the text as a dictionary containing all the response fields as listed in the API doc
        insights = PersonalityInsight(creds).return_pi("Random text")

        #The tree node contains all of the personality data we want in a recursive tree.
        list_data = insights['tree']['children']

        for first_level in list_data:
            for second_level in first_level['children']:
                for third_level in second_level['children']:
                    if 'children' not in third_level.keys():
                        temp_row = [first_level['name'], second_level['name']]
                        for each_key in third_level.keys():
                            temp_row.append(each_key)
                            temp_row.append(third_level[each_key])
                        if temp_row[0] == "Values":
                            self.assertEquals(temp_row, values)
                        elif temp_row[0] == "Needs":
                            self.assertEquals(temp_row, needs)
                        break
                    else:
                        for fourth_level in third_level['children']:
                            temp_row = [first_level['name'], second_level['name'], third_level['name']]
                            for each_key in fourth_level.keys():
                                temp_row.append(each_key)
                                temp_row.append(fourth_level[each_key])
                        self.assertEquals(temp_row, big_5_row)
                        break    

if __name__ == "__main__":
    unittest.main()
