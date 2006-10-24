#!/usr/bin/env python
# -*- coding: utf8 -*-
import socket, re
from cgi import escape as escape_html
import eppdoc_client
import client_socket
from session_base import *
from translate import encoding, options

# Tags for scripted outputs:
d_tag = {
    'html': ('<pre class="fred_messages">','</pre>'),
    'php': ('<?php /*','*/ ?>'),
}
BEGIN,END = range(2)

class ManagerTransfer(ManagerBase):
    """EPP client support.
    This class take care about sending and receiving messages from/to server.
    Function process_answer() must be implemented by derived class.
    """
    def __init__(self):
        ManagerBase.__init__(self)
        self._epp_cmd = eppdoc_client.Message()
        self._epp_response = eppdoc_client.Message()
        self._available_commands = self._epp_cmd.get_client_commands()
        self._lorry = None
        # Typ očekávané odpovědi serveru. Zde si Manager pamatuje jaký příkaz
        # odeslal a podle toho pak zařadí návratové hodnoty.
        self._command_sent = '' # jméno posledního odeslaného příkazu
        self._raw_cmd = '' # XML EPP příkaz odeslaný serveru
        self._raw_answer = '' # XML EPP odpověd serveru
        self._dct_answer = {} # API response
        #... readline variables ...............
        self.readline = None
        self.readline_prefix = None
        self.readline_words = []
        #......................................
        self.reset_src()
        #test_init_client() # TEST ONLY

    def get_command_names(self):
        return self._available_commands

    def reset_src(self):
        'Reset buffers of sources.'
        self._raw_answer = '' # XML EPP odpověd serveru
        self._dict_answer = '' # dict - slovník vytvořený z XML EPP odpovědi
        self._dct_answer = {'code':0,'command':'',  'reason':'', 'errors':[], 'data':{}} # API response
        # Set output SORT BY and VEROBOSE names:
        if self._session[TRANSLATE_ANSWER_COLUMN_NAMES]:
            # Default is 1 (display column names). Zero is used for TEST (display column keys).
            self._session[SORT_BY_COLUMNS] = self._epp_cmd.get_sort_by_names(self._command_sent)

    def reset_round(self):
        'Prepare for next round. Reset internal dict with communication values.'
        self._errors = []
        self._notes = []
        self._notes_afrer_errors = []
        self._epp_cmd.reset()
        self._epp_response.reset()
        self._command_sent = '' # jméno posledního odeslaného příkazu
        self._session[SORT_BY_COLUMNS] = []

    def get_command_line(self):
        'Returns example of command built from parameters.'
        return self._epp_cmd.get_command_line(self._session[NULL_VALUE])

    #---------------------------------
    # funkce pro nastavení session
    #---------------------------------
    def __check_is_connected__(self):
        "Control if you are still connected."
        if self._lorry and not self._lorry.is_connected():
            # spojení spadlo
            if self._session[ONLINE]:
                self.append_note(_T('ERROR: Connection to %s interrupted.')%self._session[HOST])
            self.close()

    def grab_command_name_from_xml(self, message):
        "Save EPP command type for recognize server answer."
        # manager si zapamatuje jakého typu příkaz byl a podle toho 
        # pak pracuje s hodnotami, které mu server vrátí
        # Tady se typ musí vytáhnout přímo z XML, jiná možnost není. 
        # Protože lze posílat i XML již vytvořené dříve nebo z jiného programu.
        epp_xml = eppdoc_client.Message()
        epp_xml.parse_xml(message)
        err = epp_xml.fetch_errors()
        if len(err): self._errors.append(err)
        return epp_xml.get_epp_command_name()

    #==================================================
    #
    #    Transfer functions
    #    funkce pro komunikaci se socketem
    #
    #==================================================
    def get_connect_defaults(self):
        'Get connect defaults from config'
        if not self._conf: self.load_config() # load config, if was not been yet
        section = self.config_get_section_connect()
        data = [self.get_config_value(section,'host',OMIT_ERROR),
                self.get_config_value(section,'port',OMIT_ERROR,'int'),
                self.get_config_value(section,'ssl_key',OMIT_ERROR),
                self.get_config_value(section,'ssl_cert',OMIT_ERROR),
                self.get_config_value(section,'timeout',OMIT_ERROR),
                self.get_config_value(section,'socket',OMIT_ERROR),
                ]
        # command options
        self._session[HOST] = data[0] # for prompt info
        return data

    def connect(self, data=None):
        "Connect transfer socket. data=('host',port,'client-type')"
        if self.is_connected(): return 1 # spojení je již navázáno
        self._lorry = client_socket.Lorry()
        self._lorry._notes = self._notes
        self._lorry._errors = self._errors
        self._lorry.handler_message = self.process_answer
        if not data:
            data = self.get_connect_defaults()
            labels = ('host','port','SSL private key','SSL certificate','timeout')
            errors=[]
            for n in range(len(data[:5])):
                if data[n] is None:
                    errors.append(labels[n])
            if len(errors):
                self.append_error('%s: %s'%(_T('Can not create connection. Missing values'),', '.join(errors)))
                return 0
        if self._lorry.connect(data, self._session[VERBOSE]):
            epp_greeting = self._lorry.receive() # receive greeting
            self.__check_is_connected__()
            if epp_greeting:
                self.process_answer(epp_greeting)
                return 1
            else:
                self.append_error(_T("Server didn't return Greeting message. Contact server administrator."))
        return 0
        
    def close(self):
        "Close connection with server."
        if self._lorry:
            self._lorry.close()
            self._lorry = None
        # když se spojení zrušilo, tak o zalogování nemůže být ani řeči
        self._session[ONLINE] = 0
        self._session[USERNAME] = '' # for prompt info
        self._session[HOST] = '' # for prompt info

    def is_connected(self):
        "Check if the manager is connected."
        return self._lorry and self._lorry.is_connected()
        
    def send(self, message):
        "Send message to server."
        ret = 0
        self._raw_cmd = message
        if self._lorry:
            ret = self._lorry.send(message)
            if ret:
                # If XML doc has been sent, manager saves the name of this command.
                # This is essensial for resolve how type the server answer is.
                self._command_sent = self.grab_command_name_from_xml(message)
            self.__check_is_connected__()
        else:
            self.append_error(_T('You are not connected.'))
        return ret

    def send_logout(self, no_outoupt=None):
        'Send EPP logout message.'
        if not self._session[ONLINE]: return # session zalogována nebyla
        self.reset_round()
        self._epp_cmd.assemble_logout(self.__next_clTRID__())
        epp_doc = self._epp_cmd.get_xml()
        if epp_doc and self.is_connected():
            self.append_note(_T('Logout command sent to server'))
            self.send(epp_doc)          # odeslání dokumentu na server
            answer = self.receive()     # příjem odpovědi
            self.process_answer(answer) # zpracování odpovědi
            if not no_outoupt:
                self.display() # display errors or notes
                self.print_answer() # 2. departure from the rule to print answers
        else:
            self.append_error(self._epp_cmd.get_errors())

    def receive(self):
        "Receive message from server."
        ret = ''
        if self._lorry:
            ret = self._lorry.receive()
            self.__check_is_connected__()
        else:
            self.append_error(_T('You are not connected.'))
        return ret

    #==================================================
    #
    #    PARSE RESPONSE
    #    functions for parse and display response
    #
    #==================================================
        
    def process_answer(self, epp_server_answer):
        "This function MUST override derived class."
        self.append_error('Internal Error: Function process_answer() must be overriden!')

    def print_answer(self, dct=None):
        "Returns str of dict object."
        if not dct: dct = self._dct_answer
        if self._session[VERBOSE] and dct.get('command'):
            # Print in only any command was sent.
            fnc = getattr(self,'get_answer_%s'%self._session[OUTPUT_TYPE], self.get_answer)
            print fnc(dct)
            #try:
            #    print fnc(dct) #+++
            #except Exception, msg:
            #    print 'Exception ERROR:',msg

    def get_keys_sort_by_columns(self):
        'Returns list of keys what will be used to sorting output values.'
        return self.__get_column_items__(self._dct_answer['command'], self._dct_answer['data'])
        
    def __get_column_items__(self, command_name, dct_data):
        'Returns struct of key names for sorting output values lines.'
        if self._session[SORT_BY_COLUMNS]:
            sorted_columns = self._session[SORT_BY_COLUMNS] # sorted output (included in create command part)
        elif re.match('\w+:check',command_name):
            # exeption for all check commands
            keys = dct_data.keys()
            keys.sort()
            sorted_columns = map(lambda n:(n,1,''), keys) # sorted by keys
        else:
            sorted_columns = map(lambda n:(n,1,''), dct_data.keys()) # default (unsorted)
        return sorted_columns
                
    def get_answer_udata(self, sep='\n'):
        'Special for GUI output. Returns unicode.'
        body=[]
        report = body.append
        dct_data = self._dct_answer['data']
        for key,verbose,explain in self.__get_column_items__(self._dct_answer['command'], dct_data):
            value = dct_data.get(key,u'')
            if value not in ('',[]): __append_into_report__(body,key,value,explain,self._ljust,'',1) # '' - indent; 1 - no terminal tags
        return sep.join(body).decode(encoding)

    def __append_to_body__(self, body, dct):
        'Internal support for get_answer()'
        data_indent = ''
        data = []
        in_higher_verbose = 0
        used = []
        dct_data = dct['data']
        is_check = re.match('\w+:check',dct['command']) and 1 or 0 # object:check
        for key,verbose,explain in self.__get_column_items__(dct['command'], dct_data):
            if verbose > self._session[VERBOSE]:
                in_higher_verbose += 1
                used.append(key)
                continue
            value = dct_data.get(key,u'')
            if value not in ('',[]):
                if is_check:
                    # Tighten check response by code.
                    if type(value) is int: continue
                    key = re.sub(':reason','',key)
                __append_into_report__(data,key,value,explain,self._ljust,data_indent)
            used.append(key)
        if len(data):
            body.append('')
            body.extend(data)
        #--- INTERNAL USE ----
        # POZOR!!! V ostré verzi musí být deaktivováno!!!
        # ALERT!!! MUST be disabled in release version!!!
        if self._session[SORT_BY_COLUMNS]:
            # in mode SORT_BY_COLUMNS check if all names was used
            missing = [k for k in dct_data.keys() if k not in used and dct_data[k][0] >= self._session[VERBOSE]]
            if len(missing):
                body.append(colored_output.render('\n${BOLD}${RED}Here needs FIX code: %s${NORMAL}'%'(%s)'%', '.join(missing)))
        #---------------------

    def get_answer(self, dct=None, sep='\n'):
        'Show values parsed from the server answer.'
        body=[]
        report = body.append
        if not dct: dct = self._dct_answer
        #... code and reason .............................
        code = dct['code']
        if self._session[VERBOSE] < 2:
            # brief output mode
            # exception on the command login and hello:
            if dct['command'] in ('login','hello'):
                pass # omit reason block body.pop() # remove previous empty line
            else:
                match = re.match('\w+:(\w+)',dct['command'])
                key = match is None and dct['command'] or match.group(1)
                if code != 1000 or key in ('update','delete','transfer'):
                    if code >= 2000:
                        # move reason message into ERROR block messages and omit line with reason
                        dct['errors'].insert(0, dct['reason'])
                    else:
                        report('')
                        report(get_ltext(colored_output.render('${%s}%s${NORMAL}'%(code==1000 and 'GREEN' or 'NORMAL', dct['reason']))))
        else:
            # full
            report('')
            label_code = (u'%s:'%get_unicode(_T('Return code'))).ljust(self._ljust+1) # +1 space between key and value
            label_reason = (u'%s:'%get_unicode(_T('Reason'))).ljust(self._ljust+1)
            report(colored_output.render('${BOLD}%s${NORMAL}%d'%(get_ltext(label_code),code)))
            report(colored_output.render('${BOLD}%s${%s}%s${NORMAL}'%(get_ltext(label_reason), code==1000 and 'GREEN' or 'NORMAL', get_ltext(dct['reason']))))
            # We must keep message from verbose mode one where reason is shown as ERROR:
            if code >= 2000 and not len(dct['errors']): dct['errors'].insert(0, dct['reason'])
        #... errors .............................
        if len(dct['errors']):
            report(colored_output.render('${BOLD}${RED}'))
            label = u'%s:'%get_unicode(_T('ERROR'))
            report('%s%s'%(get_ltext(label.ljust(self._ljust+1)),get_ltext(dct['errors'][0])))
            for error in dct['errors'][1:]:
                report('%s%s'%(''.ljust(self._ljust+1),get_ltext(error)))
            report(colored_output.render('${NORMAL}'))
        #... data .............................
        if re.match('\w+:list',dct['command']):
            # list output execption
            body.append('') # empty line
            cnt=0
            for item in dct['data'].get('list',[]):
                body.append(get_ltext(item))
                cnt+=1
            body.append('') # empty line
            body.append(_TP('(%d item)','(%d items)',cnt)%cnt)
        else:
            self.__append_to_body__(body, dct)
        #... third verbose level .............................
        report('') # empty row
        for n in range(len(body)):
            if type(body[n]) == unicode: body[n] = body[n].encode(encoding)
        if self._session[VERBOSE] == 3:
            report(colored_output.render('${BOLD}COMMAND:${NORMAL}${GREEN}'))
            report(human_readable(self._raw_cmd))
            report(colored_output.render('${NORMAL}${BOLD}ANSWER:${NORMAL}${GREEN}'))
            report(human_readable(self._raw_answer))
            report(colored_output.render('${NORMAL}'))
            report('')
        return sep.join(body)

    def get_answer_html(self, dct=None):
        """Returns data in HTML format. Used syles:
        CSS:
        .fred_client       - main div of HTML output
        .fred_code         - div part of message (code + reason)
        .fred_errors       - ul li with errors
        .fred_data         - table with data
        .fred_source       - pre with XML sources
        .command_success    - reason with code 1000
        .command_done       - other readons
        .even               - every even row in data table
        """
        body=[]
        report = body.append
        if not dct: dct = self._dct_answer
        #... code and reason .............................
        code = dct['code']
        reason_css_class = code==1000 and 'command_success' or 'command_done'
        if self._session[VERBOSE] > 1 or code != 1000:
            # full
            tbl_reason=['<table class="fred_data">']
            tbl_reason.append('<tr>\n\t<th>%s</th>\n\t<td>%d</td>\n</tr>'%(_T('Return code'),code))
            #tbl_reason.append('<tr>\n\t<th>command</th>\n\t<td>%s</td>\n</tr>'%get_ltext(dct['command']))
            tbl_reason.append('<tr>\n\t<th>%s</th>\n\t<td><span class="%s">%s</span></td>\n</tr>'%(_T('Reason'), reason_css_class,get_ltext(dct['reason'])))
            tbl_reason.append('</table>')
            report('\n'.join(tbl_reason))
        #... errors .............................
        if len(dct['errors']):
            report('<div class="fred_errors">\n<strong>errors:</strong><ul>')
            for error in dct['errors']:
                report('<li>%s</li>'%get_ltext(error))
            report('</ul></div>')
        #... data .............................
        is_check = re.match('\w+:check',dct['command']) and 1 or 0 # object:check
        data_indent = ''
        data = []
        dct_data = dct['data']
        for key,verbose,explain in self.__get_column_items__(dct['command'], dct_data):
            if verbose > self._session[VERBOSE]: continue
            value = dct_data.get(key,u'')
            if value not in ('',[]):
                if is_check:
                    # Tighten check response by code.
                    if type(value) is int: continue
                    key = re.sub(':reason$','',key)
                __append_into_report__(data,key,value,explain,self._ljust,'',2) # 2 - use HTML pattern;
        if len(data):
            report('<table class="fred_data">')
            body.extend(data)
            report('</table>')
        for n in range(len(body)):
            if type(body[n]) == unicode: body[n] = body[n].encode(encoding)
        #... third verbose level .............................
        if self._session[VERBOSE] == 3:
            report('<pre class="fred_source">')
            report('<strong>COMMAND:</strong>')
            report(escape_html(human_readable(self._raw_cmd)))
            report('<strong>ANSWER:</strong>')
            report(escape_html(human_readable(self._raw_answer)))
            report('</pre>')
        # ..............
        return '\n'.join(body)

    def get_answer_php(self, dct=None):
        """Returns data as a PHP code:
        $code           int
        $command        string
        $reason         string
        $errors         array
        $labels         array
        $data           array
        $source_command string (third level)
        $source_answer  string (third level)
        """
        if not dct: dct = self._dct_answer
        body=[]
        report = body.append
        report('<?php')
        report("$encoding = %s;"%php_string(encoding))
        #... code and reason .............................
        code = dct['code']
        report('$code = %d;'%code)
        report("$command = %s;"%php_string(dct['command']))
        report("$reason = %s;"%php_string(dct['reason']))
        #... errors .............................
        errors = []
        for error in dct['errors']:
            errors.append(php_string(error))
        report('$errors = array(%s);'%', '.join(errors))
        #... data .............................
        report('$labels = array();')
        report('$data = array();')
        dct_data = dct['data']
        for key,verbose,explain in self.__get_column_items__(dct['command'], dct_data):
            if verbose > self._session[VERBOSE]: continue
            if not explain: explain = key
            value = dct_data.get(key,u'')
            if value not in ('',[]):
                if type(value) in (list,tuple):
                    report('$labels[%s] = %s;'%(php_string(key),php_string(explain)))
                    report('$data[%s] = array();'%php_string(key))
                    php_key = php_string(key)
                    for v in value:
                        report('$data[%s][] = %s;'%(php_key,php_string(v)))
                else:
                    report('$labels[%s] = %s;'%(php_string(key),php_string(explain)))
                    report('$data[%s] = %s;'%(php_string(key),php_string(value)))
        #... third verbose level .............................
        if self._session[VERBOSE] == 3:
            report('$source_command = %s;'%php_string(human_readable(self._raw_cmd)))
            report('$source_answer = %s;'%php_string(human_readable(self._raw_answer)))
        # ..............
        report('?>')
        return  '\n'.join(body)

    def print_tag(self, pos):
        'Prints tag for HTML or PHP mode at the position (0-beginig,1-end)'
        tag = d_tag.get(self._options['output'],('',''))[pos]
        if tag: print tag
        
    def save_history(self):
        'Save history of command line.'
        eppdoc_client.eppdoc_assemble.save_history()

    def restore_history(self):
        'Restore history of command line.'
        eppdoc_client.eppdoc_assemble.restore_history()

    def remove_from_history(self, count=1):
        'Remove count last commands from history.'
        eppdoc_client.eppdoc_assemble.remove_from_history(count)

    #-------------------------------------
    # readline part
    #-------------------------------------
    def init_radline(self, readline):
        'Init modul readline'
        if readline:
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.complete)
            self.readline = readline

    def __get_readline_words__(self, buffer):
        'Find set of words to choose in the prompt help'
        #writelog("BUFFER=%s"%buffer)
        m = re.match('\w+',buffer)
        if m:
            command_name = m.group(0)
        else:
            command_name = None
        if command_name is not None and command_name in self._available_commands:
            #writelog("\tCOMMAND IS %s"%command_name)
            dct, errors = self._epp_cmd.readline_parse_prompt(command_name, buffer)
            #writelog("DICT %s\nERRORS: %s"%(dct,errors))
            words = self._epp_cmd.readline_find_words(command_name, dct, writelog is None and (lambda s: s) or writelog)
        else:
            words = self._available_commands # default offer
        writelog('\tOFFER WORDS = %s'%str(words))
        return words

    def complete1(self, prefix, index):
        'Function for readline.complete manages reaction on the TAB key press.'
        if index == 0:
            self.readline_words = [w for w in self.__get_readline_words__(self.readline.get_line_buffer()) if w.startswith(prefix)]
            #try: # FOR TEST ONLY
            #    self.readline_words = []
            #    words = self.__get_readline_words__(self.readline.get_line_buffer())
            #    self.readline_words = [w for w in words if w.startswith(prefix)]
            #except Exception, msg:
            #    writelog('*** EXCEPTION ***: %s'%str(msg))
        try:
            word = self.readline_words[index]+' '
        except IndexError:
            word = None
        #writelog("complete(%s, %d) WORD='%s';"%(prefix,index,word))
        #writelog('word = %s'%str(self.readline_words))
        return word

    def complete(self, prefix, index):
        'Function for readline.complete manages reaction on the TAB key press.'
        if prefix != self.readline_prefix:
            self.readline_prefix = prefix
            command = self.readline.get_line_buffer().strip()
            if command in self._available_commands:
                if prefix == command:
                    self.matching_words = [command] # space at the end missing
                else:
                    self.matching_words = [] # command is already typed
            else:
                # find all words that start with this prefix
                if not len(self.readline_words):
                    self.readline_words = [i for i in self._available_session_commands if i!='!'] + self._available_commands
                self.matching_words = [w for w in self.readline_words if w.startswith(prefix)]
        try:
            word = self.matching_words[index]+' '
        except IndexError:
            word = None
        #writelog("complete(%s, %d) WORD='%s'"%(prefix,index,word))
        return word
    #-------------------------------------

        
def __append_into_report__(body,k,v,explain,ljust, indent = '', no_terminal_tags=0):
    'Append value type(unicode|list|tuple) into report body.'
    patt = (
        ('%s${BOLD}%s${NORMAL} %s','%s${BOLD}%s${NORMAL}','%s%s'),
        ('%s%s %s','%s%s','%s%s'),
        ('%s<tr>\n\t<th>%s</th>\n\t<td>%s</td>\n</tr>','%s<tr>\n\t<th>%s</th>\n\t<td>&nbsp;</td>\n</tr>','%s<tr>\n\t<th>&nbsp;</th>\n\t<td>%s</td>\n</tr>'),
    )[no_terminal_tags]
    escape = no_terminal_tags == 2 and escape_html or (lambda s: s)
    if explain: k = explain # overwrite key by explain message
    if type(k) is str: k = k.decode(encoding)
    if type(v) is str: v = v.decode(encoding)
    if no_terminal_tags == 2:
        # html
        key = k
        ljustify = ''
    else:
        # text
        key = (k+':').ljust(ljust)
        ljustify = ''.ljust(ljust+len(indent)+1)
    if type(v) in (list,tuple):
        if len(v):
            body.append(get_ltext(colored_output.render(patt[0]%(indent,key,escape(str_lists(v[0]))))))
            for text in v[1:]:
                body.append(get_ltext(patt[2]%(ljustify,escape(str_lists(text)))))
        else:
            body.append(get_ltext(colored_output.render(patt[1]%(indent,key))))
    else:
        body.append(get_ltext(colored_output.render(patt[0]%(indent,key, v))))

def str_lists(text):
    """Prepare list or tuples for display. Same as str() but omit u'...' symbols
    and put all values into brackets.
    """
    tmp = text
    if type(text) in (list,tuple):
        body = []
        for item in text:
            if item == '': continue
            str_item = str_lists(item)
            if str_item:
                if type(item) in (list,tuple):
                    str_item = '(%s)'%str_item
                body.append(str_item)
        if len(body):
            if len(body) > 1:
                text = ', '.join(body)
            else:
                text = body[0]
        else:
            text = ''
    return text

def human_readable(body):
    'Resample to rows if they missing. This is hook while PrettyPrint missing.'
    if not re.search('</\w+>\n<',body):
        body = re.sub('(</[^>]+>)','\\1\n',body)
    return body

def php_string(value):
    'Returns escaped string for place into PHP variable.'
    if type(value) in (str,unicode):
        ret = "'%s'"%re.sub("([^\\\])'","\\1\\'",get_ltext(value))
    else:
        ret = value # int or float
    return ret

#--------------------
# For test only
#--------------------
def writelog(msg):
    'for test only, debug readline'
    if debug_sock: debug_sock.send('%s\n'%msg)
def test_init_client():
    'for test only, debug readline'
    global debug_sock
    debug_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        debug_sock.connect((DEBUG_HOST, DEBUG_PORT))
    except socket.error, msg:
        debug_sock = None
def run_test_server():
    'for test only, debug readline'
    print "RUN TEST SERVER (for debug readline) AT PORT",DEBUG_PORT
    DEBUG_HOST = '' # Symbolic name meaning the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((DEBUG_HOST, DEBUG_PORT))
    s.listen(1)
    conn=None
    try:
        conn, addr = s.accept()
        print 'Connected by', addr
        while 1:
            data = conn.recv(1024)
            if not data: break
            print data
    except (KeyboardInterrupt, EOFError):
        pass
    if conn: conn.close()

DEBUG_HOST = 'localhost'
DEBUG_PORT = 50007
debug_sock = None
#--------------------
# TEST ONLY (enable this and test_init_client())
#--------------------
#if __name__ == '__main__':
#    if len(sys.argv) > 1 and sys.argv[1]=='server':
#        run_test_server()
