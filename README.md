# Thoughtbot

Thoughtbot is a command line based mind mapper. It supports entry, editing, filtering, and deletion of tagged thoughts. Think of it as a text based Venn-diagram.

## Installation

Make sure you have Python 3 installed. 

```bash
sudo apt install python3
```

## Usage

To open: 
```
python3 main.py
```

To add a new entry: 
```python
thoughtbot > new_ <tag1> <tag2> ... thought_ <thought string> 
```

To list all tags: 
```
thoughtbot > tags_ 
```

To load entries with certain tags: 
```
thoughtbot > load_ <tag1> <tag2> ... 
```

To edit an entry: 
```
thoughtbot > edit_ <entry number> tags_ <new tag1> <new tag2> ... thought_ <new thought string> 
```

To delete an entry: 
```
thoughtbot > delete_ <entry number> 
```

The file named 'data' is a template. Simply rename it to 'data.json' and start the program. 