#!/usr/bin/python3
#
# I have asked the great minds of Stack Overflow to come up with a Regular
# Expression to validate branch names. I got some great answers, so I thought
# I'd better test them.
#
# For bonus marks, I asked contributors to exclude branches starting with
# "build-".

import sys
import re

PATTERNS = (
  r'^(?!.*/\.)(?!.*\.\.)(?!/)(?!.*//)(?!.*@\{)(?!.*\\)[^\040\177 ~^:?*[]+/[^\040\177 ~^:?*[]+(?<!\.lock)(?<!/)(?<!\.)$', # Joey v1
  r'^(?!build-)(?!.*/\.)(?!.*\.\.)(?!/)(?!.*//)(?!.*@\{)(?!.*\\)[^\040\177 ~^:?*[]+/[^\040\177 ~^:?*[]+(?<!\.lock)(?<!/)(?<!\.)$', # Joey v2
  r'^(?!build-|/|.*([/.]\.|//|@\{|\\))[^\040\177 ~^:?*[]+/[^\040\177 ~^:?*[]+(?<!\.lock|[/.])$', # Joey v3
  r'refs/heads/(?!.)(?!build-)((?!\.\.)(?!@{)[^\cA-\cZ ~^:?*[\\])+)(?<!\.)(?<!\.lock)', # murgatroid99 v1
  r'(?!.)((?!\.\.)(?!@{)[^\cA-\cZ ~^:?*[\\])+)(/(?!.)((?!\.\.)(?!@{)[^\cA-\cZ ~^:?*[\\])+))*?/(?!.)(?!build-)((?!\.\.)(?!@{)[^\cA-\cZ ~^:?*[\\])+)(?<!\.)(?<!\.lock)' # murgatroid99 v2
)

SAMPLE = (
  ('refs/heads/master', True),
  ('refs/heads/production', True),
  ('refs/heads/v0.12-dev', True),
  ('refs/heads/build-master', False), # Starts with "build-"
  ('refs/tags/v0.12.0', False) # Not a branch...
)

def check(pat):
  p = re.compile(pat)
  for s in SAMPLE:
    m = p.search(s[0])
    print("{} {} {}".format(s[0], "Not matched" if m == None else "Matched", "PASS" if (m != None) == s[1] else "FAIL"))

def main():
  for pat in PATTERNS:
    print(pat)
    try:
      check(pat)
    except Exception as e:
      print("FAILED: {}".format(str(e)))

if __name__=='__main__':
  main()
