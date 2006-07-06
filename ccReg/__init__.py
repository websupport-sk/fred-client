# -*- coding: utf8 -*-
#!/usr/bin/env python
"""
import ccReg

try:
    epp = new ccReg.Client()
    epp.login("reg-lrr","123456789")
    response = epp.check_contact(["handle1","handle2"])
    if response['handle1']:
        epp.create_contact("handle1", "My Name", "email@email.net", "City", "CZ")
    else:
        response = epp.info_contact("handle1")
        epp.show(response)
    epp.logout()
except error:
    print error.msg
"""

import cmd_history
from session_receiver import ManagerReceiver

class Client:
    """EPP client API. Process whole EPP communication with server.
    Defaults values you can save into config file.
    
    Every function does:

        - check input parameters
        - fill missing params from config
        - build EPP command
        - send EPP command to the server
        - waiting for answer
        - receive EPP server ansver
        - compile answer to the dictionary
        - returns dict whith values from server
        
    Functions accept parameters in this formats:
                       (for example)
        - string        login("user","pass")
        - list          check_domain(['domain1','domain2','domain3'])
        - dict          create_domain(period={'num':6, 'unit':'y'}, ...
        - list of dict  update_nsset('handle_nsset', {'ns':[{'name':'ns.name1', 'addr':'127.0.0.1'}, {'name':'ns.name2', 'addr':'127.2.2.2'}, ...], 'tech':'...'}, ...)

    Exception is raised if any error occurs.
    """
    
    def __init__(self):
        self._epp = ManagerReceiver()

    def check_contact(self, name):
        """Usage: check-contact name
    
    name (required)     unbounded list


   The EPP "check" command is used to determine if an object can be
   provisioned within a repository.  It provides a hint that allows a
   client to anticipate the success or failure of provisioning an object
   using the "create" command as object provisioning requirements are
   ultimately a matter of server policy.
   """
        return self._epp.api_command('check_contact',{'name':name})

    def check_domain(self, name):
        """Usage: check-domain name

    name (required)     unbounded list


   The EPP "check" command is used to determine if an object can be
   provisioned within a repository.  It provides a hint that allows a
   client to anticipate the success or failure of provisioning an object
   using the "create" command as object provisioning requirements are
   ultimately a matter of server policy.
   """
        return self._epp.api_command('check_domain',{'name':name})

    def check_nsset(self, name):
        """Usage: check-nsset name

    name (required)     unbounded list


   The EPP "check" command is used to determine if an object can be
   provisioned within a repository.  It provides a hint that allows a
   client to anticipate the success or failure of provisioning an object
   using the "create" command as object provisioning requirements are
   ultimately a matter of server policy.
   """
        return self._epp.api_command('check_nsset',{'name':name})

    def create_contact(self, contact_id, name, email, city, cc, org=None, 
            street=None, sp=None, pc=None, voice=None, fax=None, disclose=None,
            vat=None, ssn=None, notify_email=None):
        """Usage: create-contact contact-id name email city cc

    contact-id (required)
    name (required)
    email (required)
    city (required)
    cc (required)
    org (optional)
    street (optional)           list with max 3 items.
    sp (optional)
    pc (optional)
    voice (optional)
    fax (optional)
    disclose (optional)
        flag (required) accept only values: (0,1)
        name (optional)
        org (optional)
        addr (optional)
        voice (optional)
        fax (optional)
        email (optional)
    vat (optional)
    ssn (optional)
    notify_email (optional)


   The EPP "create" command is used to create an instance of an object.
   An object can be created for an indefinite period of time, or an
   object can be created for a specific validity period.

        """
        return self._epp.api_command('create_contact',{
            'contact-id':contact_id, 'name':name, 'email':email, 'city':city, 'cc':cc,
            'org':org, 'street':street, 'sp':sp, 'pc':pc, 'voice':voice, 'fax':fax,
            'disclose':disclose, 'vat':vat, 'ssn':ssn, 'notify_email':notify_email})

    def create_domain(self, name, pw, period=None, nsset=None, registrant=None, contact=None):
        """Usage: create-domain name pw

    name (required)
    pw (required)
    period (optional)
        num (required)
        unit (required) accept only values: (y,m)
    nsset (optional)
    registrant (optional)
    contact (optional)          unbounded list


   The EPP "create" command is used to create an instance of an object.
   An object can be created for an indefinite period of time, or an
   object can be created for a specific validity period.
    """
        return self._epp.api_command('create_domain',{'name':name,'pw':pw,
            'period':period,'nsset':nsset,'registrant':registrant,'contact':contact})

    def create_domain_enum(self, name, pw, period=None, nsset=None, registrant=None,
         contact=None, val_ex_date=None):
        """Usage: create-domain-enum name pw

    name (required)
    pw (required)
    period (optional)
        num (required)
        unit (required) accept only values: (y,m)
    nsset (optional)
    registrant (optional)
    contact (optional)          unbounded list
    val_ex_date (optional)


   The EPP "create" command is used to create an instance of an object.
   An object can be created for an indefinite period of time, or an
   object can be created for a specific validity period.

        """
        return self._epp.api_command('create_domain_enum',{'name':name, 
            'pw':pw, 'period':period, 'nsset':nsset, 'registrant':registrant, 
            'contact':contact, 'val_ex_date':val_ex_date})

    def create_nsset(self, nsset_id, pw, ns=None, tech=None):
        """Usage: create-nsset id pw

    id (required)
    pw (required)
    ns (optional)               list with max 9 items.
        name (required)
        addr (optional)         unbounded list
    tech (optional)             unbounded list


   The EPP "create" command is used to create an instance of an object.
   An object can be created for an indefinite period of time, or an
   object can be created for a specific validity period.

    Examples:
    create-nsset exampleNsset passw
    create-nsset exampleNsset passw ((ns1.domain.net (127.1.0.1 127.1.0.2)),(ns2.domain.net (127.2.0.1 127.2.0.2)),(ns3.domain.net (127.3.0.1 127.3.0.2))) tech-contact

        """
        return self._epp.api_command('create_nsset',{'id':nsset_id, 'pw':pw, 'ns':ns, 'tech':tech})


    def delete_contact(self, nsset_id):
        """Usage: delete-contact id

    id (required)

    The EPP "delete" command is used to remove an instance of an existing object.

        """
        return self._epp.api_command('delete_contact',{'id':nsset_id})


    def delete_domain(self, name):
        """Usage: delete-domain name

    name (required)

    The EPP "delete" command is used to remove an instance of an existing object.

        """
        return self._epp.api_command('delete_domain',{'name':name})


    def delete_nsset(self, nsset_id):
        """Usage: delete-nsset id

    id (required)

    The EPP "delete" command is used to remove an instance of an existing object.

        """
        return self._epp.api_command('delete_nsset',{'id':nsset_id})


    def hello(self):
        """Usage: hello

    The EPP "hello" request a "greeting" response message from an EPP server at any time.

        """
        return self._epp.api_command('hello')


    def info_contact(self, name):
        """Usage: info-contact name

    name (required)


   The EPP "info" command is used to retrieve information associated
   with an existing object. The elements needed to identify an object
   and the type of information associated with an object are both
   object-specific, so the child elements of the <info> command are
   specified using the EPP extension framework.

        """
        return self._epp.api_command('info_contact',{'name':name})


    def info_domain(self, name):
        """Usage: info-domain name

    name (required)


   The EPP "info" command is used to retrieve information associated
   with an existing object. The elements needed to identify an object
   and the type of information associated with an object are both
   object-specific, so the child elements of the <info> command are
   specified using the EPP extension framework.

        """
        return self._epp.api_command('info_domain',{'name':name})


    def info_nsset(self, name):
        """Usage: info-nsset name

    name (required)


   The EPP "info" command is used to retrieve information associated
   with an existing object. The elements needed to identify an object
   and the type of information associated with an object are both
   object-specific, so the child elements of the <info> command are
   specified using the EPP extension framework.

        """
        return self._epp.api_command('info_nsset',{'name':name})


    def login(self, username, password, new_password=None):
        """Usage: login username password

    username (required)
    password (required)
    new-password (optional)


   The "login" command establishes an ongoing server session that preserves client identity
   and authorization information during the duration of the session.

        """
        return self._epp.api_command('login',{'username':username, 
            'password':password, 'new-password':new_password})


    def logout(self):
        """Usage: logout

    The EPP "logout" command is used to end a session with an EPP server.

        """
        return self._epp.api_command('logout')


    def poll(self, op):
        """Usage: poll op

    op (required) accept only values: (req,ack)

    The EPP "poll" command is used to discover and retrieve service messages queued by a server for individual clients.

        """
        return self._epp.api_command('poll',{'op':op})


    def renew_domain(self, name, cur_exp_date, period=None):
        """Usage: renew-domain name cur_exp_date

    name (required)
    cur_exp_date (required)
    period (optional)
        num (required)
        unit (required) accept only values: (y,m)

    The EPP "renew" command is used to extend validity of an existing object.
        """
        return self._epp.api_command('renew_domain',{'name':name, 'cur_exp_date':cur_exp_date, 'period':period})


    def renew_domain_enum(self, name, cur_exp_date, period=None, valExDate=None):
        """Usage: renew-domain-enum name cur_exp_date

    name (required)
    cur_exp_date (required)
    period (optional)
        num (required)
        unit (required) accept only values: (y,m)
    val_ex_date (optional)

    The EPP "renew" command is used to extend validity of an existing object.

        """
        return self._epp.api_command('renew_domain_enum',{'name':name, 
            'cur_exp_date':cur_exp_date, 'period':period, 'val_ex_date':val_ex_date})


    def transfer_domain(self, name, op, passw):
        """Usage: transfer-domain name op passw

    name (required)
    op (required) accept only values: (request,approve,cancel,query,reject)
    passw (required)


   The EPP "transfer" command provides a query operation that allows a
   client to determine real-time status of pending and completed
   transfer requests.
   The EPP "transfer" command is used to manage changes in client
   sponsorship of an existing object.  Clients can initiate a transfer
   request, cancel a transfer request, approve a transfer request, and
   reject a transfer request using the "op" command attribute.
        """
        return self._epp.api_command('transfer_domain',{'name':name, 'op':op, 'passw':passw})


    def transfer_nsset(self, name, op, passw):
        """Usage: transfer-nsset name op passw

    name (required)
    op (required) accept only values: (request,approve,cancel,query,reject)
    passw (required)


   The EPP "transfer" command provides a query operation that allows a
   client to determine real-time status of pending and completed
   transfer requests.
   The EPP "transfer" command is used to manage changes in client
   sponsorship of an existing object.  Clients can initiate a transfer
   request, cancel a transfer request, approve a transfer request, and
   reject a transfer request using the "op" command attribute.

        """
        return self._epp.api_command('transfer_nsset',{'name':name, 'op':op, 'passw':passw})


    def update_contact(self, contact_id, add=None, rem=None, chg=None):
        """Usage: update-contact contact-id

    contact-id (required)
    add (optional)              list with max 5 items.
    rem (optional)              list with max 5 items.
    chg (optional)
        postalInfo (optional)
            name (optional)
            org (optional)
            addr (optional)
        voice (optional)
        fax (optional)
        email (optional)
        disclose (optional)
            flag (required) accept only values: (0,1)
            name (optional)
            org (optional)
            addr (optional)
            voice (optional)
            fax (optional)
            email (optional)
        vat (optional)
        ssn (optional)
        notifyEmail (optional)

    The EPP "update" command is used to update an instance of an existing object.
        """
        return self._epp.api_command('update_contact',{'contact-id':contact_id, 'add':add, 'rem':rem, 'chg':chg})


    def update_domain(self, name, add=None, rem=None, chg=None):
        """Usage: update-domain name

    name (required)
    add (optional)
        status (optional)       list with max 8 items. accept only values: (clientDeleteProhibited,clientTransferProhibited,clientUpdateProhibited,linked,ok,serverDeleteProhibited,serverTransferProhibited,serverUpdateProhibited)
        contact (optional)      unbounded list
    rem (optional)
        status (optional)       list with max 8 items. accept only values: (clientDeleteProhibited,clientTransferProhibited,clientUpdateProhibited,linked,ok,serverDeleteProhibited,serverTransferProhibited,serverUpdateProhibited)
        contact (optional)      unbounded list
    chg (optional)
        nsset (optional)
        registrant (optional)
        authInfo (optional)
            pw (optional)
            ext (optional)

    The EPP "update" command is used to update an instance of an existing object.
        """
        return self._epp.api_command('update_domain',{'name':name, 'add':add, 'rem':rem, 'chg':chg})


    def update_domain_enum(self, name, add=None, rem=None, chg=None, val_ex_date=None):
        """Usage: update-domain-enum name

    name (required)
    add (optional)
        status (optional)       list with max 8 items. accept only values: (clientDeleteProhibited,clientTransferProhibited,clientUpdateProhibited,linked,ok,serverDeleteProhibited,serverTransferProhibited,serverUpdateProhibited)
        contact (optional)      unbounded list
    rem (optional)
        status (optional)       list with max 8 items. accept only values: (clientDeleteProhibited,clientTransferProhibited,clientUpdateProhibited,linked,ok,serverDeleteProhibited,serverTransferProhibited,serverUpdateProhibited)
        contact (optional)      unbounded list
    chg (optional)
        nsset (optional)
        registrant (optional)
        authInfo (optional)
            pw (optional)
            ext (optional)
    val_ex_date (optional)

    The EPP "update" command is used to update an instance of an existing object.
        """
        return self._epp.api_command('update_domain_enum',{'name':name, 
            'add':add, 'rem':rem, 'chg':chg, 'val_ex_date':val_ex_date})


    def update_nsset(self, nsset_id, add=None, rem=None, chg=None):
        """Usage: update-nsset id

    id (required)
    add (optional)
        ns (optional)           list with max 9 items.
            name (required)
            addr (optional)     unbounded list
        tech (optional)         unbounded list
        status (optional)       list with max 6 items. accept only values: (clientDeleteProhibited,clientTransferProhibited,clientUpdateProhibited,linked,ok,serverDeleteProhibited,serverTransferProhibited,serverUpdateProhibited)
    rem (optional)
        name (optional)         list with max 9 items.
        tech (optional)         unbounded list
        status (optional)       list with max 6 items. accept only values: (clientDeleteProhibited,clientTransferProhibited,clientUpdateProhibited,linked,ok,serverDeleteProhibited,serverTransferProhibited,serverUpdateProhibited)
    chg (optional)
        pw (optional)
        ext (optional)

    The EPP "update" command is used to update an instance of an existing object.

    Examples:
    update-nsset nic.cz
    update-nsset nsset-ID (((nsset1.name.cz 127.0.0.1),(nsset2.name.cz (127.0.2.1 127.0.2.2)),) tech-add-contact ok) ("My Name",("Tech contact 1","Tech contact 2"),(clientDeleteProhibited ok)) (password extension)
        """
        return self._epp.api_command('update_nsset',{'id':nsset_id, 'add':add, 'rem':rem, 'chg':chg})
    
    def show(self, dct_response):
        "Show dict object."
        self._epp.__put_raw_into_note__(dct_response)
        self._epp.display()


class ClientSession(ManagerReceiver):
    "Use for console or batch applications."


if __name__ == '__main__':
    epp = Client()
    print epp.login("reg-lrr","123456789")
    print "[END]"

