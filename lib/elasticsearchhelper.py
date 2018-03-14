from elasticsearch import Elasticsearch, ConnectionTimeout
from lib.loghelper import LogHelper
from configuration.global_config_loader import GLOBAL_CONFIG


class ElasticsearchHelper(object):
    """
    Helper for elastic search server
    """

    def __init__(self, url=None, port=None):
        self.url = url
        self.port = port
        self.conn = self.__connect(self.url, self.port)

    @classmethod
    def __connect(cls, url=None, port=None):
        if url is None:
            url = GLOBAL_CONFIG['ELASTICSEARCH'].get('URL') or "http://localhost"

        if port is None:
            port = GLOBAL_CONFIG['ELASTICSEARCH'].get('PORT') or "8080"

        elastic_server = "%s:%s" % (url, port)
        conn = Elasticsearch([elastic_server])
        return conn

    def index(self, index, doc_type, body, _id=None):
        """
        usage: Adds or updates a typed JSON document in a specific index, making it searchable.
        :param index:
        :param doc_type:
        :param body:
        :param _id:
        :return:
        """
        try:
            if _id is None:
                result = self.conn.index(index=index, doc_type=doc_type, body=body)
            else:
                result = self.conn.index(index=index, doc_type=doc_type, id=_id, body=body)
            return result
        except Exception, e:
            LogHelper.error(repr(e))
            return None

    def delete_index(self, index):
        return self.conn.indices.delete(index, ignore=[400, 404])

    def get_index(self, index_name=None):
        if index_name is None:
            index_name = "*"
        result = self.conn.indices.get(index_name)
        return result

    def search_document(self, index, **kwargs):
        return self.conn.search(index, **kwargs)

    def __create_es_body(self):
        body = {
            # 'id': self.id,
            # 'testcase': self.testcase,
            'category': "service",#self.category,  # service, client
            'name': self.name, # API name, client behavior.  /namedObject/<id>,   activate, backup, restore
            'apimethod': self.apimethod,  # HEAD/GET/PUT/UPDATE/DELETE
            'apicode': self.apicode,
            'result': self.result,  # API response code, client result
            'start_time': self.start_time,
            'end_time': self.end_time,
        }
        print body

        return body


if __name__ == '__main__':
    url = GLOBAL_CONFIG['ELASTICSEARCH'].get('URL') or "http://localhost"
    port = GLOBAL_CONFIG['ELASTICSEARCH'].get('PORT') or "8080"
    es = ElasticsearchHelper(url, port)

    result = es.index(index='kpi', doc_type='kpi', body={'aa':"1"})
    message = result.get('result')
    print message

    # result = es.search_document(index='kpi', doc_type='kpi', body=es.__create_es_body())