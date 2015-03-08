# -*- coding: utf-8 -*-

## Adapted list of regular expressions proposed by Brendan O'Connor and Kevin Gimpel for tweet tokenization 

def regex_or(*items):
    r = '|'.join(items)
    r = '(' + r + ')'
    return r

def pos_lookahead(r):
    return '(?=' + r + ')'

def neg_lookahead(r):
    return '(?!' + r + ')'

def optional(r):
    return '(%s)?' % r

def punct_chars():
    return r'''['“".?!,:;]'''

def common_tlds():
    return regex_or('com','co\\.uk','org','net','info','ca','edu','gov')

def url():
    UrlStart1 = regex_or('https?://', r'www\.')
    UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + common_tlds() + pos_lookahead(r'[/ \W\b]')
    UrlBody = r'[^ \t\r\n<>]*?'  # * not + for case of:  "go to bla.com." -- don't want period
    UrlExtraCrapBeforeEnd = '%s+?' % regex_or(punct_chars(), entity())
    UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$')

    Url = (r'\b' +
        regex_or(UrlStart1, UrlStart2) +
        UrlBody +
        pos_lookahead( optional(UrlExtraCrapBeforeEnd) + UrlEnd))

    return Url

def email():
    EmailName = r'([a-zA-Z0-9-_+]+[.])*[a-zA-Z0-9-_+]+'
    EmailDomain = r'([a-zA-Z0-9]+[.])+' + common_tlds()
    return EmailName + "@" + EmailDomain

def entity():
    return '&(amp|lt|gt|quot);'

def hashtag():
    return r'#[a-zA-Z0-9_]+'

def at_mention():
    return r'@[a-zA-Z0-9_]+'

def time_like():
    return r'\d+:\d+'

def num_num():
    return r'\d+\.\d+'

def number_commas():
    return r'(\d+,)+?\d{3}' + pos_lookahead(regex_or('[^,]','$'))

def punct():
    return '%s+' % punct_chars()

def arbitrary_abbrev():
    BoundaryNotDot = regex_or(r'\s', '[“"?!,:;]', entity())
    aa1 = r'''([A-Za-z]\.){2,}''' + pos_lookahead(BoundaryNotDot)
    aa2 = r'''([A-Za-z]\.){1,}[A-Za-z]''' + pos_lookahead(BoundaryNotDot)
    return regex_or(aa1,aa2)

def separators():
    return regex_or('--+', '―')

def decorations():
    return r' [  ♫   ]+ '.replace(' ','')

def embedded_apostrophe():
    return r"\S+'\S+"

def normal_eyes():
    return r'[:=8]'

def wink():
    return r'[;]'

def nose_area():
    return r'(|o|O|-)' ## rather tight precision, \S might be reasonable... 

def happy_mouths():
    return r'[D\)\]]'

def tongue():
    return r'[pPb]'

def sad_mouths():
    return r'[\(\[]'

def other_mouths():
    return r'[\|doO/\\]'

def happy_emoticon():
    return '(\^_\^|' + normal_eyes() + nose_area() + happy_mouths() + ')'

def sad_emoticon():
    return 'T\.T|'+normal_eyes() + nose_area() + sad_mouths()

def wink_emoticon():
    return wink() + nose_area() + happy_mouths()

def tongue_emoticon():
    return normal_eyes() + nose_area() + tongue()

def other_emoticon():
    return normal_eyes() + nose_area() + other_mouths()

def faces():
    faces = (
        "(" +
        "("+normal_eyes()+"|"+wink()+")" +
        nose_area() +
        "("+tongue()+"|"+other_mouths()+"|"+sad_mouths()+"+|"+happy_mouths()+"+)" +
        "|" +
        "("+tongue()+"|"+other_mouths()+"|"+sad_mouths()+"+|"+happy_mouths()+"+)" +
        nose_area() +
        "("+normal_eyes()+"|"+wink()+")" +
        ")"
    )
    return faces

def hearts():
    return r'(<+/?3+)'

def arrows():
    return r'(<*[-=]*>+|<+[-=]*>*)'

def emoticon():
    return"("+hearts()+"|"+faces()+"|"+arrows()+")"

def not_edge_punct():
    return r"""[a-zA-Z0-9]"""

def egde_punct():
    return r"""[  ' " “ ” ‘ ’ * « » { } ( \) [ \]  ]""".replace(' ','')
def edge_punct_right():
    return r"""(%s)(%s+)(\s|$)""" % (not_edge_punct(), egde_punct())
def edge_punct_left():
    return r"""(\s|^)(%s+)(%s)""" % (egde_punct(), not_edge_punct())

