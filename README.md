python_tools
============
A collection of small programs I've written that I think may be useful in the future  
Index:
--------------
- **context_profiler.py**  
  As seen [here](http://codereview.stackexchange.com/questions/68789/subclassing-profile-profile-to-use-it-as-a-context-manager). 
  This is a tool I wrote in order to better profile chunks of my code at a time.  I was annoyed by having to continually call Profile.run() so I made it a context manager that does that for me

- **strip_whitespace.py**  
  I started using an [online PEP8 checking tool](http://pep8online.com/) and it kept flagging me for mixing spaces/tabs, having lines with just whitespace, EOL whitespace, etc.  This tool (more or less) removes all of it and cleans that up

- **to_blockdiag.py**  
  There is a pretty nifty utility called [blockdiag](http://blockdiag.com/en/).  It was an easy way for me to generate simple   images based on a graph.  This just automates the process, minimizing work for the programmer (me)

- **to_csv.py**  
  This just converts space-delimited text files to comma delimited csv files. Much nicer than doing it by hand

- **docstring_checker.py**
  Tool that checks which non-private functions and classes I've written that don't have docstrings.

- **import_finder.py**
  The idea was to use this in conjunction with `docstring_checker` to check imported modules as well (but not check python builtins).  Could use a lot of work

- **property_fun.py**
  I thought it would be interesting to play around with metaclasses and properties.  I want to add either decorators or metaclasses (or both) that give me the ability to turn every attribute of a class into a property at runtime, so no one has to type in all that cruft.  This isn't particularly useful - there is no reason to make something into a property (that I can think of) unless it has non-trivial set/get/delete behavior.  Needs work
