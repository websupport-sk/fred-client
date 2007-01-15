#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#This file is part of FredClient.
#
#    FredClient is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    FredClient is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with FredClient; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
import re
import eppdoc_assemble
from translate import options, encoding
"""
This module described all EPP commands with their parameters and 
names of the returned values. Class Message is the top of the Message
classes in modules eppdoc_. This instance is used by client session Manager
object for manage with EPP commands and answers.
"""

UNBOUNDED = eppdoc_assemble.UNBOUNDED

# Help
def get_shared_notice():
    'Returns notice for EPP commands'
    return {   
   'disclose':_T('Names what are not included into disclose list are set to opposite value of the disclose flag value.'),
   'ident':_T("""Identificator type can be: 
      op       number identity card
      rc       number of birth
      passport number of passport
      mpsv     number of Ministry of Labour and social affairs
      ico      number of company"""),
}

def make_command_parameters():
    'Returns command parameters tuple'
    notice = get_shared_notice()
    # format:
    # command-name: (param-name, (min,max), (list of required), 'help', 'example', 'pattern', (list of children)
    # For include new command you need do this steps:
    #   1. add new item into command_params
    #   2. add function assemble_...() into eppdoc_assemble.Message
    #   3. [optional] add answer_response_...() in session_receiver.ManagerReceiver
    command_params = {
        'hello': (0, [], _T("""
Command 'hello' is used to obtain information from the server.
The server answer to 'hello' command is Greeting message. This message
is used usualy at the begining of the session for getting some variables
usefull for communication. Within Server version or ID you can got
available languages, Data Collection policy etc.
Command 'hello' you can call at any time."""),()),
        'logout': (0, [], _T("""
The EPP "logout" command is used to end a session with the server.
But client will be still running. For close client type 'quit' (see help).
Before quit the client send logout automaticly."""),()),
        #----------------------------------------------------
        'login': (2,[
            ('username',(1,1),(),_T('Username'),'username','',()),
            ('password',(1,1),(),_T('Password'),'password','',()),
            ('new_password',(0,1),(),_T('New password'),'new_password','',()),
            ('lang',(0,1),(),_T('Language version'),'en','',()),
        ],_T("""
The "login" command establishes an ongoing server session that preserves client identity
and authorization information during the duration of the session. Parametr "lang" set
session and client language together. Language is possible to set also by option on the
command line, or define it in configuration file or set by client command 'lang'.
Using parameter 'new_password' you can change password.
"""),('login john mypass "my new pass!"','login john mypass NULL cs')),
        #----------------------------------------------------
        'info_contact': (1,[
            ('name',(1,1),(),_T('Contact ID'),'CID:ID01','',()),
        ],_T("""
The EPP "info" command is used to retrieve information associated
with an existing object. The elements needed to identify an object
and the type of information associated with an object are both
object-specific, so the child elements of the <info> command are
specified using the EPP extension framework."""),('info_contact cid:contact',)),
        'info_domain': (1,[
            ('name',(1,1),(),_T('Domain name'),'mydomain.cz','',()),
        ],_T("""
The EPP "info" command is used to retrieve information associated
with an existing object. The elements needed to identify an object
and the type of information associated with an object are both
object-specific, so the child elements of the <info> command are
specified using the EPP extension framework."""),('info_domain my-domain.cz',)),
        'info_nsset': (1,[
            ('name',(1,1),(),_T('NSSET ID'),'NSSET_ID','',()),
        ],_T("""
The EPP "info" command is used to retrieve information associated
with an existing object. The elements needed to identify an object
and the type of information associated with an object are both
object-specific, so the child elements of the <info> command are
specified using the EPP extension framework."""),('info_nsset nssid:nsid',)),
        #----------------------------------------------------
        'check_contact': (1,[
            ('name',(1,UNBOUNDED),(),_T('Contact ID'),'CID:ID01','',()),
        ],_T("""
The EPP "check" command is used to determine if an object can be
provisioned within a repository.  It provides a hint that allows a
client to anticipate the success or failure of provisioning an object
using the "create" command as object provisioning requirements are
ultimately a matter of server policy."""),('check_contact cid:contact1 cid:contact2',)),
        'check_domain': (1,[
            ('name',(1,UNBOUNDED),(),_T('Domain name'),'mydomain.cz','',()),
        ],_T("""
The EPP "check" command is used to determine if an object can be
provisioned within a repository.  It provides a hint that allows a
client to anticipate the success or failure of provisioning an object
using the "create" command as object provisioning requirements are
ultimately a matter of server policy."""),('check_domain domain1.cz domain2.cz',)),
        'check_nsset': (1,[
            ('name',(1,UNBOUNDED),(),_T('NSSET ID'),'NSSET_ID','',()),
        ],_T("""
The EPP "check" command is used to determine if an object can be
provisioned within a repository.  It provides a hint that allows a
client to anticipate the success or failure of provisioning an object
using the "create" command as object provisioning requirements are
ultimately a matter of server policy."""),('check_nsset nssid:id1 nssid:id2',)),
        #----------------------------------------------------
        'poll': (1,[
            ('op',(1,1),(('req',),('ack',)),_T('Query type'),'','',()),
            ('msg_id',(1,1),(),_T("Index of message (required only with op = 'ack')"),'123','',()),
        ],_T("""
Poll command is used to discover and retrieve service messages. They are saved
in the message queue. When you send poll with parameter op = req, 
you get only the last message from the queue. But this message
still remains on the queue. For remove message from the queue set
poll op = ack and ID of this message. So you needs to send two poll
commands for manage one message: 1. reading, 2. removing.
See help poll_autoack for client function that sends this commands together.
"""),('poll req','poll ack 4',)),
        #----------------------------------------------------
        'transfer_contact': (2,[
            ('name',(1,1),(),_T('Contact ID'),'CID:ID01','',()),
            ('auth_info',(1,1),(),_T('Password required by server to authorize the transfer'),'mypassword','',()),
        ],_T("""
The EPP "transfer" command makes change in client sponsorship 
of a designated registrar. New password for authorisation 
will be generated automaticly after succefull transfer."""),('transfer_contact CID:ID01 password',)),
        #----------------------------------------------------
        'transfer_nsset': (2,[
            ('name',(1,1),(),_T('NSSET ID'),'NSSET_ID','',()),
            #('op',(1,1),transfer_op,_T('query type'),()),
            ('auth_info',(1,1),(),_T('Password required by server to authorize the transfer'),'mypassword','',()),
        ],_T("""
The EPP "transfer" command makes change in client sponsorship 
of a designated registrar. New password for authorisation 
will be generated automaticly after succefull transfer."""),('transfer_nsset nssid:nsset password',)),
        #----------------------------------------------------
        'transfer_domain': (2,[
            ('name',(1,1),(),_T('Domain name of domain to change sponsorship'),'domain.cz','',()),
            #('op',(1,1),transfer_op,_T('query type'),()),
            ('auth_info',(1,1),(),_T('Password required by server to authorize the transfer'),'mypassword','',()),
        ],_T("""
The EPP "transfer" command makes change in client sponsorship 
of a designated registrar. New password for authorisation 
will be generated automaticly after succefull transfer."""),('transfer_domain domain.cz password',)),
        #----------------------------------------------------
        'create_contact': (5,[
            ('contact_id',(1,1),(),_T('Contact ID'),'CID:ID01','',()),
            ('name',(1,1),(),_T('Name'), 'John Nowak','',()), # odtud shoda s update contact
            ('email',(1,1),(),_T('Email'),'info@mymail.cz','',()),
            ('city',(1,1),(),_T('City'),'Praha','',()),
            ('cc',(1,1),(),_T('Country code'),'CZ',_T('country code'),()),
            ('auth_info',(0,1),(),_T('Password required by server to authorize the transfer'),'mypassword',_T('password'),()), # authorization information for transfer
            ('org',(0,1),(),_T('Organisation'),'Firma s.r.o.','',()),
            ('street',(0,3),(),_T('Street'), 'Downing street 1230/12','',()),
            ('sp',(0,1),(),_T('State or province'),'Outlands','',()),
            ('pc',(0,1),(),_T('Postal code'),'12000',_T('postal code'),()),
            ('voice',(0,1),(),_T('Phone'),'+420.222745111','',()),
            ('fax',(0,1),(),_T('Fax'),'+420.222745111','',()),
            ('disclose',(0,1),(),_T('Disclose'),'','',(
                ('flag',(1,1),(('y',),('n',)),_T('Disclose flag (default y)'),'n','',()),
                ('data',(0,len(eppdoc_assemble.contact_disclose)),eppdoc_assemble.contact_disclose,_T('Data for with is set the flag value'),'','',()),
            )),
            ('vat',(0,1),(),_T('VAT (Value-added tax)'),'7035555556','',()), # daˇnový identifikátor
            ('ident',(0,1),(),_T('Identificator'),'','',( # mpsv: identifikátor Ministerstva práce a sociálních věcí
                ('type',(1,1),map(lambda n:(n,),('op','rc','passport','mpsv','ico')),_T('Identificator type'),'op','',()),
                ('number',(1,1),(),_T('Identificator number'),'8888888856','',()),
            )),
            ('notify_email',(0,1),(),_T('Notification email'),'info@mymail.cz','',()),
            ],'%s\n\n%s\n\n%s'%(_T("""
The EPP "create_contact" command is used to create an instance of the contact.
The contact can be created for an indefinite period of time, or
it can be created for a specific validity period."""),notice['disclose'],notice['ident']),(
            "create_contact CID:ID01 'Jan Novak' info@mymail.cz Praha CZ mypassword 'Firma s.r.o.' 'Narodni trida 1230/12' '' 12000 +420.222745111 +420.222745111 (y (org fax email)) 7035555556 (op 8888888856) info@mymail.cz",
            "create_contact CID:ID02 'Jan Ban' info@mail.com Brno CZ"
            )),
        #----------------------------------------------------
        'create_domain': (2,[
            ('name',(1,1),(),_T('Domain name'),'mydomain.cz','',()),
            ('registrant',(1,1),(),_T('Registrant ID'),'CID:REGID','',()),
            ('auth_info',(0,1),(),_T('Password required by server to authorize the transfer'),'mypassword','',()),
            ('nsset',(0,1),(),_T('NSSET ID'),'NSSID:ID','',()),
            ('period',(0,1),(),_T('Period'),'','',(
                ('num',(1,1),(),_T('Number of months or years'),'3','',()),
                ('unit',(1,1),(('y',),('m',)),_T('Period unit (y year(default), m month)'),'','',()),
            )),
            ('admin',(0,UNBOUNDED),(),_T('Administrative contact ID'),'CID:ADMIN_ID','',()),
            ('val_ex_date',(0,1),(),_T('Validation expires at'),'2008-12-03','',()),
            ],_T("""
The EPP "create" command is used to create an instance of an object.
An object can be created for an indefinite period of time, or an
object can be created for a specific validity period."""),(
                'create_domain domain.cz cid:regid password nssid:nsid (3 y) (cid:admin1,cid:admin2)',
                'create_domain 1.1.1.7.4.5.2.2.2.0.2.4.e164.arpa cid:regid password nssid:nsid (3 y) (cid:admin1,cid:admin2) 2006-06-08'
            )),
        #----------------------------------------------------
        'create_nsset': (3,[
            ('id',(1,1),(),_T('NSSET ID'),'NSSID:ID','',()),
            ('dns',(2,9),(),_T('LIST of DNS'),'','',(
                ('name',(1,1),(),_T('Name server'),'my.dns1.cz','',()),
                ('addr',(0,UNBOUNDED),(),_T('Server address'),'217.31.207.130','',()),
            )),
            ('tech',(1,UNBOUNDED),(),_T('Technical contact'),'CID:ID01','',()),
            ('auth_info',(0,1),(),_T('Password required by server to authorize the transfer'),'mypassword','',()),
            ('reportlevel',(0,1),(),_T('Report level. Range 0 - 10'),'1','',()),
            ],_T("""
The EPP "create" command is used to create an instance of an object.
An object can be created for an indefinite period of time, or an
object can be created for a specific validity period."""),(
                'create_nsset nssid:nsset1 ((ns1.domain.cz (217.31.207.130 217.31.207.129)),(ns2.domain.cz (217.31.206.130 217.31.206.129)),(ns3.domain.cz (217.31.205.130 217.31.205.129))) cid:regid passw',
            )),
        #----------------------------------------------------
        'delete_contact': (1,[
             ('id',(1,1),(),_T('Contact ID'),'CID:ID01','',()),
            ],_T("""The EPP "delete" command is used to remove an instance of an existing object."""),('delete_contact cid:id',)),
        #----------------------------------------------------
        'delete_domain': (1,[
            ('name',(1,1),(),_T('Domain name'),'mydomain.cz','',()),
            ],_T("""The EPP "delete" command is used to remove an instance of an existing object."""),('delete_domain domain.cz',)),
        #----------------------------------------------------
        'delete_nsset': (1,[
            ('id',(1,1),(),_T('NSSET ID'),'NSSET_ID','',()),
            ],_T("""The EPP "delete" command is used to remove an instance of an existing object."""),('delete_nsset nssid:id',)),
        #----------------------------------------------------
        'renew_domain': (2,[
            ('name',(1,1),(),_T('Domain name'),'mydomain.cz','',()),
            ('cur_exp_date',(1,1),(),_T('Expiration date'),'2006-12-03','',()),
            ('period',(0,1),(),_T('Period'),'','',(
                ('num',(1,1),(),_T('Number of months or years'),'3','',()),
                ('unit',(1,1),(('y',),('m',)),_T('Period unit (y year(default), m month)'),'','',()),
            )),
            ('val_ex_date',(0,1),(),_T('Validation expires at'),'2008-12-03','',()),
            ],_T("""
A domain name object MAY have a specified validity period. If server
policy supports domain object validity periods, the validity period
is defined when a domain object is created, and it MAY be extended by
the EPP 'renew' command.

Validity periods are measured in years or months with the appropriate
units specified using the 'unit' attribute.  Valid values for the
'unit' attribute are 'y' for years and 'm' for months.  The minimum
and maximum allowable period is defined in the Communication rules."""),('renew_domain nic.cz 2008-06-02 (6 y)',)), # The EPP renew_domain command is used to extend validity of an existing domain.
        #----------------------------------------------------
        'update_contact': (1,[
            ('contact_id',(1,1),(),_T('Contact ID'),'CID:ID01','',()),
            ('chg',(0,1),(),_T('Change values'),'','',(
                ('postal_info',(0,1),(),_T('Postal informations'),'','',(
                    ('name',(0,1),(),_T('Name'),u'Jan Novák','',()),
                    ('org',(0,1),(),_T('Organisation'),'Firma s.r.o.','',()),
                    ('addr',(0,1),(),_T('Address'),'','',(
                        ('city',(1,1),(),_T('City'),'Praha','',()),
                        ('cc',(1,1),(),_T('Country code'),'CZ','',()),
                        ('street',(0,3),(),_T('Street'),u'Na národní 1234/14','',()),
                        ('sp',(0,1),(),_T('State or province'),'','',()),
                        ('pc',(0,1),(),_T('Postal code'),'12000','',()),
                    )),
                )),
                ('voice',(0,1),(),_T('Phone'),'+420.222745111','',()),
                ('fax',(0,1),(),_T('Fax'),'+420.222745111','',()),
                ('email',(0,1),(),_T('Email'),'info@mymail.cz','',()),
                ('auth_info',(0,1),(),_T('Password required by server to authorize the transfer'),'mypassword','',()),
                ('disclose',(0,1),(),_T('Disclose'),'','',(
                    ('flag',(1,1),(('y',),('n',)),_T('Disclose flag (default y)'),'','',()),
                    ('data',(0,len(eppdoc_assemble.contact_disclose)),eppdoc_assemble.contact_disclose,_T('data for with is set the flag value'),'','',()),
                )),
                ('vat',(0,1),(),_T('VAT'),'7035555556','',()),
                ('ident',(0,1),(),_T('Identificator'),'','',(
                    ('type',(1,1),map(lambda n:(n,),('op','rc','passport','mpsv','ico')),_T('Identificator type'),'op','',()),
                    ('number',(1,1),(),_T('Identificator number'),'8888888856','',()),
                )),
                ('notify_email',(0,1),(),_T('Notification email'),'notify@mymail.cz','',()),
            )),
            ],_T("""The EPP "update" command is used to update an instance of an existing object."""),(
                    "update_contact CID:ID01 (('Jan Nowak' 'Firma s.r.o.' (Praha CZ ('Na narodni 1230/12', 'Americka 12') Vinohrady 12000)) +420.222745111 +420.222745111 info@mymail.cz mypassword (y (org, voice, email)) 7035555556 (ico 8888888856) notify@mymail.cz)",
                    "update_contact cid:id01 (('Jan Novák' 'Firma s.r.o.' (Praha CZ ('Na národní 1230/12', 'Americká 12') Vinohrady 12000)) +420.222745111 +420.222745111 info@mymail.cz password (y (org, voice, email)) 7035555556 (ico 8888888856) notify@mymail.cz)",
                    "update_contact CID:ID01 (() NULL NULL NULL NULL () NULL () change.only@notify-mail.cz)",
            )),
        #----------------------------------------------------
        'update_domain': (1,[
            ('name',(1,1),(),_T('Domain name'),'mydomain.cz','',()),
            ('add_admin',(0,UNBOUNDED),(),_T('Administrative contact ID'),'CID:ID01','',()),
            ('rem_admin',(0,UNBOUNDED),(),_T('Administrative contact ID'),'CID:ID01','',()),
            ('chg',(0,1),(),_T('Change values'),'','',(
                ('nsset',(0,1),(),_T('NSSET ID'),'NSSET_ID','',()),
                ('registrant',(0,1),(),_T('Registrant ID'),'CID:ID01','',()),
                ('auth_info',(0,1),(),_T('Password required by server to authorize the transfer'),'mypassword','',()),
            )),
            ('val_ex_date',(0,1),(),_T('Validation expires at'),'2008-12-03','',()),
            ],_T("""The EPP "update" command is used to update an instance of an existing object."""),(
                'update_domain mydomain.cz (CID:ID01, CID:ID02) CID:ID03 (NSSID:NSSET01 CID:ID04 mypass)',
                'update_domain 1.1.1.7.4.5.2.2.2.0.2.4.e164.arpa (CID:ID01, CID:ID02) CID:ID03 (NSSID:NSSET01 CID:ID04 mypass) 2008-12-03',
            )),
        #----------------------------------------------------
        'update_nsset': (1,[
            ('id',(1,1),(),_T('NSSET ID'),'NSSET_ID','',()),
            ('add',(0,1),(),_T('Add values'),'','',(
                ('dns',(0,9),(),_T('List of DNS'),'','',(
                    ('name',(1,1),(),_T('Name server'),'my.dns.cz','',()),
                    ('addr',(0,UNBOUNDED),(),_T('Server address'),'217.31.207.130','',()),
                )),
                ('tech',(0,UNBOUNDED),(),_T('Technical contact ID'),'CID:ID01','',()),
            )),
            ('rem',(0,1),(),_T('Remove values'),'','',(
                ('name',(0,9),(),_T('Name server'),'my.dns.cz','',()),
                ('tech',(0,UNBOUNDED),(),_T('Technical contact ID'),'CID:ID01','',()),
            )),
            ('auth_info',(0,1),(),_T('Password required by server to authorize the transfer'),'new_password','',()),
            ('reportlevel',(0,1),(),_T('Report level. Range 0 - 10'),'1','',()),
            ],_T("""The EPP "update" command is used to update an instance of an existing object."""),(
                "update_nsset nssid:ns1 (((ns1.dns.cz (217.31.207.130, 217.31.207.131, 217.31.207.132)), (ns2.dns.cz (217.31.207.130, 217.31.207.131, 217.31.207.132))) (cid:tech1, cid:tech2, cid:tech3)) (((rem1.dns.cz, rem2.dns.cz) (cid:tech_rem01, cid:tech_rem02))) password",
            )),
        #----------------------------------------------------
        'list_contact': (0,[],_T("""The EPP "list" command is used to list all ID of an existing contact owning by registrant."""),()),
        'list_nsset': (0,[],_T("""The EPP "list" command is used to list all ID of an existing NSSET owning by registrant."""),()),
        'list_domain': (0,[],_T("""The EPP "list" command is used to list all domain names owning by registrant."""),()),
        #----------------------------------------------------
        'sendauthinfo_contact': (1,[
             ('id',(1,1),(),_T('Contact ID'),'CID:ID01','',()),
            ],_T("""The EPP 'sendauthinfo_contact' command transmit request for send authorisation info to contact email."""),('sendauthinfo_contact cid:id',)),
        #----------------------------------------------------
        'sendauthinfo_domain': (1,[
            ('name',(1,1),(),_T('Domain name'),'mydomain.cz','',()),
            ],_T("""The EPP 'sendauthinfo_domain' command transmit request for send password to registrant email."""),('sendauthinfo_domain domain.cz',)),
        #----------------------------------------------------
        'sendauthinfo_nsset': (1,[
            ('id',(1,1),(),_T('NSSET ID'),'NSSID:MYID','',()),
            ],_T("""The EPP 'sendauthinfo_nsset' command transmit request for send authorisation info to technical contact email."""),('sendauthinfo_nsset nssid:id',)),
        #----------------------------------------------------
        'credit_info': (0,[],_T("""The EPP 'credit_info' command returns credit information."""),('credit_info',)),
        #----------------------------------------------------
        'technical_test': (2,[
            ('id',(1,1),(),_T('NSSET ID'),'NSSID:MYID','',()),
            ('name',(1,1),(),_T('Domain name'),'mydomain.cz','',()),
            ],_T("""
The EPP 'technical_test' command transmit request for technical test for particular NSSET and domain.
The result of the test will be saved into the message queue from where the registrant can fetch it by poll command.
"""),('technical_test nssid:id mydomain.cz',)),
        #----------------------------------------------------
    }
    for k,v in command_params.items():
        if k == 'hello': continue
        v[1].append((eppdoc_assemble.TAG_clTRID,(0,1),(),_T('Client transaction ID'),'unique_transaction_id','',()))
    return command_params

def make_sort_by_names():
    'Returns tuple of names used for sorting received values'
    #----------------------------------
    #
    # OUTPUT SORTED BY NAMES
    # (key, verbose, description)
    # verbose 1: shown in verbose 1 and higher
    #         2: shown in verbose 2 and higher
    #         ...
    #----------------------------------
    sort_by_names = {
    
       'contact:info': ('contact',(
         ('id',          1,  _T('Contact ID')),
         ('roid',        1,  _T('Repository object ID')),
         ('crID',        1,  _T("Created by")),
         ('clID',        1,  _T("Designated registrar")),
         ('upID',        1,  _T("Updated by")),
         ('crDate',      1,  _T('Created on')),
         ('trDate',      1,  _T('Last transfer on')),
         ('upDate',      1,  _T('Last update on')),
         ('name',        1,  _T('Name')),
         ('org',         1,  _T('Organisation')),
         ('street',      1,  _T('Street')),
         ('city',        1,  _T('City')),
         ('sp',          1,  _T('State or province')),
         ('pc',          1,  _T('Postal code')),
         ('cc',          1,  _T('Country code')),
         ('authInfo',    1,  _T('Password for transfer')),
         ('voice',       1,  _T('Phone')),
         ('fax',         1,  'Fax'),
         ('email',       1,  'Email'),
         ('notifyEmail', 1,  _T('Notification email')),
         ('status.s',    1,  _T('Status')),
         ('status',      1,  _T('Status message')),
         ('disclose',    1,  _T('Disclose')),
         ('hide',        1,  _T('Hide')),
         ('vat',         1,  _T('VAT')),
         ('ident.type',  1,  _T('Identificator type')),
         ('ident',       1,  _T('Identificator')),
         )),

       'domain:info': ('domain',(
         ('name',        1,  _T('Domain name')),
         ('roid',        1,  _T('Repository object ID')),
         ('crID',        1,  _T("Created by")),
         ('clID',        1,  _T("Designated registrar")),
         ('upID',        1,  _T("Updated by")),
         ('crDate',      1,  _T('Created on')),
         ('trDate',      1,  _T('Last transfer on')),
         ('upDate',      1,  _T('Last update on')),
         ('exDate',      1,  _T('Expiration date')),
         ('valExDate',   1,  _T('Validation expires at')), # validace platná do
         ('renew',       1,  _T('Last renew on')),
         ('nsset',       1,  _T('NSSET ID')),
         ('authInfo',    1,  _T('Password for transfer')),
         ('status.s',    1,  _T('Status')),
         ('status',      1,  _T('Status message')),
         ('registrant',  1,  _T('Registrant ID')),
         ('admin',       1,  _T('Administrative contact')),
         )),

       'nsset:info': ('nsset',(
         ('id',          1,  _T('NSSET ID')),
         ('roid',        1,  _T('Repository object ID')),
         ('crID',        1,  _T("Created by")),
         ('clID',        1,  _T("Designated registrar")),
         ('upID',        1,  _T("Updated by")),
         ('crDate',      1,  _T('Created on')),
         ('trDate',      1,  _T('Last transfer on')),
         ('upDate',      1,  _T('Last updated on')),
         ('authInfo',    1,  _T('Password for transfer')),
         ('status.s',    1,  _T('Status')),
         ('status',      1,  _T('Status message')),
         ('tech',        1,  _T('Technical contact')),
         ('ns',          1,  _T('Name servers')),
         ('reportlevel', 1,  _T('Report level')),
         )),

       'contact:create': ('contact',(
         ('id',          1,  _T('Contact ID')),
         ('crDate',      1,  _T('Created on')),
         )),
         
       'nsset:create': ('nsset',(
         ('id',          1,  _T('NSSET ID')),
         ('crDate',      1,  _T('Created on')),
         )),

       'domain:create': ('domain',(
         ('name',        1,  _T('Domain name')),
         ('crDate',      1,  _T('Created on')),
         ('exDate',      1,  _T('Expiration date')),
         )),

       'hello': ('',(
         ('lang',        2,  _T('Available languages')),
         ('svID',        1,  _T('Server ID')),
         ('svDate',      2,  _T('Server date')),
         ('version',     2,  _T('Server version')),
         ('objURI',      2,  _T('Objects URI')),
         ('extURI',      2,  _T('Extensions URI')),
         ('dcp',         2,  _T('Data Collection policy')), # Soubor zásad Pravidla přístupu
         # Turn OFF for the time being:
         #('dcp.access',  2,  _T('DCP: Access')), # přístup
         #('dcp.statement',  2,  _T('DCP: Statement')), # specifikace, příkaz, zpráva, prohlášení
         #('dcp.statement.purpose',  2,  _T('DCP: Statement: Purpose')), # účel,záměr
         #('dcp.statement.recipient',  2,  _T('DCP: Statement: Recipient')), # příjemce
         #('dcp.statement.retention',  2,  _T('DCP: Statement: Retention')), # uchování, zapamatování
         )),

       'domain:list': ('',(
         ('list',        1,  _T('List')),
         ('count',       1,  _T('Count')),
         )),

       'poll': ('',(
         ('msgQ.count',  1,  _T('Queue size')),
         ('msgQ.id',     1,  _T('Message ID')),
         ('qDate',       1,  _T('Message date')),
         ('msg',         1,  _T('Message content')),
         )),

       'domain:renew': ('domain',(
         ('name',        1,  _T('Domain name')),
         ('exDate',      1,  _T('Expiration date')),
         )),        
    }
    # append similar objects
    sort_by_names['contact:list']   = sort_by_names['domain:list']
    sort_by_names['nsset:list']     = sort_by_names['domain:list']
    return sort_by_names
    
class Message(eppdoc_assemble.Message):
    "Client EPP commands."

    def get_sort_by_names(self, command_name):
        'Prepare column names for sorted output answer.'
        if re.match('check_',self._dct.get('command',[''])[0]):
            # check commands sort by parameters
            names = map(lambda s: (s,1,s), self._dct.get('name',[])) # (key, verbose_level, description)
        else:
            # othes commands sort by defined namse
            scope = self.sort_by_names.get(command_name,None)
            if scope:
                if scope[0]:
                    names = map(lambda i: ('%s:%s'%(scope[0],i[0]),i[1],i[2]),scope[1])
                else:
                    names = scope[1]
            else:
                names = []
        return names

    def __init__(self):
        eppdoc_assemble.Message.__init__(self)
        self._command_params = make_command_parameters()
        self.sort_by_names = make_sort_by_names()
    
    def reset_translation(self):
        'Reset struct with translation after changing language'
        self._command_params = make_command_parameters()
        self.sort_by_names = make_sort_by_names()
        self.make_param_required_types()
    
def test(commands):
    import pprint
    import session_base
    manag = session_base.ManagerBase()
    epp = Message()
    manag.load_config()
    print "#"*60
    for cmd in commands:
        print "COMMAND:",cmd
        m = re.match('(\S+)',cmd)
        if not m: continue
        cmd_name = m.group(1)
        epp.reset()
        errors, example, stop = epp.parse_cmd(cmd_name, cmd, manag._conf, 0, 2)
        if stop == 2: break # User press Ctrl+C or Ctrl+D
        if errors:
            print "Errors:",errors
        else:
            getattr(epp,'assemble_%s'%cmd_name)('llcc002#06-06-16at13:21:30',('1.0', ('objURI',), ('extURI',), 'LANG'))
            errors, xmlepp = epp.get_results()
            print xmlepp
            if errors:
                print "Errors:",errors
            if xmlepp:
                print 'VALID?',manag.is_epp_valid(xmlepp)
        print "EXAMPLE:",epp.get_command_line(manag._session[session_base.NULL_VALUE])
        print '='*60

def test_help(command_names):
    import terminal_controler
    colored_output = terminal_controler.TerminalController()
    colored_output.set_mode(options['color'])
    epp = Message()
    for command_name in command_names:
        command_line,command_help,notice, examples = epp.get_help(command_name)
        print colored_output.render(command_line)
        print colored_output.render(command_help)
        print colored_output.render(notice)
        print '\nExamples:'
        print '\n'.join(examples)
        print '\n\n'

if __name__ == '__main__':
    # Test na jednotlivé příkazy
    test(("update_contact reg-id () () (('' '' ('' Město '' '' CZ)) '' '' '' (0) '' '' notify@mail.cz)",))
