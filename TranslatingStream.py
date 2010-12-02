#!/usr/bin/env python

"""This module defines a class that can be fed a stream of data piece by piece. 

Perhaps it should also keep track of the time of each data, and unblock itself
after a timeout?
"""

class TranslatingStream:
    def __init__(self,search,replacement):
        self.__search = search
        self.__replacement = replacement
        self.__search_length = len(self.__search)
        self.__buffer = ""
    def feed(self,new_data):
        self.__buffer = self.__buffer + new_data
    def __does_pos_x_match_search_text_prefix(self,x):
        prefix_length = self.__search_length
        if len(self.__buffer) < x + prefix_length:
            prefix_length = len(self.__buffer) - x
        return self.__buffer[x:x+prefix_length] == self.__search[:prefix_length]
    def __does_pos_x_match_search_text(self,x):
        return self.__buffer[x:x+self.__search_length] == self.__search
    def is_constipated(self):
        """Are we unable to harvest any further because we need more input before we can know whether we've hit a search term or not?"""
        if self.__buffer == "": return False
        return (not(self.__does_pos_x_match_search_text(0)) 
                and
                self.__does_pos_x_match_search_text_prefix(0)
                )
    def __harvest_next(self,more_feeds_to_come=True):
        if self.__buffer == "": return ""
        if self.is_constipated(): return ""
        if self.__does_pos_x_match_search_text(0):
            self.__buffer = self.__buffer[self.__search_length:]
            return self.__replacement
        for i in range(len(self.__buffer)):
            if self.__does_pos_x_match_search_text(i):
                unchanged = self.__buffer[:i]
                self.__buffer = self.__buffer[i:]
                return unchanged
            if more_feeds_to_come and self.__does_pos_x_match_search_text_prefix(i):
                # have to stop here and wait for more data
                unchanged = self.__buffer[:i]
                self.__buffer = self.__buffer[i:]
                return unchanged
        # We made it to the end of the loop without anything matching
        unchanged = self.__buffer[:]
        self.__buffer = ""
        return unchanged
    def harvest(self,more_to_come=True):
        answer = ""
        next_chunk = self.__harvest_next(more_to_come)
        while next_chunk != "":
            answer = answer + next_chunk
            next_chunk = self.__harvest_next(more_to_come)
        return answer
                
        

    
