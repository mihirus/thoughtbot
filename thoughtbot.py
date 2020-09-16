from cmd import Cmd
import readline
import json 
import os 
import textwrap
import sys


class ThoughtBot(Cmd): 
   
   
   def __init__(self):
      '''
      Allows entry, filtering, editing, and deletion of thought strings. 
      Thought strings are thoughts that are put into words. 

      Requires python3
      ''' 

      super(ThoughtBot, self).__init__()
      self.prompt = 'thoughtbot > '
      self.thoughts = {
         'tags':{
            # 'ex1': [1,3], 
            # 'ex2': [1,2]
         },
         'entries':{
            # 1: 'here is the first thought', 
            # 2: 'here is the second thought', 
            # 3: 'here is the third thought'
         }
      }

      self.load_from_json()

   def load_from_json(self): 
      with open('data.json', 'r') as json_data: 
         self.thoughts = json.load(json_data)

   def save_to_json(self): 
      with open('data.json', 'w') as json_data: 
         json.dump(self.thoughts, json_data)

   def do_new_(self, args): 
      '''
      Add new thought to thoughtbot. 

      Usage:
      new_ <tag1> <tag2> thought_ <thought string> 

      A new thought must have a thought string and at least one tag. 
      '''

      # Find where thought_ is
      thought_index = args.find('thought_')

      # Leave if there is no thought_ 
      if thought_index == -1:
         return 
      
      # Get string after thought_ 
      thought_string = args[thought_index+8:len(args)].strip()
      
      # Add thoughtstring to entries 
      self.thoughts['entries'].update({str(len(self.thoughts['entries'])+1):thought_string})

      # Make a list of tags
      tags_list = args[0:thought_index].split()

      
      # Add thoughtstring num to corresponding tags 
      for tag in tags_list: 
         if tag in self.thoughts['tags']: 
            self.thoughts['tags'][tag].append(len(self.thoughts['entries']))
         else: 
            self.thoughts['tags'].update({tag:[len(self.thoughts['entries'])]})

      # Save to file after thought has been recorded 
      self.save_to_json()


   def do_load_(self, args): 
      '''
      Prints entries according to desired tags. 

      Usage: 
      load_ <tag1> <tag2> ... 

      Will print all entries that correspond to every given tag. 
      If no tag is specified, will load all entries with corresponding tags. 
      ''' 

      # Split up tags into list 
      args_list = args.split()

      # The entries with at least one specified tag, aka OR
      entry_contenders = []

      # Eventually contains the entries with all specified tags, aka AND
      entry_display = []

      # Populate entry contenders list
      for tag in args_list: 
         if tag in self.thoughts['tags']:
            entry_contenders.extend(self.thoughts['tags'][tag])

      # Populate entry display list 
      # If same number of entries in contender list as number of tags 
      # Then that entry must correspond to all tags
      # Based on how the above block is implemented
      # Therefore, append to entry display list once 
      for i in range(1, len(self.thoughts['entries'])+1): 
         if entry_contenders.count(i) == len(args_list) and \
         entry_display.count(i) == 0: 
            entry_display.append(i)


      # Get terminal size so that print can be done properly
      num_columns = os.get_terminal_size().columns
      
      # Print entry display list readably 
      print('\n')
      for i in range(0,len(entry_display)): 
         entry_str = str(entry_display[i]) + '\t' + self.thoughts['entries'][str(entry_display[i])]
         print(textwrap.fill(
            entry_str, 
            initial_indent='', 
            subsequent_indent=' '*8, 
            width=num_columns-20
         ))
      print('\n')


   def do_tags_(self, args):    
      '''
      Prints all available tags. 

      Format: 
      tags_ 
      ''' 

      print('\n')   
      # Print all tags 
      for key in self.thoughts['tags'].keys():
         print(key)
      print('\n')

   def do_delete_(self, args): 
      '''
      Deletes thought with given entry number. 
      Also removes tag correspondences. 

      Usage: 
      delete_ <entry number> 
      '''

      args_list = args.split()

      # If entry number isn't a key in entries, return 
      if args_list[0] not in self.thoughts['entries']:
         return  
      
      # Get rid of entry with entry number as key 
      self.thoughts['entries'].pop(args_list[0]) 

      # Reference to the tags dictionary 
      ref_to_tags = self.thoughts['tags']

      # List of tags to delete, in case certain tags only have deleted entry
      tags_to_delete = []

      # Pop entry number in each tag list
      for tag in ref_to_tags: 
         try: 
            ref_to_tags[tag].pop(ref_to_tags[tag].index(int(args_list[0])))
            if(len(ref_to_tags[tag])==0): 
               tags_to_delete.append(tag)
         # If entry number doesn't exist in tag list 
         except ValueError: 
            pass 

      # Pop tags if tag list is empty 
      for i in range(0, len(tags_to_delete)):
         ref_to_tags.pop(tags_to_delete[i])

      # Save to file after thought has been recorded 
      self.save_to_json()


   def do_edit_(self, args): 
      '''
      Edits tags and thought string of an entry. 
      Keeps entry number the same. 

      Usage: 
      
      Editing both tags and thought 
      edit_ <entry number> tags_ <new tag1> <new tag2> ... thought_ <new thought string> 
      
      To only edit tags, omit <new thought string> but keep thought_ 
      To only edit thought string, omit <new tags> but keep tag_ 
      ''' 

      # Make sure thought_ is present 
      try: 
         thought_string = args[args.index('thought_')+8:len(args)].strip()
      except ValueError: 
         return 

      # Split up everything before thought_ into tags list 
      args_list = args[0:args.index('thought_')].split()

      # Make sure tags_ is present
      if args_list[1] != "tags_": 
         return 

      # Entry number is the first item in list 
      # Only a string in entries, but already in entries 
      # So cast to int
      entry_number = int(args_list[0])
 
      # Edit tag list 
      tags_list = args_list[2:len(args_list)]

      # No edit tags, just change thought string  
      # Unless thought string is empty, in which case intent is to change tags
      if len(thought_string) > 0: 
         self.thoughts['entries'][str(entry_number)] = thought_string

      # List of tags that end up empty so they can be cleaned up 
      tags_to_delete = []

      ref_to_tags = self.thoughts['tags']
      for tag in ref_to_tags: 
         # Existing tag is an edit tag
         # And existing tag does not correspond to entry  
         if tags_list.count(tag) > 0 and ref_to_tags[tag].count(entry_number) == 0: 
            ref_to_tags[tag].append(entry_number)
            tags_list.pop(tags_list.index(tag))
         # Existing tag is an edit tag 
         # And existing tag does correspond to entry
         elif tags_list.count(tag) > 0 and ref_to_tags[tag].count(entry_number) > 0:
            tags_list.pop(tags_list.index(tag))
         # Existing tag is not an edit tag 
         # But existing tag does correspond to entry 
         elif tags_list.count(tag) == 0 and ref_to_tags[tag].count(entry_number) > 0:  
            tags_to_delete.append(tag)
   
      # Another loop so not editing existing tags while iterating over them
      # Edit tags left that do not already exist 
      for tag in tags_list: 
         ref_to_tags.update({tag : [entry_number]})

      # Another loop to remove empty tags 
      for tag in tags_to_delete: 
         ref_to_tags.pop(tag)
         
      # Save to file after thought has been recorded 
      self.save_to_json()

   def do_exit_(self, args): 
      '''
      Exits program and goes back to command line. 

      Usage: 
      exit_
      '''
      sys.exit(0)
      

if __name__=="__main__": 
   ThoughtBot().cmdloop()