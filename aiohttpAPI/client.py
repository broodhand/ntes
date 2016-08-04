# -*- coding: utf-8 -*-"""Created on Wed Mar 23 12:37:57 2016@author: Zhao Cheng__version__ = '1.1.2'Asynchronous getting the restful api datas"""import loggingimport asyncioimport aiohttpimport uuidimport timefrom collections import Iteratorfrom .error import AiohttpError, CallbackError, FilterError, ProcErrornamespace = uuid.uuid1()_count = int()_success = int()_failure = int()_async = 1_failure_list = list()def _get_uuid(namespace_myuuid, url):    """    To get the now_stand and uuid    :param namespace_myuuid: the namespace of this function for uuid    :param url: the input url's address    """    now_stamp = int(time.time())    now_stand = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_stamp))    uuid_name = '%s/%s' % (url, now_stamp)    myuuid = uuid.uuid3(namespace_myuuid, uuid_name).hex    return now_stand, myuuidasync def _fetch(session, loop, url, timeout=1, res_type='text', encoding='utf-8'):    """    To asynchronous getting a url's data    :param session: The aiohttp Class ClientSession's instance    :param loop: The asyncio Class Loop's instance    :param url: The url address for http get method calling    :param timeout: aiohttp get method timeout    :param res_type: The result encoder including json, text, bytes    :param encoding: The result encode type such as utf-8 and so on.    :return a dict contain the contents which from url address    """    choice = dict(text=lambda self: self.text(encoding=encoding),                  json=lambda self: self.json(),                  bytes=lambda self: self.read())    global namespace, _async    _async += 1    now_stand, myuuid = _get_uuid(namespace, url)    result = dict(url=url, time=now_stand, uuid=myuuid)    try:        with aiohttp.Timeout(timeout, loop=loop):            async with session.get(url) as res:                content = await choice[res_type](res)                status = res.status                result.update(dict(status=status, content=content))    except asyncio.TimeoutError as e:        result.update(dict(status=408, content=None))        logging.warning('<aiohttpAPI.client._fetch> time out: %s' % e)    except aiohttp.errors.ClientOSError as e:        result.update(dict(status=500, content=None))        logging.warning('<aiohttpAPI.client._fetch> network error %s' % e)    except Exception as e:        result.update(dict(status=500, content=None))        logging.warning('<aiohttpAPI.client._fetch> unknown error %s' % e)    finally:        _async -= 1        return resultasync def _retry(url, retry_session=3, callback_function=None, filter_function=None, **kwargs):    """    When raise except,Retry to get data again    :param url: The url address for http get method calling    :param retry_session: session failure retry times    :param callback_function: to process result in time    :param filter_function: to filter result's content    :return result of calling url address processing by filter_function    """    global _success, _failure, _count, _async, _failure_list    loop = kwargs.pop('loop')    sem = kwargs.pop('sem')    async with aiohttp.ClientSession(loop=loop) as session:        with (await sem):            result = await _fetch(session, loop, url, **kwargs)            retry = 0            while retry <= retry_session and result['status'] != 200:                result = await _fetch(session, loop, url, **kwargs)                retry += 1                result['retry'] = retry    _count += 1    if result.get('status') == 200:        _success += 1    else:        _failure_list.append(result)        _failure += 1        logging.warning('<aiohttpAPI.client._retry> Failure log:\r\n %s' % result)    if _count % 10 == 0:        logging.info(            '<aiohttpAPI.client._retry> Count %d/Success %d/Failure %d/Asyncio session %d' % (                _count, _success, _failure, _async))    if callback_function:        try:            callback_function(result)            return None        except Exception as e:            raise CallbackError('<aiohttpAPI.client._retry> callback_function Error %s' % e)    if filter_function:        try:            filter_result = filter_function(result)        except Exception as e:            raise FilterError('<aiohttpAPI.client._retry> filter_function Error %s' % e)        else:            if filter_result:                return filter_result    else:        return resultdef _get_urls(urls, semaphore=20, **kwargs):    """    To asynchronous getting datas from restful api.    :param urls: Input a url list for getting datas.    :param semaphore: The max sessions to connect servers at the same time.    :return: the result of the urls' content    """    global _count, _success, _failure, _failure_list, _async    _count = int()    _success = int()    _failure = int()    _failure_list = list()    _async = 1    if not isinstance(urls, (tuple, list, Iterator)):        raise TypeError('Must be tuple, list, Iterator')    loop = asyncio.get_event_loop()    sem = asyncio.Semaphore(semaphore, loop=loop)    kwargs['loop'] = loop    kwargs['sem'] = sem    result_list = list()    tasks = list()    for url in urls:        tasks.append(asyncio.ensure_future(_retry(url, **kwargs)))    start_time = int(time.time())    try:        loop.run_until_complete(asyncio.wait(tasks))    except Exception as e:        raise AiohttpError('<aiohttpAPI.client._get_urls> aiohttp Error %s' % e)    else:        logging.info('<aiohttpAPI.client._get_urls> Success: use %s s/count: %s/success: %s/failure: %s' % (            str(int(time.time()) - start_time), _count, _success, _failure))        if kwargs.get('callback_function'):            return None        for task in tasks:            if task.result():                result_list.append(task.result())        tasks.clear()        result_report = dict(count=_count, success=_success, failure=_failure, failure_list=_failure_list)        return result_list, result_reportdef _proc_result(urls, retry_failure=3, proc_function=None, **kwargs):    """    To asynchronous getting datas from restful api.    :param urls: Input a url list for getting datas.    :param retry_failure=3: When failure occur reload failure times, Flash or None is never reload, True is reload    :param proc_function: to process the result's content    :param retry_failure: when get failure to retry retry_failure times    :parameter :            retry_session=3: session failure retry times            retry_failure=3: When failure occur reload failure times, Flash or None is never reload, True is reload            while no failure            semaphore=20: The max sessions to connect servers at the same time.            timeout=1: the timeout of sessions            res_type='text': type of data. 'text':str 'bytes':bytes 'json':auto using json encoder            encode='utf-8': the data's str code            callback_function=None:  to process result in time            filter_function=None: to filter result's content            proc_function=None: to process the result's content    :return: the result of the urls' content    """    urls_retry = list()    result_get_urls = _get_urls(urls, **kwargs)    if isinstance(result_get_urls, tuple):        result_list = result_get_urls[0]        result_report = result_get_urls[1]    else:        return    if retry_failure:        if isinstance(retry_failure, int):            retry = 0        elif retry_failure is True:            retry = None        else:            raise AiohttpError('<aiohttpAPI.client._proc_result> retry_failure must be int or true')        while len(result_report['failure_list']) > 0:            for result in result_report['failure_list']:                urls_retry.append(result['url'])            kwargs['timeout'] = kwargs.get('timeout', 1) + 1            logging.info('<aiohttpAPI.client._proc_result> Start retry failure... Timeout set %s s' % kwargs['timeout'])            result_list_failure, result_report_failure = _get_urls(urls_retry, **kwargs)            urls_retry = list()            result_list += result_list_failure            result_report['success'] += result_report_failure['success']            result_report['failure'] -= result_report_failure['success']            result_report['failure_list'] = result_report_failure['failure_list']            if retry:                retry += 1                if retry == retry_failure:                    break    if proc_function:        try:            result_proc = proc_function(result_list)        except Exception as e:            raise ProcError('<aiohttpAPI.client._get_urls> proc_function Error %s' % e)        else:            return result_proc, result_report    else:        return result_list, result_reportdef get_urls(urls, **kwargs):    """    Try to getting the urls's data    :param urls: input urls list    :return: result    """    result = False    try:        result = _proc_result(urls, **kwargs)    except AiohttpError as e:        logging.warning('<aiohttpAPI.client.get_urls> Aiohttp Error %s' % e)    except CallbackError as e:        logging.warning('<aiohttpAPI.client.get_urls> Callback Error %s' % e)    except FilterError as e:        logging.warning('<aiohttpAPI.client.get_urls> Filter Error %s' % e)    except ProcError as e:        logging.warning('<aiohttpAPI.client.get_urls> Proc Error %s' % e)    except Exception as e:        logging.warning('<aiohttpAPI.client.get_urls> Unknown Error %s' % e)    finally:        return resultdef get_url(*url, **kwargs):    return get_urls(url, **kwargs)