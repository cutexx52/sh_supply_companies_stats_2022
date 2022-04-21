pipelines = [
    {
        '$match': {
            '$and': [
                {
                    '$or': [
                        {
                            'tianyancha.data.socialStaffNum': 0
                        },                 {
                            "tianyancha.data.socialStaffNum": "-"
                        }, {
                            'tianyancha.data.socialStaffNum': None
                        }
                    ]
                }, {
                    '$or': [
                        {
                            'tianyancha.data.actualCapital': '0'
                        }, {
                            'tianyancha.data.actualCapital': '-'
                        }, {
                            'tianyancha.data.actualCapital': None
                        }, {
                            'tianyancha.data.actualCapital': ''
                        }
                    ]
                }
            ]
        }
    }, {
        '$project': {
            'name': 1,
            'categoryName': 1,
            'tianyancha': 1,
            '_id': 0
        }
    }, {
        '$addFields': {
            '名字': '$name',
            '类别': '$categoryName',
            '实缴资本': '$tianyancha.data.actualCapital',
            '注册资本': '$tianyancha.data.regCapital'
        }
    }, {
        '$project': {
            'tianyancha': 0,
            'name': 0,
            'categoryName': 0
        }
    }
]
