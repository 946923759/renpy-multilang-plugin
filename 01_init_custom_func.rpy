#Add 'characters' layer to the game
define config.layers = ['master','characters','transient','screens','overlay']
#Required for color manipulation on images.
define config.gl2  = True


python early:
    def intTryParse(value, errorVal=-1):
        try:
            return int(value)
        except:
            return errorVal

    def tlc(firstChoice,remaining):
        choices = [firstChoice]+list(remaining)
        #print(choices)
        pref = intTryParse(gui.preference("custom_lang"),0)
        if len(choices) > pref:
            return choices[pref]
        else:
            return choices[0]

    NAMES = {
        "Girl": "少女",
    }
    def tl_name(n):
        
        lang = intTryParse(gui.preference("custom_lang"),0)
        if lang!=2: #If not Japanese
            return n
        elif n in NAMES:
            return NAMES[n]
        else:
            #print("No translation found for "+n)
            return n #No translation needed

python early hide:
    import re

    ###
    # HIGHLIGHT COMMAND
    ###

    #parser function decides how to parse the command and what to return.
    #The given argument is always the lexer.
    def parse_highlight(o):
        #Returns list of strings of displayed tags, includes bg
        return renpy.get_showing_tags('characters')

    #the returned object (or objects) from the parser func is given as an argument here
    def exec_highlight(portraits):
        for p in portraits:
            print(p)

    #Checks if the command is written correctly and determines
    #if an error should be thrown in the renpy console
    def lint_highlight(o):
        try:
            int(o)
        except:
            renpy.error("Not a number!")

    ###
    # LINE COMMAND
    ###

    def parse_smartline(lex):
        who = lex.simple_expression()
        what = lex.rest()
        return (who, what)

    def execute_smartline(o):
        who, what = o
        renpy.say(eval(who), what)

    def lint_smartline(o):
        who, what = o
        try:
            eval(who)
        except:
            renpy.error("Character not defined: %s" % who)

        tte = renpy.check_text_tags(what)
        if tte:
            renpy.error(tte)

    ###
    # MULTILANG HACK
    ###

    def parse_multilang(lexer):
        #return lexer.match(r"(?=[\"'])(?:\"[^\"\\]*(?:\\[\s\S][^\"\\]*)*\")")
        #print (lexer.rest())
        #return 'a'
        #s =  + lexer.rest()

        # "What the fuck?" -That one famous quake guy
        return (
            lexer.simple_expression(),
            re.findall(r"(?=[\"'])(?:\"[^\"\\]*(?:\\[\s\S][^\"\\]*)*\")",lexer.rest())
        )
    
    def execute_multilang(o):
        who, txt = o
        pref = intTryParse(gui.preference("custom_lang"),0)
        #print("Lang is "+str(pref))
        
        if len(txt) >= pref:
            renpy.say(eval(who), txt[pref][1:-1])
            
            # This doesn't work because name colors will be removed
            # advChar = eval(who)
            # if type(advChar) == str:
            #     name = tl_name(advChar,pref)
            # elif advChar:
            #     name = tl_name(advChar.name,pref)
            # else:
            #     name = None
            # renpy.say(name, txt[pref][1:-1])
        else:
            if len(txt[0][1:-1])>0:
                renpy.say(eval(who),txt[0][1:-1])
        #print(o)
    
    def lint_multilang(o):
        pass

    # def parse_multilang_nospeaker(lexer):
    #     s = lexer.rest()
    #     print(s)
    #     #return lexer.match(r"(?=[\"'])(?:\"[^\"\\]*(?:\\[\s\S][^\"\\]*)*\")")
    #     #print (lexer.rest())
    #     #return 'a'
    #     #s =  + lexer.rest()

    #     # "What the fuck?" -That one famous quake guy
    #     return (
    #         lexer.simple_expression(),
    #         re.findall(r"(?=[\"'])(?:\"[^\"\\]*(?:\\[\s\S][^\"\\]*)*\")",lexer.rest())
    #     )
    
    # def execute_multilang_nospeaker(o):
    #     who, txt = o
    #     pref = intTryParse(gui.preference("custom_lang"),0)
    #     print("Lang is "+str(pref))
    #     if len(txt) >= pref:
    #         renpy.say(eval(who), txt[pref][1:-1])
    #     else:
    #         if len(txt[0][1:-1])>0:
    #             renpy.say(eval(who),txt[0][1:-1])
    #     #print(o)
    
    # def lint_multilang(o):
    #     pass


    renpy.register_statement("hl",parse=parse_highlight,execute=exec_highlight,lint=lint_highlight)
    renpy.register_statement("line", parse=parse_smartline, execute=execute_smartline, lint=lint_smartline)
    renpy.register_statement("tl", parse=parse_multilang, execute=execute_multilang, lint=lint_multilang)
    print("Loaded!")


init 0:

    transform dim:
        linear .5 matrixcolor BrightnessMatrix(-.2)
    transform nodim:
        linear .5 matrixcolor BrightnessMatrix(0)
    #transform slideright:
    
    define gui.custom_lang = gui.preference("custom_lang",0)
    
# Copyleft 2023 Amaryllis
# 
# This program is free software: you can redistribute it and/or modify it under the 
# terms of the GNU Lesser General Public License as published by the Free Software 
# Foundation, either version 2 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for 
# more details.
# 
# You should have received a copy of the GNU Lesser General Public License along with 
# this program. If not, see <https://www.gnu.org/licenses/>. 
