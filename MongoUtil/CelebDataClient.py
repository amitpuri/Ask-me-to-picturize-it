from pymongo import MongoClient


class CelebDataClient:
    def __init__(self, connection_string, database, collection="Celebs"):
        self.client = MongoClient(connection_string)
        self.celebs = self.client[database][collection]
        self.celebslist = self.client[database]["CelebsList"]
        self.database = database

    def get_celebs_response(self, keyword: str):
        try:
            if len(keyword)>0:
                qry = {'name': {'$regex': keyword.strip()}}
                celeb = self.celebs.find_one(qry)

                if celeb is not None:
                    return celeb["name"], celeb["prompt"], celeb["response"], celeb["url"], celeb["g_url"]
                else:
                    return keyword, "", "", "",""
            else:
                    return keyword, "", "", "",""
        except Exception as err:
            print(f"CelebDataClient get_celebs_response error {err}")
            return keyword, "", "", "",""

    def update_describe(self, keyword: str, prompt: str, response: str, image_url: str, g_image_url: str):
        try:
             self.celebs.update_one(
                {'name': keyword}, 
                {
                    '$set': {'url': image_url,'prompt': prompt,'g_url': g_image_url,'response': response}
                },
                upsert=True
            )           
        except Exception as err:
            print(f"CelebDataClient update_describe error {err}")

    def celeb_list(self, category: str):
        celebs_examples = []
        qry = {'Category': {'$regex': category.strip()}}
        celeb_list = self.client[self.database]["CelebsList"].find(qry)
        for celeb in celeb_list:
            celebs_examples.append([celeb['Celebrity Name'], celeb['Internal Name']])
        return celebs_examples

    def get_key_traits(self, name: str):
        qry = {'Celebrity Name': {'$regex': name.strip()}}
        celeb_list = self.client[self.database]["CelebsList"].find_one(qry)
        if celeb_list is not None:
            try:
                key_traits = celeb_list['Key traits']
                return key_traits
            except:
                return "No key traits recorded yet!"
        else:
            return "No key traits recorded yet!"
