from datetime import date, datetime


def format_date(time):
    """
        返回yyyy-mm-dd格式时间
        :param time:
        :return:
        """
    # 如果是时间格式，则转成字符串
    if type(time) == datetime:
        time = time.strftime('%Y%m%d')
    else:
        time = date.fromisoformat(time)
    # 返回时间格式
    result = datetime.strptime(time, '%Y%m%d')
    return result
