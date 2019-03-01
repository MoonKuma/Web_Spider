#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : WaitingList.py
# @Author: MoonKuma
# @Date  : 2019/3/1
# @Desc  : class WaitingList for adding, storing, and popping links to the compute module

import threading


class WaitingList(object):

    def __init__(self, timeout=10, root=""):
        self.Marking_Set = set()  # this marks all links that have been added
        self.Waiting_List = list()  # waiting list used to store links for further execution
        self.sem_lock = threading.Semaphore(1)  # locks the adding the popping steps
        self.timeout = timeout
        if root != "":
            self.Waiting_List.append(root)
            self.Marking_Set.add(root)

    def add_links(self, links):
        if self.sem_lock.acquire(blocking=True, timeout=self.timeout):
            for link in links:
                if str(link) not in self.Marking_Set:
                    self.Marking_Set.add(str(link))
                    self.Waiting_List.append(str(link))
            self.sem_lock.release()

    def pop_link(self):
        link = ""
        if self.sem_lock.acquire(blocking=True, timeout=self.timeout):
            if len(self.Waiting_List) > 0:
                link = self.Waiting_List.pop()
            self.sem_lock.release()
        return link

    def get_length_marking(self):
        return len(self.Marking_Set)

    def get_length_waiting(self):
        return len(self.Waiting_List)
