#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""\
Mdig
Copyright (C) Zhou Changrong
"""

import os, sys, pycurl, StringIO, types, re, getopt, time, platform, locale
reload(sys)
sys.setdefaultencoding("UTF8")

version = "0.1.0"

# python less 2.6.0
# json module is simplejson
if platform.python_version() < '2.6.0':
	import simplejson as json
else:
	import json

class httprequest:
	def __init__(self, **args):
		self.c = None
		self.proxy_host = None
		self.proxy_port = None
		self.user_agent = None
		self.post_data = None
		self.headers = None
		self.method = None
		self.max_redirs = None
		self.followlocation = None
		self.connect_timeout = 0
		self.timeout = 0
		self.verbose = None
		self.version = None
		self.userpwd = None
		for key in args.keys():
			if key == 'proxy_host':
				self.proxy_host = args['proxy_host']
			elif key == 'proxy_port':
				self.proxy_port = args['proxy_port']
			elif key == 'user_agent':
				self.user_agent = args['user_agent']
			elif key == 'post_data':
				self.post_data = args['post_data']
			elif key == 'headers':
				self.headers = args['headers']
			elif key == 'method':
				self.method = args['method']
			elif key == 'max_redirs':
				self.max_redirs = args['max_redirs']
			elif key == 'followlocation':
				self.fllowlocation = args['followlocation']
			elif key == 'connect_timeout':
				self.connect_timeout = args['connect_timeout']
			elif key == 'timeout':
				self.timeout = args['timeout']
			elif key == 'verbose':
				self.verbose = args['verbose']
			elif key == 'userpwd':
				self.userpwd = args['userpwd']
			else:
				raise TypeError, 'httprequest() got an unexpected keyword argument \'%s\'' %(key)
		self.c = pycurl.Curl()
	def request(self, url = None, **args):
		c = self.c
		proxy_host = self.proxy_host
		proxy_port = self.proxy_port
		user_agent = self.user_agent
		post_data = self.post_data
		headers = self.headers
		method = self.method
		max_redirs = self.max_redirs
		followlocation = self.followlocation
		connect_timeout = self.connect_timeout
		timeout = self.timeout
		verbose = self.verbose
		version = self.version
		userpwd = self.userpwd
		result = {}
		for key in args.keys():
			if key == 'proxy_host':
				proxy_host = args['proxy_host']
			elif key == 'proxy_port':
				proxy_port = args['proxy_port']
			elif key == 'user_agent':
				user_agent = args['user_agent']
			elif key == 'post_data':
				post_data = args['post_data']
			elif key == 'headers':
				headers = args['headers']
			elif key == 'method':
				method = args['method']
			elif key == 'max_redirs':
				max_redirs = args['max_redirs']
			elif key == 'followlocation':
				fllowlocation = args['followlocation']
			elif key == 'connect_timeout':
				connect_timeout = args['connect_timeout']
			elif key == 'timeout':
				timeout = args['timeout']
			elif key == 'verbose':
				verbose = args['verbose']
			elif key == 'version':
				version = args['version']
			elif key == 'userpwd':
				userpwd = args['userpwd']
			else:
				raise TypeError, 'request() got an unexpected keyword argument \'%s\'' %(key)
		c.setopt(c.URL, url)
		if proxy_host != None:
			c.setopt(c.PROXY, proxy_host)
			if proxy_port != None and proxy_port != 0:
				c.setopt(c.PROXYPORT, proxy_port)
		if user_agent != None:
			c.setopt(c.USERAGENT, user_agent)
		if headers != None and len(headers) > 0:
			c.setopt(c.HTTPHEADER, headers)
		if method != None:
			c.setopt(c.CUSTOMREQUEST, method)
		if method == 'POST' and post_data != None:
			c.setopt(c.POSTFIELDS, post_data)
		if followlocation != None:
			c.setopt(c.FOLLOWLOCATION, followlocation)
		if verbose != None:
			c.setopt(c.VERBOSE, verbose)
		if version != None:
			c.setopt(c.HTTP_VERSION, version)
		if userpwd != None:
			c.setopt(c.USERPWD, userpwd)
		if method == 'HEAD':
			c.setopt(c.NOBODY, True)
		b = StringIO.StringIO()
		h = StringIO.StringIO()
		c.setopt(c.WRITEFUNCTION, b.write)
		c.setopt(c.HEADERFUNCTION, h.write)
		c.setopt(c.HEADER, False)
		if timeout > 0:
			c.setopt(c.TIMEOUT, timeout)
		if connect_timeout > 0:
			c.setopt(c.CONNECTTIMEOUT, connect_timeout)
		c.perform()
		result['code'] = c.getinfo(c.HTTP_CODE)
		result['body'] = b.getvalue()
		result['header'] = h.getvalue()
		b.close()
		h.close()
		result['header_size'] = c.getinfo(c.HEADER_SIZE)
		result['body_size'] = len(result['body'])
		result['total_time'] = c.getinfo(c.TOTAL_TIME)
		result['speed_download'] = c.getinfo(c.SPEED_DOWNLOAD)
		result['speed_upload'] = c.getinfo(c.SPEED_UPLOAD)
		result['size_download'] = c.getinfo(c.SIZE_DOWNLOAD)
		result['size_upload'] = c.getinfo(c.SIZE_UPLOAD)
		return result
	def close(self):
		c = self.c
		if c != None:
			c.close()
class mhttprequest:
	handles = {}
	def __init__(self, line_out = None):
		self.line_out = line_out
		self.m = pycurl.CurlMulti()
	def add_request(self, url = None, **args):
		c = pycurl.Curl()
		proxy_host = None
		proxy_port = None
		user_agent = None
		post_data  = None
		headers    = None
		method     = None
		max_redirs = None
		followlocation = None
		connect_timeout = None
		timeout = 0
		verbose = 0
		version = None
		userpwd = None
		other_data = None
		result = {}
		for key in args.keys():
			if key == 'proxy_host':
				proxy_host = args['proxy_host']
			elif key == 'proxy_port':
				proxy_port = args['proxy_port']
			elif key == 'user_agent':
				user_agent = args['user_agent']
			elif key == 'post_data':
				post_data = args['post_data']
			elif key == 'headers':
				headers = args['headers']
			elif key == 'method':
				method = args['method']
			elif key == 'max_redirs':
				max_redirs = args['max_redirs']
			elif key == 'followlocation':
				fllowlocation = args['followlocation']
			elif key == 'connect_timeout':
				connect_timeout = args['connect_timeout']
			elif key == 'timeout':
				timeout = args['timeout']
			elif key == 'verbose':
				verbose = args['verbose']
			elif key == 'version':
				version = args['version']
			elif key == 'userpwd':
				userpwd = args['userpwd']
			elif key == 'other_data':
				other_data = args['other_data']
			else:
				raise TypeError, 'add_request() got an unexpected keyword argument \'%s\'' %(key)
		c.setopt(c.URL, url)
		if proxy_host != None:
			c.setopt(c.PROXY, proxy_host)
			if proxy_port != None and proxy_port != 0:
				c.setopt(c.PROXYPORT, proxy_port)
		if user_agent != None:
			c.setopt(c.USERAGENT, user_agent)
		if headers != None and len(headers) > 0:
			c.setopt(c.HTTPHEADER, headers)
		if method != None:
			c.setopt(c.CUSTOMREQUEST, method)
		if method == 'POST' and post_data != None:
			c.setopt(c.POSTFIELDS, post_data)
		if followlocation != None:
			c.setopt(c.FOLLOWLOCATION, followlocation)
		if verbose != None:
			c.setopt(c.VERBOSE, verbose)
		if version != None:
			c.setopt(c.HTTP_VERSION, version)
		if userpwd != None:
			c.setopt(c.USERPWD, userpwd)
		if method == 'HEAD':
			c.setopt(c.NOBODY, True)
		b = StringIO.StringIO()
		h = StringIO.StringIO()
		c.setopt(c.WRITEFUNCTION, b.write)
		c.setopt(c.HEADERFUNCTION, h.write)
		c.setopt(c.HEADER, False)
		if timeout > 0:
			c.setopt(c.TIMEOUT, timeout)
		if connect_timeout > 0:
			c.setopt(c.CONNECTTIMEOUT, connect_timeout)
		self.handles[c]=[b, h, other_data]
		return None
	def perform(self, max_connections = 0):
		handle_list = self.handles.keys()
		n = len(handle_list)
		current_connections = 0
		i = 0
		while True:
			while i<n and (current_connections<max_connections or max_connections == 0):
				self.m.add_handle(handle_list[i])
				self.handles[handle_list[i]].append(time.time())
				i+=1
				current_connections += 1
			ret, num = self.m.perform()
			if ret == pycurl.E_CALL_MULTI_PERFORM:
				continue
			ret, handlers, others = self.m.info_read()
			now = time.time()
			for c in handlers:
				self.m.remove_handle(c)
				b, h, other_data, start = self.handles[c]
				total_time = now - start
				result = {}
				result['code'] = c.getinfo(c.HTTP_CODE)
				result['body'] = b.getvalue()
				result['header'] = h.getvalue()
				b.close()
				h.close()
				result['header_size'] = c.getinfo(c.HEADER_SIZE)
				result['body_size'] = len(result['body'])
				#result['total_time'] = c.getinfo(c.TOTAL_TIME)
				result['total_time'] = total_time
				result['speed_download'] = c.getinfo(c.SPEED_DOWNLOAD)
				result['speed_upload'] = c.getinfo(c.SPEED_UPLOAD)
				result['size_download'] = c.getinfo(c.SIZE_DOWNLOAD)
				result['size_upload'] = c.getinfo(c.SIZE_UPLOAD)
				self.line_out(result, other_data)
				c.close()
				del(self.handles[c])
				current_connections -= 1
			for o in others:
				c, code, msg = o
				self.m.remove_handle(c)
				b, h, other_data, start = self.handles[c]
				total_time = now - start

				result = {}
				result['code'] = c.getinfo(c.HTTP_CODE)
				result['body'] = b.getvalue()
				result['header'] = h.getvalue()
				b.close()
				h.close()
				result['header_size'] = c.getinfo(c.HEADER_SIZE)
				result['body_size'] = len(result['body'])
				result['total_time'] = total_time
				result['speed_download'] = c.getinfo(c.SPEED_DOWNLOAD)
				result['speed_upload'] = c.getinfo(c.SPEED_UPLOAD)
				result['size_download'] = c.getinfo(c.SIZE_DOWNLOAD)
				result['size_upload'] = c.getinfo(c.SIZE_UPLOAD)
				self.line_out(result, other_data, code, msg)
				c.close()
				del(self.handles[c])
				current_connections -= 1
			#print num, i, n, current_connections, max_connections
			if num == 0 and i == n:
				break
			ret = self.m.select(1.0)
	def close(self):
		for c in self.handles.keys():
			if c != None:
				c.close()
		m = self.m
		if m != None:
			m.close()

def usage():
	print u"Usage: %s [OPTIONS...] <uri|domain>" %(sys.argv[0])
	print
	print u"Options:"
	print u" -c/--connect-timeout=<int>  connect timeout"
	print u" -m/--method=<string>        Method"
	print u" -t/--timeout=<int>          timeout"
	print u" -n/--max-connections=<int>  max connections"
	print u" -h/--help          Display this page and exit"
	print u" -v/--version       Display version and exit"

def line_out(result, other_data, code = 0, msg = None):
	print (u'%-14s %-19s %-14d %-14d %5.6f          %-14s %5d %s' %(other_data[0], other_data[1], result['code'], result['body_size'], result['total_time'], other_data[2], code, msg))

def main():
	get_uri = False
	port = 80
	method = 'GET'
	timeout = 0
	connect_timeout = 0
	max_connections = 10
	try:
		opts,args = getopt.gnu_getopt(sys.argv[1:], "c:n:t:m:hv", ["connect-timeout=", "max-connections=", "timeout=", "method=", "help", "version"])
		for opt,arg in opts:
			if opt in ("-m", "--method"):
				method = arg
			elif opt in ("-c", "--connect-timeout"):
				try:
					connect_timeout = int(arg)
				except ValueError, e:
					print >>sys.stderr, "option '%s': %s" %(opt, e)
					os._exit(1)

			elif opt in ("-t", "--timeout"):
				try:
					timeout = int(arg)
				except ValueError, e:
					print >>sys.stderr, "option '%s': %s" %(opt, e)
					os._exit(1)
			elif opt in ("-n", "--max-connections"):
				try:
					max_connections = int(arg)
				except ValueError, e:
					print >>sys.stderr, "option '%s': %s" %(opt, e)
					os._exit(1)

			elif opt in ("-h", "--help"):
				usage()
				os._exit(0)
			elif opt in ("-v", "--version"):
				print u"version %s" %version
				os._exit(0)
	except getopt.GetoptError, e:
		sys.stderr.write(u"Error: %s\n" %(e))
		os._exit(1)
	if len(args) > 1:
		sys.stderr.write(u"Error: Too many arguments\n")
		usage()
		os._exit(1)
	elif len(args) < 1:
		sys.stderr.write(u"Error: Too few arguemnts\n")
		usage()
		os._exit(1) 
	uri = args[0]
	m = re.match(r'^(http://)?(.+?)(:(\d+))?(/.*)?$', uri)
	if not m:
		print >>sys.stderr, u"无效参数"
		os._exit(1)
	groups = m.groups()
	if groups[0] is not None or groups[2] is not None or groups[4] is not None:
		get_uri = True
	domain_name = groups[1]
	# python 2.4 not support
	#port = port if groups[3] is None else int(groups[3])
	if groups[3] is not None:
		port = int(groups[3])
	try:
		h = httprequest()
		result = h.request('http://tools.fastweb.com.cn/index.php/Index/Mdig',
				method = 'GET')
		h.close()
	except pycurl.error, e:
		print >>sys.stderr, u"%s" %e
		os._exit(1)
	m = re.search(r'PHPSESSID=(.+?);', result['header'], re.S)
	if not m:
		print >>sys.stderr, u"没有取到PHPSESSID"
		os._exit(1)
	phpsessid = m.groups()[0]
	

	m = re.search(r'name="sid" value="(.+?)"', result['body'], re.S)
	if not m:
		print >>sys.stderr, u"没有取到sid"
		os._exit(1)
	sid = m.groups()[0]
	data = 'query_type=A&domain_name=%s&city=6,7,8,1,2,3,4,5,15,27,28,29,30,31,22,23,24,25,26,16,17,18,9,10,11,12,13,14,19,20,21,32,33,34,36,37&isp=1,2,3,5,8&rand=13739&sid=%s' %(domain_name, sid)
	i = 0
	while i < 3:
		if i>0:
			print >>sys.stderr, u"正在重试1..."
		try:
			h = httprequest()
			result = h.request('http://tools.fastweb.com.cn/index.php/Index/sendMdig',
					method = 'POST',
					headers = ["Cookie: PHPSESSID=%s" %phpsessid],
					post_data = data)
			h.close()
		except pycurl.error, e:
			print >>sys.stderr, "%s" %e
			os._exit(1)

		try:
			s = json.loads(unicode(result['body'], 'UTF-8'))
		except:
			print >>sys.stderr, u"无效的: %s" %(result['body'])
			continue
		if not s['status'] or type(s['data']) is not types.DictType:
			print >>sys.stderr, u"没有取到结果1"
		else:
			break
		i+=1
	
	data = 'task_id=%d&view_ids=%s&from=mdig&query_type=A&result_id=0' %(s['data']['task_id'], str(s['data']['view_ids']))
	i = 0
	while i < 3:
		if i>0:
			print >>sys.stderr, u"正在重试2..."
		try:
			h = httprequest()
			result = h.request('http://tools.fastweb.com.cn/index.php/Index/getMdigResultOne',
					method = 'POST',
					headers = ["Cookie: PHPSESSID=%s" %phpsessid],
					post_data = data)
			h.close()
		except pycurl.error, e:
			print >>sys.stderr, u"%s" %e
			os._exit(1)
		try:
			s = json.loads(result['body'])
		except:
			print >>sys.stderr, u"无效的: %s" %(result['body'])
			continue
		if not s['status'] or type(s['data']) is not types.DictType:
			print >>sys.stderr, u"没有取到结果2"
		else:
			break
		i+=1
	#print json.dumps(s, indent=4)
	h = mhttprequest(line_out)
	if get_uri:
		print "zone                ip                  return_code    length         use_time            provider     errno  message"
		print "====================================================================================================================="
	del s['data']['result_id']
	for view_id in s['data'].keys():
		view_name_out = False
		for r in s['data'][view_id]:
			if get_uri:
				if r['type_trans'] != 'A':
					continue
				m = re.match(r'^(.+?)\((.*)\)$', r['result_trans'])
				groups = m.groups()
				host = str(groups[0])
				provider = groups[1]
				data = [r['view_name'], host, provider]
				try:
					result = h.add_request(uri,
						proxy_host = host,
						proxy_port = port,
						method = method,
						timeout = timeout,
						connect_timeout = connect_timeout,
						other_data = data)
				except pycurl.error, e:
					print >>sys.stderr, "%s" %e
					continue
			else:
				if not view_name_out:
					view_name_out = True
					print u"%s %s:" %(r['view_name'], r['from_ip_trans'])
				print u"IN %s %s"  %(r['type_trans'], r['result_trans'])
		if not get_uri:
			print
	if get_uri:
		h.perform(max_connections)
	h.close()
	
main()
	

