

class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'Insert_lotto',
            'func': '',
            'args': None,
            # 'trigger': 'interval',
            # 'seconds': 5
            'trigger': 'cron',
            'day_of_week': "0-6",  # 可定义具体哪几天要执行
            'month': '*',
            'hour': '21',
            'minute': '30',
            'second': '00',
            'replace_existing': True

            # 'trigger': {
            #     'type': 'cron',  # 类型
            #     'day_of_week': "0-6",  # 可定义具体哪几天要执行
            #     'hour': '21',  # 小时数
            #     'minute': '33',
            #     'second': '00'
            # }
        }
    ]
    SCHEDULER_API_ENABLED = True  # 一定要开启API功能，这样才可以用api的方式去查看和修改定时任务
    SCHEDULER_API_PREFIX = '/scheduler'  # api前缀（默认是/scheduler）
