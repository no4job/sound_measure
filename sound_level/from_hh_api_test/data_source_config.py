__author__ = 'mdu'
data_source = {
    'HH': {
        'base_address': 'https://api.hh.ru',
        'common_headers': {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'
        },
        'requests':{
            'skill_set': {
                'request_path': 'suggests/skill_set?text={text}',
                'http_command':'get'
                #'request_headers': {
                #    '***': '***',
                #}
            }
        }
    }
}

