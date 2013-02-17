#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""\
Mdig
Copyright (C) Zhou Changrong
"""

import os, sys, pycurl, StringIO, types, re, getopt, time, platform
reload(sys)
sys.setdefaultencoding('utf-8')

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
				raise TypeError, 'http_request() got an unexpected keyword argument \'%s\'' %(key)
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
				raise TypeError, 'http_request() got an unexpected keyword argument \'%s\'' %(key)
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
	cs = {}
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
				raise TypeError, 'http_request() got an unexpected keyword argument \'%s\'' %(key)
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
		self.m.add_handle(c)
		self.cs[c]=[b, h, other_data]
		return None
	def perform(self):
		start = time.time()
		while True:
			ret, num = self.m.perform()
			if ret == pycurl.E_CALL_MULTI_PERFORM:
				continue
			ret, handlers, others = self.m.info_read()
			now = time.time()
			total_time = now - start
			for c in handlers:
				self.m.remove_handle(c)
				b, h, other_data = self.cs[c]
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
				self.cs[c] = None
			for o in others:
				c, code, msg = o
				self.m.remove_handle(c)
				b, h, other_data = self.cs[c]
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
				self.cs[c] = None
			if num == 0:
				break
			ret = self.m.select(1.0)
	def close(self):
		for c in self.cs:
			if c != None:
				c.close()
		m = self.m
		if m != None:
			m.close()

def usage():
	print "Usage: %s [OPTIONS...] <uri|domain>" %(sys.argv[0])
	print
	print "Options:"
	print " -c/--connect-timeout=<int>  connect timeout"
	print " -m/--method=<string>        Method"
	print " -t/--timeout=<int>          timeout"
	print " -h/--help          Display this page and exit"
	print " -v/--version       Display version and exit"

def line_out(result, other_data, code = 0, msg = None):
	print ('%-14s %-19s %-14d %-14d %5.6f          %-14s %5d %s' %(other_data[0], other_data[1], result['code'], result['body_size'], result['total_time'], other_data[2], code, msg))

def main():
	get_uri = False
	port = 80
	method = 'GET'
	timeout = 0
	connect_timeout = 0
	try:
		opts,args = getopt.gnu_getopt(sys.argv[1:], "c:t:m:hv", ["connect-timeout=", "timeout=", "method=", "help", "version"])
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
			elif opt in ("-h", "--help"):
				usage()
				os._exit(0)
			elif opt in ("-v", "--version"):
				print "version %s" %version
				os._exit(0)
	except getopt.GetoptError, e:
		sys.stderr.write("Error: %s\n" %(e))
		os._exit(1)
	if len(args) > 1:
		sys.stderr.write("Error: Too many arguments\n")
		usage()
		os._exit(1)
	elif len(args) < 1:
		sys.stderr.write("Error: Too few arguemnts\n")
		usage()
		os._exit(1) 
	uri = args[0]
	m = re.match(r'^(http://)?(.+?)(:(\d+))?(/.*)?$', uri)
	if not m:
		print >>sys.stderr, "无效参数"
		os._exit(1)
	groups = m.groups()
	if groups[0] is not None or groups[2] is not None or groups[4] is not None:
		get_uri = True
	domain_name = groups[1]
	# python 2.4 not support
	#port = port if groups[3] is None else int(groups[3])
	if groups[3] is not None:
		port = int(groups[3])
	data = 'query_type=A&domain_name=%s&city=6,7,8,1,2,3,4,5,15,27,28,29,30,31,22,23,24,25,26,16,17,18,9,10,11,12,13,14,19,20,21,32,33,34,36,37&isp=1,2,3,5,8&rand=13739' %(domain_name)
	i = 0
	while i < 3:
		if i>0:
			print >>sys.stderr, "正在重试1..."
		try:
			h = httprequest()
			result = h.request('http://tools.fastweb.com.cn/index.php/Index/sendMdig',
					method = 'POST',
					post_data = data)
			h.close()
		except pycurl.error, e:
			print >>sys.stderr, "%s" %e
			os._exit(1)

		s = json.loads(result['body'])
		if not s['status'] or type(s['data']) is not types.DictType:
			print >>sys.stderr, "没有取到结果1"
			os._exit(1)
		else:
			break
		i+=1
	
	data = 'task_id=%d&view_ids=%s&from=mdig&query_type=A&result_id=0' %(s['data']['task_id'], str(s['data']['view_ids']))
	i = 0
	while i < 3:
		if i>0:
			print >>sys.stderr, "正在重试2..."
		try:
			h = httprequest()
			result = h.request('http://tools.fastweb.com.cn/index.php/Index/getMdigResultOne',
					method = 'POST',
					post_data = data)
			h.close()
		except pycurl.error, e:
			print >>sys.stderr, "%s" %e
			os._exit(1)

		s = json.loads(result['body'])
		if not s['status'] or type(s['data']) is not types.DictType:
			print >>sys.stderr, "没有取到结果2"
		else:
			break
		i+=1
	#print json.dumps(s, indent=4)
	h = mhttprequest(line_out)
	if get_uri:
		print "zone                ip                  return_code    length         use_time            provider     errno  message"
		print "====================================================================================================================="
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
					print r['view_name']
				print "IN %s %s"  %(r['type_trans'], r['result_trans'])
		if not get_uri:
			print
	if get_uri:
		h.perform()
	h.close()
	
main()
	

