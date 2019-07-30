# JTools

## Scanning Tools

### Directory Scanning

DirScanner: A simple directory and sensitive files scanning tool for pen testers.\
简单的敏感目录和文件扫描工具

cd Scanner\
python3 scan.py\
-u http://www.example.com \
-d path_to_dict1 path_to_dict2 ...\
-e 1st_extention_added_to_dict2 2nd_extention_added_to_dict2 ...\
-d path_to_dict3 ...\
-c cookie\
-r referer (default to google)\
-mr max_retrys\
-mt max_threads\
-to timeout\
-user username_for_authentication_purpose\
-pwd password_for_authentication_purpose\
--no-redirect: no redirecting\
--no-overlap: If put into the command, the program will run from dict1 to dict3, while avoiding repeated dictionary items; otherwise overlaps of paths between different dictionary will be allowed

#### TODO
better redirected url handling\
changing stats to display hit rate with status code 200 and hit rate with all other status\
an optional and default path to save the result to\
find common dicts/sensitive file names
