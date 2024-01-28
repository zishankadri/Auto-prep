from django import template

register = template.Library()

# Subtract
@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

# TIMES
@register.filter(name='times') 
def times(model):
    num = len(model)
    return range(num)


# SIMPLIFY
@register.filter(name='simplify') 
def simplify(n):
    """ (142.1398724) -> (142.14) """
    return "%.2f" % n


# GETVAL
@register.filter(name='getval')
def getval(dict, key):
    return dict[key]


# GET
@register.filter(name='get')
def get(obj, element_str):
    # val = obj.__dict__[element_str]
    element_arr = element_str.split(".")
    if len(element_arr) > 1:
        current = obj
        for element in element_arr:
            current = getattr(current, element)
        
        return current
        
    val = getattr(obj, element_str)

    if isinstance(val, float):  # If float
        return f"${simplify(val)}"  # 142.1398714 -> $142.14
    
    return val


# REMOVE
@register.filter(name='remove')
def remove(list, args):
    my_list = list.copy()
    for i in args.split(","):
        my_list.remove(i)
    return my_list


# Get Vote
@register.filter(name='get_vote')
def get_vote(stock, i):
    return stock.votes[i]


# Get Vote
@register.filter(name='get_rank')
def get_rank(rank):
    # return f"{rank}"
    if rank == 1: return f"1 st"
    if rank == 2: return f"2 nd"
    if rank == 3: return f"3 rd"
    # else:
    return f"{rank} th"


# Get Vote
@register.filter(name='getName')
def getName(class_str):
    import re
    result = re.search("'(.*)'", class_str)
    return result.group(1)


# Gets the name of the passed in field on the passed in object
@register.filter
def verbose_name(the_object, the_field):
    try:
        # Check if the verbose name is using the default value, in which case it will be all lowercase
        if the_object._meta.get_field(the_field).verbose_name.islower:
            # Change
            return the_object._meta.get_field(the_field).verbose_name.capitalize()
        else:
            # The verbose name has been set in the model, so just display it normally
            return the_object._meta.get_field(the_field).verbose_name
    except:
        return the_field
    

# CUSTOM ADMIN
from django.contrib.humanize.templatetags.humanize import intcomma
@register.filter
def currency(dollars):
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
