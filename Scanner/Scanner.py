__author__ = "Jayde Yue"
# Website: www.jaydeyue.com

import queue
from DictWorker import DictWorker


class Scanner(object):

    def __init__(self, arguments):
        self.base_url = ''
        self.cookie = ''
        self.max_retrys = 3
        self.max_threads = 5
        self.time_out = 3
        self.referer = 'http://www.google.com'
        self.user = ''
        self.pwd = ''
        self.dict_paths = []
        self.allow_overlap = True
        self.allow_redirect = True
        self.all_trys = {}
        self.dict_stats = []
        self.redirect_list = {}

        # base_url, cookie, max_retrys, max_threads, time_out, referer, user, pwd
        arg_processing_tracker = [0,0,0,0,0,0,0,0]
        processing_dic = False
        processing_extension = False

        for arg in arguments:
            if arg_processing_tracker[0] == 1:
                self.base_url = arg
                arg_processing_tracker[0] +=1
            elif arg_processing_tracker[1] == 1:
                self.cookie = arg
                arg_processing_tracker[1] +=1
            elif arg_processing_tracker[2] == 1:
                self.max_retrys = int(arg)
                arg_processing_tracker[2] +=1
            elif arg_processing_tracker[3] == 1:
                self.max_threads = int(arg)
                arg_processing_tracker[3] +=1
            elif arg_processing_tracker[4] == 1:
                self.time_out = int(arg)
                arg_processing_tracker[4] +=1
            elif arg_processing_tracker[5] == 1:
                self.referer = arg
                arg_processing_tracker[5] +=1
            elif arg_processing_tracker[6] == 1:
                self.user = arg
                arg_processing_tracker[6] +=1
            elif arg_processing_tracker[7] == 1:
                self.pwd = arg
                arg_processing_tracker[7] +=1
            elif arg[0] == '-':
                if arg == '-d':
                    processing_dic = True
                    processing_extension = False
                elif arg == '-e':
                    processing_extension = True
                else:
                    if arg == '-u':
                        arg_processing_tracker[0] +=1
                    elif arg == '-c':
                        arg_processing_tracker[1] += 1
                    elif arg == '-mr':
                        arg_processing_tracker[2] += 1
                    elif arg == '-mt':
                        arg_processing_tracker[3] += 1
                    elif arg == '-to':
                        arg_processing_tracker[4] += 1
                    elif arg == '-r':
                        arg_processing_tracker[5] += 1
                    elif arg == '-user':
                        arg_processing_tracker[6] += 1
                    elif arg == '-pwd':
                        arg_processing_tracker[7] += 1
                    elif arg == '--no-overlap':
                        self.allow_overlap = False
                    elif arg == '--no-redirect':
                        self.allow_redirect = False
                    processing_dic = False
                    processing_extension = False
            elif processing_extension:
                if len(self.dict_paths) == 0:
                    print("Extensions should be added after the dictionary for which the extensions will be applied")
                    exit()
                else:
                    self.dict_paths[-1][1].append(arg)
            elif processing_dic:
                self.dict_paths.append((arg, []))
            else:
                if not all(count <=2 for count in arg_processing_tracker):
                    print("-u, -c, -mr, -mt, -to could be only used once")
                else:
                    print("Error processing argument: " + arg )
                exit()
        if not all(count <=2 for count in arg_processing_tracker):
            print("-u, -c, -mr, -mt, -to could be only used once")
            exit()

        if not self.base_url.startswith('http://') and not self.base_url.startswith('https://'):
            self.base_url = 'http://' + self.base_url
        if not self.base_url.endswith('/'):
            self.base_url = self.base_url + '/'

        print("base_url: " + self.base_url)
        print("cookie: " + self.cookie)
        print("max_retrys: " + str(self.max_retrys))
        print("max_threads: " + str(self.max_threads))
        print("time_out: " + str(self.time_out))
        print("allow_overlap: " + str(self.allow_overlap))
        print("allow_redirect: " + str(self.allow_redirect))
        print("scanning_dicts_path_with_added_extensions: ")
        print(self.dict_paths)

    def run(self):
        print("Scanning...Starts!")
        dict_count = 0
        for dict in self.dict_paths:
            if len(dict[1]) == 0:
                self.dict_stats.append(0)
                threads = []
                current_dict = queue.Queue()
                overlap_count = 0
                with open(dict[0],"r") as file:
                    for line in file:
                        line = line.strip('\n')
                        if line not in self.all_trys:
                            current_dict.put(self.base_url + line)
                            self.all_trys[line] = 0
                        elif self.all_trys[line] == 1:
                            overlap_count += 1
                dict_size = current_dict.qsize()
                for i in range(self.max_threads):
                    threads.append(DictWorker(current_dict, self, dict_count))
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                valid_result_count = overlap_count + self.dict_stats[dict_count]
                print("Dictionary: " + dict[0] + "; Size: " + str(dict_size) + "; Valid results: " + str(valid_result_count) + "; Hit rate: " +str(valid_result_count/dict_size))
            else:
                for ext in dict[1]:
                    self.dict_stats.append(0)
                    threads = []
                    current_dict = queue.Queue()
                    overlap_count = 0
                    with open(dict[0],"r") as file:
                        for line in file:
                            line = line.strip('\n')
                            if line not in self.all_trys:
                                current_dict.put(self.base_url + line + "." + ext)
                                self.all_trys[line+ "." + ext] = 0
                            elif self.all_trys[line+ "." + ext] == 1:
                                overlap_count += 1
                    dict_size = current_dict.qsize()
                    for i in range(self.max_threads):
                        threads.append(DictWorker(current_dict, self, dict_count))
                    for t in threads:
                        t.start()
                    for t in threads:
                        t.join()
                    valid_result_count = overlap_count + self.dict_stats[dict_count]
                    print("Dictionary: " + dict[0] + "; With extension: " + ext + "; Size: " + str(dict_size) + "; Valid results: " + str(valid_result_count) + "; Hit rate: " + str(valid_result_count/dict_size))
        for redirected_url, redirect_count in self.redirect_list.items():
            print("Redirected to " + redirected_url + ": " + str(redirect_count) + " times")
